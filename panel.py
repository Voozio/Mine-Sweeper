import pygame

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (150, 150, 150)
IVORY = (255, 255, 240)
SKY_BLUE = (100, 215, 250)
DARK_BLUE = (0, 90, 125)
GREEN = (150, 225, 75)
LIGHT_RED = (255, 200, 200)

# Side Panel
SIDE_PANEL_X = 24
SIDE_PANEL_Y = 24

# Icons
FLAG_ICON = pygame.image.load("img/flags/red.png")

# High-Score List
scores = [line[:-1] for line in open("scoreboard.txt")]


class SidePanel:
    """
    A class to handle the side panel functionality.
    """

    def __init__(self):
        """
        A border is created for every rectangle separately.
        """
        self.panel_width = 112
        self.top_panel_height = 156
        self.bottom_panel_height = 288
        self.small_box_width = 90
        self.small_box_height = 60
        self.large_box_width = 88
        self.large_box_height = 264

        self.timer = None
        self.timer_bg = WHITE
        self.paused = False

        self.top_rect_border = pygame.Rect((SIDE_PANEL_X - 1, SIDE_PANEL_Y - 1),
                                           (self.panel_width + 2, self.top_panel_height + 2))
        self.top_rect = pygame.Rect((SIDE_PANEL_X, SIDE_PANEL_Y), (self.panel_width, self.top_panel_height))

        self.timer_border = pygame.Rect((SIDE_PANEL_X + 11, SIDE_PANEL_Y + 11),
                                        (self.small_box_width + 2, self.small_box_height + 2))
        self.timer_rect = pygame.Rect((SIDE_PANEL_X + 12, SIDE_PANEL_Y + 12),
                                      (self.small_box_width, self.small_box_height))
        self.timer_text, self.timer_text_rect = self.setup_font(self.timer,
                                                                SIDE_PANEL_X + 12,
                                                                SIDE_PANEL_Y + 12,
                                                                self.small_box_width, self.small_box_height, 1)

        self.flag_count_border = pygame.Rect((SIDE_PANEL_X + 11, SIDE_PANEL_Y + 83),
                                             (self.small_box_width + 2, self.small_box_height + 2))
        self.flag_count_rect = pygame.Rect((SIDE_PANEL_X + 12, SIDE_PANEL_Y + 84),
                                           (self.small_box_width, self.small_box_height))
        self.flag_count_text, self.flag_count_text_rect = self.setup_font(self.timer,
                                                                          SIDE_PANEL_X + 12,
                                                                          SIDE_PANEL_Y + 72,
                                                                          self.small_box_width,
                                                                          self.small_box_height, 2)

        self.bottom_rect_border = pygame.Rect((SIDE_PANEL_X - 1, SIDE_PANEL_Y + 311),
                                              (self.panel_width + 2, self.bottom_panel_height + 2))
        self.bottom_rect = pygame.Rect((SIDE_PANEL_X, SIDE_PANEL_Y + 312), (self.panel_width, self.bottom_panel_height))

        self.scoreboard_title, self.scoreboard_title_rect = self.setup_font("Scoreboard",
                                                                            SIDE_PANEL_X + 12,
                                                                            SIDE_PANEL_Y + 288,
                                                                            self.large_box_width,
                                                                            24, 1)
        self.scoreboard_border = pygame.Rect((SIDE_PANEL_X + 11, SIDE_PANEL_Y + 321),
                                             (self.large_box_width + 2, self.large_box_height + 2))
        self.scoreboard_rect = pygame.Rect((SIDE_PANEL_X + 12, SIDE_PANEL_Y + 322),
                                           (self.large_box_width, self.large_box_height))

    # noinspection PyMethodMayBeStatic
    def setup_font(self, msg, x_pos, y_pos, width, height, purpose):
        """
        A method to center the text.
        """
        font = pygame.font.SysFont("verdana", 18)
        text = font.render(msg, True, BLACK)
        text_rect = text.get_rect()
        if purpose == 1:
            text_rect.center = ((x_pos + width / 2), (y_pos + height / 2))
        elif purpose == 2:
            text_rect.center = ((x_pos + width * (2/3)), (y_pos + height * (2/3)))
        return text, text_rect

    def toggle_pause(self):
        """
        Pauses/unpauses the game.
        """
        self.paused = not self.paused

    def game_over(self, win):
        if win:
            self.timer_bg = GREEN
        elif not win:
            self.timer_bg = LIGHT_RED

    def reset(self):
        self.timer_bg = WHITE

    def update(self, time, flags_remaining):
        """
        Sets and formats the time.
        """
        if not self.paused:
            seconds = time // 1000

            self.timer = str(int(seconds // 60)) + ":" + str(int(seconds % 60)).zfill(2)
            self.timer_text, self.timer_text_rect = self.setup_font(self.timer,
                                                                    SIDE_PANEL_X + 12,
                                                                    SIDE_PANEL_Y + 12,
                                                                    self.small_box_width,
                                                                    self.small_box_height, 1)

            self.flag_count_text, self.flag_count_text_rect = self.setup_font(str(flags_remaining),
                                                                              SIDE_PANEL_X + 12,
                                                                              SIDE_PANEL_Y + 72,
                                                                              self.small_box_width,
                                                                              self.small_box_height, 2)

    def draw(self, surface):
        """
        A draw method for the game side panel.
        """
        # Upper Box Section
        surface.fill(BLACK, self.top_rect_border)
        surface.fill(DARK_BLUE, self.top_rect)

        surface.fill(BLACK, self.timer_border)
        surface.fill(self.timer_bg, self.timer_rect)
        surface.blit(self.timer_text, self.timer_text_rect)

        surface.fill(BLACK, self.flag_count_border)
        surface.fill(WHITE, self.flag_count_rect)
        surface.blit(self.flag_count_text, self.flag_count_text_rect)
        surface.blit(FLAG_ICON, (SIDE_PANEL_X + 24 + (self.small_box_width / 12),
                                 SIDE_PANEL_Y + 84 + (self.small_box_height / 4)))

        # Lower Box Section
        surface.fill(BLACK, self.bottom_rect_border)
        surface.fill(DARK_BLUE, self.bottom_rect)

        surface.blit(self.scoreboard_title, self.scoreboard_title_rect)
        surface.fill(BLACK, self.scoreboard_border)
        surface.fill(WHITE, self.scoreboard_rect)
