import pygame
import pytest

from tlamina.entities.enemy import Ufo
from tlamina.entities.laser import Laser
from tlamina.entities.powerup import PowerUp
from tlamina.settings import (
    ENEMY_LASER_SPEED,
    PLAYER_LASER_COOLDOWN,
    PLAYER_LASER_SPEED,
    PLAYER_LIVES,
    POWERUP_SPRITES,
    POWERUP_TIME,
    RAPID_FIRE_COOLDOWN,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
)


def shoot_down_ufo(game):
    ufo = Ufo('left')
    ufo.rect.center = (SCREEN_WIDTH / 2, 100)
    game.ufo.add(ufo)
    game.player.sprite.lasers.add(Laser(ufo.rect.center, PLAYER_LASER_SPEED))
    game.collision_checks()
    return ufo


def test_the_bonus_ufo_drops_a_power_up(game):
    ufo = shoot_down_ufo(game)

    assert len(game.powerups) == 1
    powerup = game.powerups.sprites()[0]
    assert powerup.kind in POWERUP_SPRITES
    assert powerup.rect.center == pytest.approx(ufo.rect.center)


def test_power_ups_fall_and_leave_the_screen():
    group = pygame.sprite.Group(PowerUp((100, 100), 'shield'))
    powerup = group.sprites()[0]

    group.update(0.5)
    assert powerup.rect.centery > 100

    for _ in range(60 * 10):
        group.update(1 / 60)
    assert not powerup.alive()


def catch(game, kind):
    powerup = PowerUp(game.player.sprite.rect.center, kind)
    game.powerups.add(powerup)
    game.collision_checks()
    return powerup


@pytest.mark.parametrize('kind', list(POWERUP_SPRITES))
def test_catching_a_power_up_activates_it(game, kind):
    powerup = catch(game, kind)

    assert not powerup.alive()
    assert game.player.sprite.has(kind)


def test_power_ups_run_out(game):
    catch(game, 'volley')
    player = game.player.sprite

    player.update(POWERUP_TIME - 0.1)
    assert player.has('volley')

    player.update(0.2)
    assert not player.has('volley')
    assert player.powerups == {}


def test_catching_one_again_restarts_its_timer(game):
    catch(game, 'rapid_fire')
    player = game.player.sprite
    player.update(POWERUP_TIME - 1)

    catch(game, 'rapid_fire')

    assert player.powerups['rapid_fire'] == POWERUP_TIME


def test_volley_fires_a_fan_of_three_lasers_as_one_shot(game):
    catch(game, 'volley')
    player = game.player.sprite

    player.shoot_laser()

    lasers = player.lasers.sprites()
    assert len(lasers) == 3
    assert len({laser.shot for laser in lasers}) == 1
    assert sorted(laser.x_speed > 0 for laser in lasers) == [False, False, True]
    assert any(laser.x_speed < 0 for laser in lasers)


def test_rapid_fire_shortens_the_cooldown(game):
    player = game.player.sprite
    player.shoot_laser()
    assert player.cooldown_left == PLAYER_LASER_COOLDOWN

    catch(game, 'rapid_fire')
    player.cooldown_left = 0
    player.shoot_laser()

    assert player.cooldown_left == RAPID_FIRE_COOLDOWN


def test_the_shield_absorbs_one_hit(game):
    catch(game, 'shield')
    game.combo_hits = 7
    player = game.player.sprite

    game.enemy_lasers.add(Laser(player.rect.center, ENEMY_LASER_SPEED))
    game.collision_checks()

    assert game.lives == PLAYER_LIVES
    assert game.combo_hits == 7
    assert not player.has('shield')

    game.enemy_lasers.add(Laser(player.rect.center, ENEMY_LASER_SPEED))
    game.collision_checks()

    assert game.lives == PLAYER_LIVES - 1


def test_the_hud_and_shield_draw_with_every_power_up_active(game):
    surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    for kind in POWERUP_SPRITES:
        catch(game, kind)

    for _ in range(round(POWERUP_TIME * 60) + 1):
        game.player.sprite.update(1 / 60)
        game.draw(surface)

    assert game.player.sprite.powerups == {}
