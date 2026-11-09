import webbrowser

import pygame

from tlamina.game import GAME_OVER, Game
from tlamina.highscore import load_high_score, save_high_score
from tlamina.resources import load_font, load_sound
from tlamina.settings import BLINK_PERIOD, OVERLAY_ALPHA, SCREEN_HEIGHT, SCREEN_WIDTH
from tlamina.visuals.ui import draw_text

CENTER_X = SCREEN_WIDTH / 2
CENTER_Y = SCREEN_HEIGHT / 2

PORTFOLIO_TEXT = 'licaza.dev'
PORTFOLIO_URL = 'https://licaza.dev'
PORTFOLIO_SIZE = 14


def pressed(event, *keys):
    return event.type == pygame.KEYDOWN and event.key in keys


def blink_on(time):
    return time % BLINK_PERIOD < BLINK_PERIOD * 0.6


def set_cursor(cursor):
    # Cosmetic only: some video drivers (like the headless one in tests) have no system cursors
    try:
        pygame.mouse.set_cursor(cursor)
    except pygame.error:
        pass


def dim(surface):
    overlay = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, OVERLAY_ALPHA))
    surface.blit(overlay, (0, 0))


class Scene:
    """One screen of the game. handle_event and update return the scene to show next, usually self."""

    def handle_event(self, event):
        return self

    def update(self, dt):
        return self

    def draw(self, surface):
        pass


class SplashScene(Scene):
    def __init__(self):
        # Only the fleet of this game is used, as a moving backdrop
        self.backdrop = Game()
        self.time = 0
        self.high_score = load_high_score()
        self.link_rect = pygame.Rect((0, 0), load_font(PORTFOLIO_SIZE).size(PORTFOLIO_TEXT))
        self.link_rect.center = (CENTER_X, 712)
        self.link_hovered = False

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            set_cursor(pygame.SYSTEM_CURSOR_ARROW)
            return PlayingScene(Game())
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.link_rect.collidepoint(event.pos):
            webbrowser.open(PORTFOLIO_URL)
        return self

    def update(self, dt):
        self.time += dt
        self.backdrop.enemies.update(self.backdrop.enemy_x_speed, dt)
        self.backdrop.enemy_position_checker()

        hovered = self.link_rect.collidepoint(pygame.mouse.get_pos())
        if hovered != self.link_hovered:
            self.link_hovered = hovered
            set_cursor(pygame.SYSTEM_CURSOR_HAND if hovered else pygame.SYSTEM_CURSOR_ARROW)
        return self

    def draw(self, surface):
        self.backdrop.enemies.draw(surface)
        draw_text(surface, 'TLAMINA', 72, center=(CENTER_X, 515))
        if self.high_score:
            draw_text(surface, f'High score {self.high_score}', 16, 'gray70', center=(CENTER_X, 565))
        if blink_on(self.time):
            draw_text(surface, 'Press any key to start', 20, center=(CENTER_X, 615))
        draw_text(surface, 'by Lando Icaza', 14, 'gray70', center=(CENTER_X, 690))
        if self.link_hovered:
            draw_text(surface, PORTFOLIO_TEXT, PORTFOLIO_SIZE, center=self.link_rect.center)
            pygame.draw.line(surface, 'white', self.link_rect.move(0, 2).bottomleft, self.link_rect.move(0, 2).bottomright)
        else:
            draw_text(surface, PORTFOLIO_TEXT, PORTFOLIO_SIZE, 'gray70', center=self.link_rect.center)


class PlayingScene(Scene):
    def __init__(self, game):
        self.game = game
        self.lose_sfx = load_sound('assets/kenney/space-shooter-redux/sfx_lose.ogg', 0.5)

    def handle_event(self, event):
        # Also pause when the window loses focus, so the player can't die while away
        if pressed(event, pygame.K_ESCAPE) or event.type == pygame.WINDOWFOCUSLOST:
            return PausedScene(self)
        return self

    def update(self, dt):
        self.game.update(dt)
        if self.game.state == GAME_OVER:
            self.lose_sfx.play()
            return GameOverScene(self.game)
        return self

    def draw(self, surface):
        self.game.draw(surface)


class PausedScene(Scene):
    def __init__(self, playing):
        self.playing = playing

    def handle_event(self, event):
        if pressed(event, pygame.K_ESCAPE):
            return self.playing
        return self

    def draw(self, surface):
        self.playing.draw(surface)
        dim(surface)
        draw_text(surface, 'PAUSED', 48, center=(CENTER_X, CENTER_Y - 20))
        draw_text(surface, 'Press Esc to resume', 18, center=(CENTER_X, CENTER_Y + 40))


class GameOverScene(Scene):
    def __init__(self, game):
        self.game = game
        self.time = 0
        self.high_score = load_high_score()
        self.new_record = game.score > self.high_score
        if self.new_record:
            self.high_score = game.score
            save_high_score(game.score)

    def handle_event(self, event):
        if pressed(event, pygame.K_RETURN, pygame.K_KP_ENTER):
            return PlayingScene(Game())
        return self

    def update(self, dt):
        self.time += dt
        return self

    def draw(self, surface):
        self.game.draw(surface)
        dim(surface)
        draw_text(surface, 'GAME OVER', 48, center=(CENTER_X, CENTER_Y - 60))
        draw_text(surface, f'Score {self.game.score}', 24, center=(CENTER_X, CENTER_Y))
        if self.new_record:
            draw_text(surface, 'New high score', 18, 'gold', center=(CENTER_X, CENTER_Y + 40))
        else:
            draw_text(surface, f'High score {self.high_score}', 18, 'gray70', center=(CENTER_X, CENTER_Y + 40))
        if blink_on(self.time):
            draw_text(surface, 'Press Enter to play again', 18, center=(CENTER_X, CENTER_Y + 100))
