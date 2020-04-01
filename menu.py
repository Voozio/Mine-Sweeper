import pygame
import sys
import button

# Constants
BUTTON_W = 150
BUTTON_H = 50

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (150, 150, 150)
GREEN = (150, 225, 75)


class Menu:
    """
    A class to handle menu functionality.
    """
    def __init__(self):
        """
        Difficulty is initialized to None until a difficulty is chosen.
        """
        self.state = "main_menu"
        self.difficulty = None

        self.play_button = button.Button(0, 430, BUTTON_W, BUTTON_H, GREEN, "Play")
        self.rules_button = button.Button(0, 490, BUTTON_W, BUTTON_H, GREEN, "Rules")
        self.quit_button = button.Button(0, 550, BUTTON_W, BUTTON_H, GREEN, "Quit")
        self.easy_button = button.Button(0, 430, BUTTON_W, BUTTON_H, GREEN, "Easy")
        self.medium_button = button.Button(0, 490, BUTTON_W, BUTTON_H, GREEN, "Medium")
        self.hard_button = button.Button(0, 550, BUTTON_W, BUTTON_H, GREEN, "Hard")
        self.credits_button = button.Button(634, 550, BUTTON_W, BUTTON_H, GREEN, "Credits")
        self.back_button = button.Button(634, 550, BUTTON_W, BUTTON_H, GREEN, "Back")

    def get_menu_state(self):
        """
        Returns the current state of the menu.
        """
        return self.state

    def set_menu_state(self, state):
        """
        Sets the state of the menu.
        """
        self.state = state

    def get_difficulty(self):
        """
        Returns the chosen difficulty.
        """
        return self.difficulty

    def set_difficulty(self, difficulty):
        """
        Sets the difficulty.
        """
        self.difficulty = difficulty

    def check_click(self, pos):
        """
        Buttons are checked to see if they have been clicked.
        """
        if self.state == "main_menu":
            self.play_button.check_left_click(pos)
            self.rules_button.check_left_click(pos)
            self.credits_button.check_left_click(pos)
            self.quit_button.check_left_click(pos)
        elif self.state == "difficulty_menu":
            self.easy_button.check_left_click(pos)
            self.medium_button.check_left_click(pos)
            self.hard_button.check_left_click(pos)
            self.back_button.check_left_click(pos)

    def check_hover(self, mouse):
        """
        Buttons are checked to see if they are being hovered over.
        If so, the button color changes.
        """
        if self.state == "main_menu":
            self.play_button.check_hover(mouse)
            self.rules_button.check_hover(mouse)
            self.credits_button.check_hover(mouse)
            self.quit_button.check_hover(mouse)
        elif self.state == "difficulty_menu":
            self.easy_button.check_hover(mouse)
            self.medium_button.check_hover(mouse)
            self.hard_button.check_hover(mouse)
            self.back_button.check_hover(mouse)

    def no_click(self):
        """
        Sets l_click on each button to False.
        """
        self.play_button.l_click = False
        self.rules_button.l_click = False
        self.credits_button.l_click = False
        self.quit_button.l_click = False
        self.easy_button.l_click = False
        self.medium_button.l_click = False
        self.hard_button.l_click = False
        self.back_button.l_click = False

    def update(self):
        """
        The state changes depending on if a button has been clicked.
        """
        if self.state == "main_menu":
            if self.play_button.l_click:
                self.state = "difficulty_menu"
            elif self.rules_button.l_click:
                self.state = "rules_menu"
            elif self.credits_button.l_click:
                self.state = "credits_menu"
            elif self.quit_button.l_click:
                pygame.quit()
                sys.exit()
        elif self.state == "difficulty_menu":
            if self.easy_button.l_click:
                self.difficulty = "easy"
                self.state = "hidden"
            elif self.medium_button.l_click:
                self.difficulty = "medium"
                self.state = "hidden"
            elif self.hard_button.l_click:
                self.difficulty = "hard"
                self.state = "hidden"
            elif self.back_button.l_click:
                self.state = "main_menu"

    def draw(self, surface):
        """
        The menu is drawn depending on the state.
        """
        if self.state == "main_menu":
            self.play_button.draw(surface)
            self.rules_button.draw(surface)
            self.credits_button.draw(surface)
            self.quit_button.draw(surface)
        elif self.state == "difficulty_menu":
            self.easy_button.draw(surface)
            self.medium_button.draw(surface)
            self.hard_button.draw(surface)
            self.back_button.draw(surface)
        elif self.state == "rules_menu":
            self.draw_rules(surface)
        elif self.state == "credits_menu":
            self.draw_credits(surface)

    # noinspection PyMethodMayBeStatic
    def draw_rules(self, surface):
        """
        A function that is supposed to spell out the rules for the game.
        """
        font = pygame.font.SysFont("verdana", 30)
        width = 640
        height = 360
        surface_rect_x = surface.get_rect().centerx - (width/2)
        surface_rect_y = surface.get_rect().centery - (height/3)

        rect = pygame.Rect((surface_rect_x, surface_rect_y), (width, height))
        rect_border = pygame.Rect((surface_rect_x - 1, surface_rect_y - 1), (width + 2, height + 2))

        surface.fill(BLACK, rect_border)
        surface.fill(GREEN, rect)

    # noinspection PyMethodMayBeStatic
    def draw_credits(self, surface):
        """
        Code written by Voozio
        Icons made by UIJess
        """
        font = pygame.font.SysFont("verdana", 20)
        # bold = pygame.font.SysFont("verdana", 20, True)
        width = 640
        height = 360
        surface_rect_x = surface.get_rect().centerx - (width/2)
        surface_rect_y = surface.get_rect().centery - (height/3)

        rect = pygame.Rect((surface_rect_x, surface_rect_y), (width, height))
        rect_border = pygame.Rect((surface_rect_x - 1, surface_rect_y - 1), (width + 2, height + 2))

        created = "Created by Justin Voo"
        icons = "Sprites drawn by UIJess"
        updated = "Last Updated on March 31, 2020"

        text1 = font.render(created, True, BLACK)
        text1_rect = text1.get_rect()
        text1_rect.center = ((surface_rect_x + width/2), (surface_rect_y + height/4))

        text2 = font.render(icons, True, BLACK)
        text2_rect = text2.get_rect()
        text2_rect.center = ((surface_rect_x + width/2), (surface_rect_y + height*(1/2)))

        text3 = font.render(updated, True, BLACK)
        text3_rect = text3.get_rect()
        text3_rect.center = ((surface_rect_x + width/2), (surface_rect_y + height*(3/4)))

        surface.fill(BLACK, rect_border)
        surface.fill(GREEN, rect)
        surface.blit(text1, text1_rect)
        surface.blit(text2, text2_rect)
        surface.blit(text3, text3_rect)
