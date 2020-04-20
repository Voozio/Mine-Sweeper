import pygame

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (150, 150, 150)
LIGHT_GRAY = (175, 175, 175)
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
        self.box_width = 90
        self.small_box_height = 60
        self.large_box_height = 264

        self.raw_time = 0
        self.timer = None
        self.timer_bg = WHITE
        self.paused = False
        self.difficulty = None
        self.scores_updated = False

        self.top_rect_border = pygame.Rect((SIDE_PANEL_X - 1, SIDE_PANEL_Y - 1),
                                           (self.panel_width + 2, self.top_panel_height + 2))
        self.top_rect = pygame.Rect((SIDE_PANEL_X, SIDE_PANEL_Y), (self.panel_width, self.top_panel_height))

        self.timer_border = pygame.Rect((SIDE_PANEL_X + 11, SIDE_PANEL_Y + 11),
                                        (self.box_width + 2, self.small_box_height + 2))
        self.timer_rect = pygame.Rect((SIDE_PANEL_X + 12, SIDE_PANEL_Y + 12),
                                      (self.box_width, self.small_box_height))
        self.timer_text, self.timer_text_rect = self.setup_font(self.timer,
                                                                SIDE_PANEL_X + 12,
                                                                SIDE_PANEL_Y + 12,
                                                                self.box_width, self.small_box_height, 1)

        self.flag_count_border = pygame.Rect((SIDE_PANEL_X + 11, SIDE_PANEL_Y + 83),
                                             (self.box_width + 2, self.small_box_height + 2))
        self.flag_count_rect = pygame.Rect((SIDE_PANEL_X + 12, SIDE_PANEL_Y + 84),
                                           (self.box_width, self.small_box_height))
        self.flag_count_text, self.flag_count_text_rect = self.setup_font(self.timer,
                                                                          SIDE_PANEL_X + 12,
                                                                          SIDE_PANEL_Y + 72,
                                                                          self.box_width,
                                                                          self.small_box_height, 2)

        self.bottom_rect_border = pygame.Rect((SIDE_PANEL_X - 1, SIDE_PANEL_Y + 311),
                                              (self.panel_width + 2, self.bottom_panel_height + 2))
        self.bottom_rect = pygame.Rect((SIDE_PANEL_X, SIDE_PANEL_Y + 312), (self.panel_width, self.bottom_panel_height))

        self.scoreboard_title, self.scoreboard_title_rect = self.setup_font("Scoreboard",
                                                                            SIDE_PANEL_X + 12,
                                                                            SIDE_PANEL_Y + 288,
                                                                            self.box_width,
                                                                            24, 1)
        self.scoreboard_border = pygame.Rect((SIDE_PANEL_X + 11, SIDE_PANEL_Y + 321),
                                             (self.box_width + 2, self.large_box_height + 2))
        self.scoreboard_rect = pygame.Rect((SIDE_PANEL_X + 12, SIDE_PANEL_Y + 322),
                                           (self.box_width, self.large_box_height))
        self.scoreboard_lines = self.create_scoreboard_lines()

        self.scores = None
        self.score_names_text, self.score_times_text = None, None

    # noinspection PyMethodMayBeStatic
    def setup_font(self, msg, x_pos, y_pos, width, height, purpose, fontsize = 18, bold = False):
        """
        A method to center the text.
        """
        font = pygame.font.SysFont("verdana", fontsize, bold)
        text = font.render(msg, True, BLACK)
        text_rect = text.get_rect()
        if purpose == 1:
            text_rect.center = ((x_pos + width / 2), (y_pos + height / 2))
        elif purpose == 2:
            text_rect.center = ((x_pos + width * (2/3)), (y_pos + height * (2/3)))
        return text, text_rect

    def setup_font_scores(self):
        score_names = []
        score_times = []
        y_pos = SIDE_PANEL_Y + 324

        for i in range(5):
            if int(self.scores[i][1]) > 43200:
                break
            text, rect = self.setup_font(self.scores[i][0],
                                         SIDE_PANEL_X + 12,
                                         y_pos,
                                         self.box_width,
                                         24, 1, 18, True)
            name = [text, rect]
            score_names.append(name)
            y_pos += 53

        y_pos = SIDE_PANEL_Y + 345

        for j in range(5):
            if int(self.scores[j][1]) > 43200:
                break
            time = str(int(int(self.scores[j][1]) // 60)) + ":" + str(int(int(self.scores[j][1]) % 60)).zfill(2)
            text, rect = self.setup_font(time,
                                         SIDE_PANEL_X + 12,
                                         y_pos,
                                         self.box_width,
                                         24, 1, 16)
            time = [text, rect]
            score_times.append(time)
            y_pos += 53

        return score_names, score_times

    def create_scoreboard_lines(self):
        board_lines = []
        y_pos = SIDE_PANEL_Y + 374

        for i in range(4):
            board_lines.append(pygame.Rect((SIDE_PANEL_X + 12, y_pos), (self.box_width, 1)))
            y_pos += 53

        return board_lines

    def set_difficulty(self, difficulty):
        self.difficulty = difficulty
        self.retrieve_scores()
        self.score_names_text, self.score_times_text = self.setup_font_scores()

    # noinspection PyMethodMayBeStatic
    def retrieve_scores(self):
        scores = []
        for line in open(f"scoreboard_{self.difficulty}.txt"):
            line = line[:-1].split(" ")
            scores.append(line)
        self.scores = scores

    def update_scores(self, name):
        if not self.scores_updated:
            self.scores_updated = True
            new_scores = self.scores
            new_scores.append([name, self.raw_time])

            for i in range(len(new_scores)):
                temp = new_scores[i]
                num = i
                while num > 0 and int(new_scores[num][1]) < int(new_scores[num-1][1]):
                    new_scores[num] = new_scores[num-1]
                    num -= 1
                    new_scores[num] = temp

            new_scores.pop()
            self.scores = new_scores
            self.score_names_text, self.score_times_text = self.setup_font_scores()

            out = open(f"scoreboard_{self.difficulty}.txt", "w")
            for j in range(len(self.scores)):
                out.write(f"{self.scores[j][0]} {self.scores[j][1]}\n")
            out.close()

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
        self.scores_updated = False

    def update(self, time, flags_remaining):
        """
        Sets and formats the time.
        """
        if not self.paused:
            self.raw_time = seconds = time // 1000

            self.timer = str(int(seconds // 60)) + ":" + str(int(seconds % 60)).zfill(2)
            self.timer_text, self.timer_text_rect = self.setup_font(self.timer,
                                                                    SIDE_PANEL_X + 12,
                                                                    SIDE_PANEL_Y + 12,
                                                                    self.box_width,
                                                                    self.small_box_height, 1)

            self.flag_count_text, self.flag_count_text_rect = self.setup_font(str(flags_remaining),
                                                                              SIDE_PANEL_X + 12,
                                                                              SIDE_PANEL_Y + 72,
                                                                              self.box_width,
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
        surface.blit(FLAG_ICON, (SIDE_PANEL_X + 24 + (self.box_width / 12),
                                 SIDE_PANEL_Y + 84 + (self.small_box_height / 4)))

        # Middle Box Section

        # Lower Box Section
        surface.fill(BLACK, self.bottom_rect_border)
        surface.fill(DARK_BLUE, self.bottom_rect)

        surface.blit(self.scoreboard_title, self.scoreboard_title_rect)
        surface.fill(BLACK, self.scoreboard_border)
        surface.fill(WHITE, self.scoreboard_rect)

        for i in range(4):
            surface.fill(LIGHT_GRAY, self.scoreboard_lines[i])

        for j in range(len(self.scores)):
            if int(self.scores[j][1]) > 43200:
                break
            surface.blit(self.score_names_text[j][0], self.score_names_text[j][1])

        for k in range(len(self.scores)):
            if int(self.scores[k][1]) > 43200:
                break
            surface.blit(self.score_times_text[k][0], self.score_times_text[k][1])
