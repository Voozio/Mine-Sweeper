import pygame

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (150, 150, 150)

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
        self.top_panel_height = 168
        self.bottom_panel_height = 288
        self.small_box_width = 66
        self.small_box_height = 48
        self.large_box_width = 88
        self.large_box_height = 264

        self.timer = None
        self.paused = False

        self.top_rect_border = pygame.Rect((SIDE_PANEL_X - 1, SIDE_PANEL_Y - 1),
                                           (self.panel_width + 2, self.top_panel_height + 2))
        self.top_rect = pygame.Rect((SIDE_PANEL_X, SIDE_PANEL_Y), (self.panel_width, self.top_panel_height))

        self.timer_border = pygame.Rect((SIDE_PANEL_X + 23, SIDE_PANEL_Y + 23),
                                        (self.small_box_width + 2, self.small_box_height + 2))
        self.timer_rect = pygame.Rect((SIDE_PANEL_X + 24, SIDE_PANEL_Y + 24),
                                      (self.small_box_width, self.small_box_height))
        self.timer_text, self.timer_text_rect = self.setup_font(self.timer,
                                                                SIDE_PANEL_X + 24,
                                                                SIDE_PANEL_Y + 24,
                                                                self.small_box_width, self.small_box_height, 1)

        self.flag_count_border = pygame.Rect((SIDE_PANEL_X + 23, SIDE_PANEL_Y + 95),
                                             (self.small_box_width + 2, self.small_box_height + 2))
        self.flag_count_rect = pygame.Rect((SIDE_PANEL_X + 24, SIDE_PANEL_Y + 96),
                                           (self.small_box_width, self.small_box_height))
        self.flag_count_text, self.flag_count_text_rect = self.setup_font(self.timer,
                                                                          SIDE_PANEL_X + 24,
                                                                          SIDE_PANEL_Y + 96,
                                                                          self.small_box_width,
                                                                          self.small_box_height, 2)

        self.bottom_rect_border = pygame.Rect((SIDE_PANEL_X - 1, SIDE_PANEL_Y + 191),
                                              (self.panel_width + 2, self.bottom_panel_height + 2))
        self.bottom_rect = pygame.Rect((SIDE_PANEL_X, SIDE_PANEL_Y + 192), (self.panel_width, self.bottom_panel_height))

        self.scoreboard_border = pygame.Rect((SIDE_PANEL_X + 11, SIDE_PANEL_Y + 201),
                                             (self.large_box_width + 2, self.large_box_height + 2))
        self.scoreboard_rect = pygame.Rect((SIDE_PANEL_X + 12, SIDE_PANEL_Y + 202),
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
            text_rect.center = ((x_pos + width * (2/3)), (y_pos + height / 2))
        return text, text_rect

    def toggle_pause(self):
        """
        Pauses/unpauses the game.
        """
        self.paused = not self.paused

    def update(self, time, flags_remaining):
        """
        Sets and formats the time.
        """
        if not self.paused:
            seconds = time // 1000

            self.timer = str(int(seconds // 60)) + ":" + str(int(seconds % 60)).zfill(2)
            self.timer_text, self.timer_text_rect = self.setup_font(self.timer,
                                                                    SIDE_PANEL_X + 24,
                                                                    SIDE_PANEL_Y + 24,
                                                                    self.small_box_width,
                                                                    self.small_box_height, 1)

            self.flag_count_text, self.flag_count_text_rect = self.setup_font(str(flags_remaining),
                                                                              SIDE_PANEL_X + 24,
                                                                              SIDE_PANEL_Y + 96,
                                                                              self.small_box_width,
                                                                              self.small_box_height, 2)

    def draw(self, surface):
        """
        A draw method for the game side panel.
        """
        # Upper Box Section
        surface.fill(BLACK, self.top_rect_border)
        surface.fill(GRAY, self.top_rect)

        surface.fill(BLACK, self.timer_border)
        surface.fill(WHITE, self.timer_rect)
        surface.blit(self.timer_text, self.timer_text_rect)

        surface.fill(BLACK, self.flag_count_border)
        surface.fill(WHITE, self.flag_count_rect)
        surface.blit(self.flag_count_text, self.flag_count_text_rect)
        surface.blit(FLAG_ICON, (SIDE_PANEL_X + 24 + (self.small_box_width / 10),
                                 SIDE_PANEL_Y + 96 + (self.small_box_height / 4)))

        # Lower Box Section
        surface.fill(BLACK, self.bottom_rect_border)
        surface.fill(GRAY, self.bottom_rect)

        surface.fill(BLACK, self.scoreboard_border)
        surface.fill(WHITE, self.scoreboard_rect)
