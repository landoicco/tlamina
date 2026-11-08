import pygame
import pytest

from enemy import Alien
from game import GAME_OVER, PLAYING, Game
from laser import Laser
from settings import (
    ALIEN_POINTS,
    PLAYER_LASER_COOLDOWN,
    PLAYER_LASER_SPEED,
    PLAYER_LIVES,
    SCREEN_WIDTH,
    UFO_DROP,
    UFO_LASER_SPEED,
)


def player_laser_at(game, pos):
    laser = Laser(pos, PLAYER_LASER_SPEED)
    game.player.sprite.lasers.add(laser)
    return laser


def ufo_laser_at(game, pos):
    laser = Laser(pos, UFO_LASER_SPEED)
    game.ufo_lasers.add(laser)
    return laser


# Scoring


def test_destroying_a_ufo_adds_its_points(game):
    ufo = game.ufos.sprites()[0]
    laser = player_laser_at(game, ufo.rect.center)

    game.collision_checks()

    assert game.score == ufo.value
    assert not ufo.alive()
    assert not laser.alive()


def test_destroying_the_bonus_alien_adds_bonus_points(game):
    alien = Alien('left')
    alien.rect.center = (SCREEN_WIDTH / 2, 100)
    game.alien.add(alien)
    player_laser_at(game, alien.rect.center)

    game.collision_checks()

    assert game.score == ALIEN_POINTS
    assert not alien.alive()


def test_obstacles_block_player_lasers(game):
    rock = game.obstacles.sprites()[0]
    laser = player_laser_at(game, rock.rect.center)

    game.collision_checks()

    assert game.score == 0
    assert not rock.alive()
    assert not laser.alive()


# Lives and game over


def test_getting_hit_costs_a_life(game):
    laser = ufo_laser_at(game, game.player.sprite.rect.center)

    game.collision_checks()

    assert game.lives == PLAYER_LIVES - 1
    assert game.state == PLAYING
    assert not laser.alive()


def test_losing_the_last_life_ends_the_game(game):
    game.lives = 1
    ufo_laser_at(game, game.player.sprite.rect.center)

    game.collision_checks()

    assert game.lives == 0
    assert game.state == GAME_OVER


def test_a_ufo_reaching_the_player_ends_the_game(game):
    game.ufos.sprites()[0].rect.center = game.player.sprite.rect.center

    game.collision_checks()

    assert game.state == GAME_OVER


# Ufo fleet


def move_fleet_to_right_edge(game):
    rightmost = max(ufo.rect.right for ufo in game.ufos)
    for ufo in game.ufos:
        ufo.rect.x += SCREEN_WIDTH - rightmost


@pytest.mark.parametrize('ufos_left_in_edge_column', [1, 2, 3])
def test_fleet_bounces_once_per_edge_hit(game, ufos_left_in_edge_column):
    rightmost = max(ufo.rect.right for ufo in game.ufos)
    edge_column = [ufo for ufo in game.ufos if ufo.rect.right == rightmost]
    for ufo in edge_column[ufos_left_in_edge_column:]:
        ufo.kill()
    move_fleet_to_right_edge(game)
    top_before = min(ufo.rect.top for ufo in game.ufos)
    speed_before = game.ufo_x_speed

    game.ufo_position_checker()
    game.ufo_position_checker()

    assert game.ufo_x_speed == -speed_before
    assert min(ufo.rect.top for ufo in game.ufos) == top_before + UFO_DROP


def fleet_position_after(seconds, fps):
    game = Game()
    game.obstacles.empty()
    game.ufo_shoot = lambda: None
    for _ in range(round(seconds * fps)):
        game.ufos.update(game.ufo_x_speed, 1 / fps)
        game.ufo_position_checker()
    ufo = min(game.ufos, key=lambda u: (u.rect.top, u.rect.left))
    return ufo.rect.left, ufo.rect.top


@pytest.mark.parametrize('fps', [30, 144])
def test_fleet_movement_does_not_depend_on_frame_rate(keys, fps):
    expected_left, expected_top = fleet_position_after(20, 60)
    left, top = fleet_position_after(20, fps)

    assert left == pytest.approx(expected_left, abs=0.5)
    assert top == expected_top


# Lasers and bonus alien


def test_lasers_are_removed_off_screen(game):
    up = player_laser_at(game, (SCREEN_WIDTH / 2, 0))
    down = ufo_laser_at(game, (SCREEN_WIDTH / 2, game.player.sprite.rect.bottom))

    for _ in range(10):
        game.player.sprite.lasers.update(1 / 60)
        game.ufo_lasers.update(1 / 60)

    assert not up.alive()
    assert not down.alive()


@pytest.mark.parametrize('side', ['left', 'right'])
def test_bonus_alien_is_removed_after_crossing_the_screen(game, side):
    alien = Alien(side)
    game.alien.add(alien)

    for _ in range(60 * 10):
        game.alien.update(1 / 60)

    assert not alien.alive()


# Player


def test_player_shooting_respects_the_cooldown(game, keys):
    keys.add(pygame.K_SPACE)
    player = game.player.sprite

    player.update(0)
    assert len(player.lasers) == 1

    player.update(PLAYER_LASER_COOLDOWN - 0.05)
    assert len(player.lasers) == 1

    player.update(0.1)
    assert len(player.lasers) == 2


def test_player_stays_on_screen(game, keys):
    keys.add(pygame.K_RIGHT)
    player = game.player.sprite

    for _ in range(60 * 5):
        player.update(1 / 60)

    assert player.rect.right <= SCREEN_WIDTH
