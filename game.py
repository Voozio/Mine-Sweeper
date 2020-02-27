import pygame
import os
import sys
import menu
import board
import panel

# Screen
CAPTION = "Mine Sweeper"
SCREEN_SIZE = (784, 648)
BOMB_ICON = pygame.image.load('img/bombs/bomb32.png')

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Difficulty
EASY = 9
MEDIUM = 16
HARD = 22


class App:
    """
    A class to manage events and the game loop.
    """
    def __init__(self):
        """
        The board starts off initialized to None until a difficulty is selected.
        """
        self.screen = pygame.display.get_surface()
        self.screen_rect = self.screen.get_rect()
        self.state = "menu"

        self.menu = menu.Menu()
        self.board = None
        self.side_panel = panel.SidePanel()
        self.pause_menu = board.PauseMenu()

        self.clock = pygame.time.Clock()
        self.timer = 0
        self.fps = 60

    def event_loop(self):
        """
        Code is sectioned off by current state.
        The game states consist of: menu, game.
        The menu states consist of: main_menu, difficulty_menu, about_menu.
        The board has only one active state.
        """
        for event in pygame.event.get():
            mouse = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif self.state == "menu":
                if self.menu.get_menu_state() == "main_menu":
                    self.menu.check_hover(mouse)
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        self.menu.check_click(event.pos)
                    elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                        self.menu.no_click()
                elif self.menu.get_menu_state() == "difficulty_menu":
                    self.menu.check_hover(mouse)
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        self.menu.check_click(event.pos)
                    elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                        self.menu.no_click()
                elif self.menu.get_menu_state() == "rules_menu" or self.menu.get_menu_state() == "credits_menu":
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        self.menu.set_menu_state("main_menu")
                    else:
                        self.menu.no_click()
                elif self.menu.get_menu_state() == "hidden":
                    if self.menu.get_difficulty() is not None:
                        self.state = "board"
                        if self.menu.get_difficulty() == "easy":
                            self.board = board.Board(EASY)
                        elif self.menu.get_difficulty() == "medium":
                            self.board = board.Board(MEDIUM)
                        else:
                            self.board = board.Board(HARD)
            elif self.state == "board":
                if self.pause_menu.get_visible():
                    self.pause_menu.check_hover(mouse)
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        self.pause_menu.check_left_click(event.pos)
                    elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        if not self.board.is_game_over():
                            self.side_panel.toggle_pause()
                        self.pause_menu.toggle_visible()
                    else:
                        self.board.no_click()
                        self.pause_menu.no_click()
                elif not self.board.is_game_over():
                    self.board.check_hover(mouse)
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        self.board.check_left_click(event.pos)
                    elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                        self.board.check_right_click(event.pos)
                    elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        self.side_panel.toggle_pause()
                        self.pause_menu.toggle_visible()
                    else:
                        self.board.no_click()
                        self.pause_menu.no_click()
                elif self.board.get_win():
                    self.board.game_over_safe()
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        self.menu.check_click(event.pos)
                    elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        self.pause_menu.toggle_visible()
                    else:
                        self.board.no_click()
                        self.pause_menu.no_click()
                elif not self.board.get_win():
                    self.board.game_over_explosion()
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        self.menu.check_click(event.pos)
                    elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        self.pause_menu.toggle_visible()
                    else:
                        self.board.no_click()
                        self.pause_menu.no_click()

    def render(self):
        """
        All drawing is done through this method.
        This should be the only instance of pygame.display.update().
        """
        self.screen.fill(WHITE)
        if self.state == "menu":
            self.menu.draw(self.screen)
        elif self.state == "board":
            self.side_panel.draw(self.screen)
            if self.pause_menu.get_visible():
                self.pause_menu.draw(self.screen)
            else:
                self.board.draw(self.screen)
        pygame.display.update()

    def main_loop(self):
        """
        This is the main loop for the entire program.
        """
        running = True
        time_delta = 0
        self.clock.tick()

        while running:
            self.event_loop()
            if self.state == "menu":
                self.menu.update()
            elif self.state == "board":
                if self.pause_menu.get_visible():
                    temp = self.pause_menu.update()
                    if temp == 0:
                        if not self.board.is_game_over():
                            self.side_panel.toggle_pause()
                        self.pause_menu.toggle_visible()
                    elif temp == 1:
                        if not self.board.is_game_over():
                            self.side_panel.toggle_pause()
                        self.timer = 0
                        self.board.reset()
                        self.pause_menu.toggle_visible()
                    elif temp == 2:
                        self.full_reset()
                elif not self.board.is_game_over():
                    self.timer += time_delta
                    self.board.update()
                    self.side_panel.update(self.timer, self.board.get_flags_remaining())
            self.render()
            time_delta = self.clock.tick(self.fps)

    def full_reset(self):
        self.state = "menu"
        self.menu = menu.Menu()
        self.board = None
        self.side_panel = panel.SidePanel()
        self.pause_menu = board.PauseMenu()

        self.clock = pygame.time.Clock()
        self.timer = 0


def main():
    """
    Prepares the environment to center the window, create a display, and start the program.
    """
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pygame.init()
    pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption(CAPTION)
    pygame.display.set_icon(BOMB_ICON)
    App().main_loop()


if __name__ == "__main__":
    main()
