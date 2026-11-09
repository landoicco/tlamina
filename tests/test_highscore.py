from pathlib import Path

import pytest

from tlamina import highscore
from tlamina.game import GAME_OVER
from tlamina.highscore import load_high_score, save_high_score
from tlamina.scenes import GameOverScene, SplashScene


def test_no_saved_file_means_zero():
    assert load_high_score() == 0


def test_a_saved_score_loads_back(data_dir):
    save_high_score(1230)

    assert load_high_score() == 1230
    assert (data_dir / 'highscore.json').is_file()


@pytest.mark.parametrize('content', ['', 'not json', '{"high_score": "lots"}', '[]', '{}'])
def test_a_damaged_file_means_zero(data_dir, content):
    data_dir.mkdir()
    (data_dir / 'highscore.json').write_text(content)

    assert load_high_score() == 0


def test_saving_where_it_cannot_write_does_not_crash(data_dir):
    # A file where the folder should be makes creating the folder fail
    data_dir.write_text('')

    save_high_score(100)

    assert load_high_score() == 0


@pytest.mark.parametrize(
    ('platform', 'env', 'expected'),
    [
        ('linux', {'XDG_DATA_HOME': '/xdg'}, Path('/xdg/tlamina')),
        ('linux', {}, Path.home() / '.local' / 'share' / 'tlamina'),
        ('win32', {'APPDATA': 'C:/Users/me/AppData/Roaming'}, Path('C:/Users/me/AppData/Roaming/tlamina')),
    ],
)
def test_data_dir_follows_the_platform(monkeypatch, platform, env, expected):
    monkeypatch.delenv('TLAMINA_DATA_DIR')
    monkeypatch.delenv('XDG_DATA_HOME', raising=False)
    monkeypatch.delenv('APPDATA', raising=False)
    for name, value in env.items():
        monkeypatch.setenv(name, value)
    monkeypatch.setattr(highscore.sys, 'platform', platform)

    assert highscore.data_dir() == expected


def game_over_with(game, score):
    game.score = score
    game.state = GAME_OVER
    return GameOverScene(game)


def test_beating_the_high_score_saves_it(game):
    save_high_score(100)

    scene = game_over_with(game, 250)

    assert scene.new_record
    assert load_high_score() == 250


def test_a_lower_score_keeps_the_high_score(game):
    save_high_score(300)

    scene = game_over_with(game, 250)

    assert not scene.new_record
    assert scene.high_score == 300
    assert load_high_score() == 300


def test_a_score_of_zero_is_not_a_record(game):
    assert not game_over_with(game, 0).new_record


def test_the_splash_shows_the_saved_high_score(keys):
    save_high_score(800)

    assert SplashScene().high_score == 800
