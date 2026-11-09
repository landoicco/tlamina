import pygame
import pytest

from tlamina.game import GAME_OVER
from tlamina.scenes import GameOverScene, PausedScene, PlayingScene, SplashScene
from tlamina.settings import SCREEN_HEIGHT, SCREEN_WIDTH


def key_down(key):
    return pygame.event.Event(pygame.KEYDOWN, key=key)


@pytest.fixture
def playing(game):
    return PlayingScene(game)


def test_any_key_on_the_splash_starts_a_game(keys):
    scene = SplashScene().handle_event(key_down(pygame.K_a))

    assert isinstance(scene, PlayingScene)


def test_splash_ignores_other_events(keys):
    splash = SplashScene()

    assert splash.handle_event(pygame.event.Event(pygame.MOUSEMOTION, pos=(0, 0))) is splash


def click(pos):
    return pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1, pos=pos)


def test_clicking_the_portfolio_link_opens_it(monkeypatch, keys):
    opened = []
    monkeypatch.setattr('webbrowser.open', opened.append)
    splash = SplashScene()

    assert splash.handle_event(click(splash.link_rect.center)) is splash
    assert opened == ['https://licaza.dev']


def test_clicking_elsewhere_on_the_splash_does_nothing(monkeypatch, keys):
    opened = []
    monkeypatch.setattr('webbrowser.open', opened.append)
    splash = SplashScene()

    assert splash.handle_event(click((0, 0))) is splash
    assert opened == []


def test_hovering_the_portfolio_link_highlights_it(monkeypatch, keys):
    splash = SplashScene()
    monkeypatch.setattr(pygame.mouse, 'get_pos', lambda: splash.link_rect.center)

    splash.update(1 / 60)

    assert splash.link_hovered


def test_escape_pauses_and_resumes_the_same_game(playing):
    paused = playing.handle_event(key_down(pygame.K_ESCAPE))
    assert isinstance(paused, PausedScene)

    assert paused.handle_event(key_down(pygame.K_ESCAPE)) is playing


def test_losing_window_focus_pauses(playing):
    scene = playing.handle_event(pygame.event.Event(pygame.WINDOWFOCUSLOST))

    assert isinstance(scene, PausedScene)


def test_the_game_does_not_move_while_paused(playing):
    paused = playing.handle_event(key_down(pygame.K_ESCAPE))
    positions = [enemy.rect.topleft for enemy in playing.game.enemies]

    for _ in range(60):
        paused.update(1 / 60)

    assert [enemy.rect.topleft for enemy in playing.game.enemies] == positions


def test_game_over_shows_the_game_over_scene(playing):
    playing.game.state = GAME_OVER

    scene = playing.update(1 / 60)

    assert isinstance(scene, GameOverScene)
    assert scene.game is playing.game


@pytest.mark.parametrize('key', [pygame.K_RETURN, pygame.K_KP_ENTER])
def test_enter_after_game_over_starts_a_new_game(game, key):
    game.score = 500
    game.state = GAME_OVER

    scene = GameOverScene(game).handle_event(key_down(key))

    assert isinstance(scene, PlayingScene)
    assert scene.game is not game
    assert scene.game.score == 0


def test_every_scene_updates_and_draws(keys):
    # Walk through every scene, a few frames each, to catch crashes in drawing code
    surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    scene = SplashScene()
    for event in (key_down(pygame.K_SPACE), key_down(pygame.K_ESCAPE), key_down(pygame.K_ESCAPE)):
        for _ in range(30):
            scene = scene.update(1 / 60)
            scene.draw(surface)
        scene = scene.handle_event(event)
    scene.game.state = GAME_OVER
    for _ in range(30):
        scene = scene.update(1 / 60)
        scene.draw(surface)

    assert isinstance(scene, GameOverScene)
