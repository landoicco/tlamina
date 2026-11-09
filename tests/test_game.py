import pygame
import pytest

from tlamina.entities.enemy import Ufo, enemy_sprite
from tlamina.entities.laser import Laser
from tlamina.game import GAME_OVER, PLAYING, Game
from tlamina.resources import load_sprite
from tlamina.settings import (
    ARMORED_FROM_WAVE,
    ENEMY_COLS,
    ENEMY_DROP,
    ENEMY_FLASH_TIME,
    ENEMY_LASER_SPEED,
    ENEMY_MODELS,
    ENEMY_ROW_COLORS,
    PLAYER_INVULNERABLE_TIME,
    PLAYER_LASER_COOLDOWN,
    PLAYER_LASER_SPEED,
    PLAYER_LIVES,
    SCREEN_WIDTH,
    UFO_POINTS,
)


def player_laser_at(game, pos):
    laser = Laser(pos, PLAYER_LASER_SPEED)
    game.player.sprite.lasers.add(laser)
    return laser


def enemy_laser_at(game, pos):
    laser = Laser(pos, ENEMY_LASER_SPEED)
    game.enemy_lasers.add(laser)
    return laser


# Scoring


def test_destroying_an_enemy_adds_its_points(game):
    enemy = game.enemies.sprites()[0]
    laser = player_laser_at(game, enemy.rect.center)

    game.collision_checks()

    assert game.score == enemy.value
    assert not enemy.alive()
    assert not laser.alive()


def test_destroying_the_bonus_ufo_adds_bonus_points(game):
    ufo = Ufo('left')
    ufo.rect.center = (SCREEN_WIDTH / 2, 100)
    game.ufo.add(ufo)
    player_laser_at(game, ufo.rect.center)

    game.collision_checks()

    assert game.score == UFO_POINTS
    assert not ufo.alive()


def test_obstacles_block_player_lasers(game):
    rock = game.obstacles.sprites()[0]
    laser = player_laser_at(game, rock.rect.center)

    game.collision_checks()

    assert game.score == 0
    assert not rock.alive()
    assert not laser.alive()


# Lives and game over


def test_getting_hit_costs_a_life(game):
    laser = enemy_laser_at(game, game.player.sprite.rect.center)

    game.collision_checks()

    assert game.lives == PLAYER_LIVES - 1
    assert game.state == PLAYING
    assert not laser.alive()


def test_losing_the_last_life_ends_the_game(game):
    game.lives = 1
    enemy_laser_at(game, game.player.sprite.rect.center)

    game.collision_checks()

    assert game.lives == 0
    assert game.state == GAME_OVER


def test_an_enemy_reaching_the_player_ends_the_game(game):
    game.enemies.sprites()[0].rect.center = game.player.sprite.rect.center

    game.collision_checks()

    assert game.state == GAME_OVER


def test_a_hit_makes_the_player_briefly_invulnerable(game):
    player = game.player.sprite
    enemy_laser_at(game, player.rect.center)
    game.collision_checks()

    second = enemy_laser_at(game, player.rect.center)
    game.collision_checks()

    assert game.lives == PLAYER_LIVES - 1
    assert second.alive()

    player.update(PLAYER_INVULNERABLE_TIME)
    game.collision_checks()

    assert game.lives == PLAYER_LIVES - 2


def test_the_player_blinks_while_invulnerable(game):
    player = game.player.sprite
    assert player.visible

    player.take_hit(1)
    seen = set()
    for _ in range(round(PLAYER_INVULNERABLE_TIME * 60)):
        player.update(1 / 60)
        seen.add(player.visible)

    assert seen == {True, False}
    assert player.visible


def test_hits_crack_the_ship(game):
    player = game.player.sprite
    clean = pygame.image.tobytes(player.image, 'RGBA')

    player.take_hit(1)
    cracked = pygame.image.tobytes(player.image, 'RGBA')

    assert cracked != clean
    # The shared, cached ship sprite stays clean
    assert pygame.image.tobytes(load_sprite('playerShip1_blue'), 'RGBA') == clean


# Effects


def test_destroying_an_enemy_explodes_and_shows_its_points(game):
    enemy = game.enemies.sprites()[0]
    player_laser_at(game, enemy.rect.center)

    game.collision_checks()

    kinds = {type(item).__name__ for item in game.effects.items}
    assert kinds == {'Particle', 'FloatingText'}


def test_hitting_an_armored_enemy_sparks(game):
    enemy = game.enemies.sprites()[0]
    enemy.health = 2
    player_laser_at(game, enemy.rect.center)

    game.collision_checks()

    assert [type(item).__name__ for item in game.effects.items] == ['Spark']


def test_getting_hit_shakes_the_screen(game):
    enemy_laser_at(game, game.player.sprite.rect.center)

    game.collision_checks()

    assert game.effects.shake_left > 0


# Enemy fleet


def move_fleet_to_right_edge(game):
    rightmost = max(enemy.rect.right for enemy in game.enemies)
    for enemy in game.enemies:
        enemy.rect.x += SCREEN_WIDTH - rightmost


@pytest.mark.parametrize('enemies_left_in_edge_column', [1, 2, 3])
def test_fleet_bounces_once_per_edge_hit(game, enemies_left_in_edge_column):
    rightmost = max(enemy.rect.right for enemy in game.enemies)
    edge_column = [enemy for enemy in game.enemies if enemy.rect.right == rightmost]
    for enemy in edge_column[enemies_left_in_edge_column:]:
        enemy.kill()
    move_fleet_to_right_edge(game)
    top_before = min(enemy.rect.top for enemy in game.enemies)
    speed_before = game.enemy_x_speed

    game.enemy_position_checker()
    game.enemy_position_checker()

    assert game.enemy_x_speed == -speed_before
    assert min(enemy.rect.top for enemy in game.enemies) == top_before + ENEMY_DROP


def fleet_position_after(seconds, fps):
    game = Game()
    game.obstacles.empty()
    game.enemy_shoot = lambda: None
    for _ in range(round(seconds * fps)):
        game.enemies.update(game.enemy_x_speed, 1 / fps)
        game.enemy_position_checker()
    enemy = min(game.enemies, key=lambda e: (e.rect.top, e.rect.left))
    return enemy.rect.left, enemy.rect.top


@pytest.mark.parametrize('fps', [30, 144])
def test_fleet_movement_does_not_depend_on_frame_rate(keys, fps):
    expected_left, expected_top = fleet_position_after(20, 60)
    left, top = fleet_position_after(20, fps)

    assert left == pytest.approx(expected_left, abs=0.5)
    assert top == expected_top


# Lasers and bonus ufo


def test_lasers_are_removed_off_screen(game):
    up = player_laser_at(game, (SCREEN_WIDTH / 2, 0))
    down = enemy_laser_at(game, (SCREEN_WIDTH / 2, game.player.sprite.rect.bottom))

    for _ in range(10):
        game.player.sprite.lasers.update(1 / 60)
        game.enemy_lasers.update(1 / 60)

    assert not up.alive()
    assert not down.alive()


@pytest.mark.parametrize('side', ['left', 'right'])
def test_bonus_ufo_is_removed_after_crossing_the_screen(game, side):
    ufo = Ufo(side)
    game.ufo.add(ufo)

    for _ in range(60 * 10):
        game.ufo.update(1 / 60)

    assert not ufo.alive()


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


# Waves


def clear_wave(game):
    game.enemies.empty()
    game.update(0)


def test_clearing_the_fleet_starts_a_faster_wave(game):
    speed_before = abs(game.enemy_x_speed)
    interval_before = game.enemy_laser_interval

    clear_wave(game)

    assert game.wave == 2
    assert len(game.enemies) == len(ENEMY_ROW_COLORS) * ENEMY_COLS
    assert abs(game.enemy_x_speed) > speed_before
    assert game.enemy_laser_interval < interval_before


def test_each_wave_uses_the_next_enemy_model(game):
    for wave in range(1, ENEMY_MODELS + 2):
        model = (wave - 1) % ENEMY_MODELS + 1
        for enemy in game.enemies:
            assert enemy.image in {load_sprite(enemy_sprite(color, model)) for color in ENEMY_ROW_COLORS}
        clear_wave(game)


def back_row(game):
    top = min(enemy.rect.top for enemy in game.enemies)
    return [enemy for enemy in game.enemies if enemy.rect.top == top]


def test_the_back_row_is_armored_from_wave_3(game):
    while game.wave < ARMORED_FROM_WAVE - 1:
        clear_wave(game)
    assert all(enemy.health == 1 for enemy in game.enemies)

    clear_wave(game)

    armored = back_row(game)
    assert len(armored) == ENEMY_COLS
    assert all(enemy.health == 2 for enemy in armored)
    assert all(enemy.health == 1 for enemy in game.enemies if enemy not in armored)


def test_an_armored_enemy_takes_two_hits(game):
    enemy = game.enemies.sprites()[0]
    enemy.health = 2

    first = player_laser_at(game, enemy.rect.center)
    game.collision_checks()

    assert enemy.alive()
    assert not first.alive()
    assert game.score == 0
    assert enemy.image is enemy.flash_image

    player_laser_at(game, enemy.rect.center)
    game.collision_checks()

    assert not enemy.alive()
    assert game.score == enemy.value


def test_the_hit_flash_wears_off(game):
    enemy = game.enemies.sprites()[0]
    enemy.health = 2
    enemy.hit()

    enemy.update(0, ENEMY_FLASH_TIME + 0.01)

    assert enemy.image is enemy.normal_image
