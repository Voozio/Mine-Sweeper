import pygame
import button
import random

# Game Panel
GAME_PANEL_X = 160
GAME_PANEL_Y = 24
GAME_PANEL_SIDE = 600

# Buttons
BUTTON_W = 24
BUTTON_H = 24
PAUSE_MENU_BUTTON_W = 150
PAUSE_MENU_BUTTON_H = 50

# Bomb Count
B_EASY = 10
B_MEDIUM = 40
B_HARD = 84

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (150, 150, 150)
LIGHT_GRAY = (175, 175, 175)
DARK_GRAY = (35, 35, 45)
IVORY = (255, 255, 240)
SKY_BLUE = (100, 215, 250)
GREEN = (150, 225, 75)

# Icons
BOMB_ICON = pygame.image.load("img/bombs/bomb24.png")
FLAG_ICON = pygame.image.load("img/flags/red.png")
ONE_ICON = pygame.image.load("img/numbers/1.png")
TWO_ICON = pygame.image.load("img/numbers/2.png")
THREE_ICON = pygame.image.load("img/numbers/3.png")
FOUR_ICON = pygame.image.load("img/numbers/4.png")
FIVE_ICON = pygame.image.load("img/numbers/5.png")
SIX_ICON = pygame.image.load("img/numbers/6.png")
SEVEN_ICON = pygame.image.load("img/numbers/7.png")
EIGHT_ICON = pygame.image.load("img/numbers/8_1.png")

EXPLOSION_LIST = [BOMB_ICON,
                  pygame.image.load("img/explosion/1.png"),
                  pygame.image.load("img/explosion/2.png"),
                  pygame.image.load("img/explosion/3.png"),
                  pygame.image.load("img/explosion/4.png"),
                  pygame.image.load("img/explosion/5.png"),
                  pygame.image.load("img/explosion/6.png"),
                  pygame.image.load("img/explosion/7.png"),
                  pygame.image.load("img/explosion/8.png"),
                  pygame.image.load("img/explosion/9.png")]


class Board:
    """
    A class to handle the board functionality.
    """
    def __init__(self, difficulty):
        """
        A button is created for each clickable space on the board and placed into a 2D array.
        Every time a button is clicked, last_row_col keeps track of which button that is.
        Once a bomb is clicked, an explosion_order list is created.
        This list holds lists of tuples for the order at which bombs explode.
        When the program registers that the game is over, last_row_col should be the location of a bomb.
        This location will be the center of an exploding ripple effect.
        To create the ripple, explosion_count starts at 0 and increments every cycle.
        explosion_count is the number up to and including which explosion_order list should be visible.
        explosion_num holds the counts for which explosion frame should be shown.
        explosion_num_count works like like explosion_count, increamenting up to and including those visible.
        """
        self.side = difficulty
        self.win = False
        self.game_over = False
        self.exploded = False
        self.explosion_order = []
        self.explosion_count = 0
        self.explosion_num = []
        self.explosion_num_count = 0
        self.total_mines = self.set_difficulty(difficulty)
        self.last_row_col = (0, 0)

        self.bomb_key = [[0 for _ in range(self.side)] for _ in range(self.side)]
        self.board_key = [[0 for _ in range(self.side)] for _ in range(self.side)]

        self.initialize_key()

        self.board_button = button.Button(0, 0, BUTTON_W, BUTTON_H, GREEN)
        self.board = [[self.board_button for _ in range(self.side)] for _ in range(self.side)]

        self.board_border, self.board_bg = self.initialize_board()
        self.board_bg_lines = self.create_board_lines()

        self.game_panel_border = pygame.Rect((GAME_PANEL_X - 1, GAME_PANEL_Y - 1),
                                             (GAME_PANEL_SIDE + 2, GAME_PANEL_SIDE + 2))
        self.game_panel_bg = pygame.Rect((GAME_PANEL_X, GAME_PANEL_Y), (GAME_PANEL_SIDE, GAME_PANEL_SIDE))

    # noinspection PyMethodMayBeStatic
    def set_difficulty(self, difficulty):
        """
        Returns the number of bombs based on the difficulty selected.
        """
        if difficulty == 9:
            return B_EASY
        elif difficulty == 16:
            return B_MEDIUM
        else:
            return B_HARD

    def check_hover(self, mouse):
        """
        If the mouse position falls within any tile, the tile color changes.
        """
        [[self.board[i][j].check_hover(mouse) for i in range(self.side)] for j in range(self.side)]

    def check_left_click(self, pos):
        """
        Tiles are checked to see if they have been clicked with the left mouse button.
        """
        for i in range(self.side):
            for j in range(self.side):
                if self.board[i][j].check_left_click(pos):
                    self.last_row_col = (i, j)

    def check_right_click(self, pos):
        """
        Tiles are checked to see if they have been clicked with the right mouse button.
        """
        for i in range(self.side):
            for j in range(self.side):
                if self.get_flags_remaining() != 0:
                    self.board[i][j].check_right_click(pos)
                elif self.board[i][j].get_flagged():
                    self.board[i][j].check_right_click(pos)

    def no_click(self):
        """
        Sets l_click on each tile to False.
        """
        for i in range(self.side):
            for j in range(self.side):
                self.board[i][j].l_click = False

    def determine_number_icon(self, grid_x, grid_y):
        """
        Return an icon based on the number in board_key.
        """
        if self.board_key[grid_x][grid_y] == 1:
            return ONE_ICON
        elif self.board_key[grid_x][grid_y] == 2:
            return TWO_ICON
        elif self.board_key[grid_x][grid_y] == 3:
            return THREE_ICON
        elif self.board_key[grid_x][grid_y] == 4:
            return FOUR_ICON
        elif self.board_key[grid_x][grid_y] == 5:
            return FIVE_ICON
        elif self.board_key[grid_x][grid_y] == 6:
            return SIX_ICON
        elif self.board_key[grid_x][grid_y] == 7:
            return SEVEN_ICON
        elif self.board_key[grid_x][grid_y] == 8:
            return EIGHT_ICON

    def initialize_board(self):
        """
        Initializes the board based on difficulty and returns board_border and board_bg based on the size.
        """
        if self.side == 9:
            x_pos = GAME_PANEL_X * 2.2
            y_pos = GAME_PANEL_Y * 9
        elif self.side == 16:
            x_pos = GAME_PANEL_X * 1.6
            y_pos = GAME_PANEL_Y * 4.5
        else:
            x_pos = GAME_PANEL_X * 1.15
            y_pos = GAME_PANEL_Y * 2

        temp_x = x_pos
        board_bg = pygame.Rect((x_pos, y_pos), ((self.side * 25) - 1, (self.side * 25) - 1))
        board_border = pygame.Rect((x_pos - 1, y_pos - 1), ((self.side * 25) + 1, (self.side * 25) + 1))

        for i in range(self.side):
            for j in range(self.side):
                self.board[i][j] = button.Button(temp_x, y_pos, BUTTON_W, BUTTON_H, GREEN)
                temp_x += 25
            y_pos += 25
            temp_x = x_pos

        return board_border, board_bg

    def initialize_key(self):
        """
        Initializes bomb_key and board_key.
        """
        self.bomb_key = [[0 for _ in range(self.side)] for _ in range(self.side)]
        mine_count = 0

        while mine_count < self.total_mines:
            rand_x = random.randint(0, self.side - 1)
            rand_y = random.randint(0, self.side - 1)

            if self.bomb_key[rand_x][rand_y] == 0:
                self.bomb_key[rand_x][rand_y] = -1
                mine_count += 1

        self.count_adjacent_spaces()

    def create_board_lines(self):
        """
        Board lines are drawn with the dimensions of (game board length - 2) by 1 pixel.
        Calculations are based on how large the game board is.
        """
        board_lines = [pygame.Rect((0, 0), (0, 0)) for _ in range((self.side * 2) - 2)]

        if self.side == 9:
            x_pos = GAME_PANEL_X * 2.2
            y_pos = GAME_PANEL_Y * 9
        elif self.side == 16:
            x_pos = GAME_PANEL_X * 1.6
            y_pos = GAME_PANEL_Y * 4.5
        else:
            x_pos = GAME_PANEL_X * 1.15
            y_pos = GAME_PANEL_Y * 2

        temp_x = x_pos + 24
        temp_y = y_pos + 24

        for i in range(self.side - 1):
            board_lines[i] = pygame.Rect((temp_x, y_pos), (1, (self.side * 25) - 1))
            temp_x += 25

        for i in range(self.side - 1, (self.side * 2) - 2):
            board_lines[i] = pygame.Rect((x_pos, temp_y), ((self.side * 25) - 1, 1))
            temp_y += 25

        return board_lines

    def count_adjacent_spaces(self):
        """
        Loops through each tile and counts the number of bombs adjacent to it.
        """
        for i in range(self.side):
            for j in range(self.side):
                if self.bomb_key[i][j] != 1:
                    if j != self.side - 1:
                        if self.bomb_key[i][j + 1] == -1:
                            self.board_key[i][j] += 1
                    if i != self.side - 1 and j != self.side - 1:
                        if self.bomb_key[i + 1][j + 1] == -1:
                            self.board_key[i][j] += 1
                    if i != self.side - 1:
                        if self.bomb_key[i + 1][j] == -1:
                            self.board_key[i][j] += 1
                    if i != self.side - 1 and j != 0:
                        if self.bomb_key[i + 1][j - 1] == -1:
                            self.board_key[i][j] += 1
                    if j != 0:
                        if self.bomb_key[i][j - 1] == -1:
                            self.board_key[i][j] += 1
                    if i != 0 and j != 0:
                        if self.bomb_key[i - 1][j - 1] == -1:
                            self.board_key[i][j] += 1
                    if i != 0:
                        if self.bomb_key[i - 1][j] == -1:
                            self.board_key[i][j] += 1
                    if i != 0 and j != self.side - 1:
                        if self.bomb_key[i - 1][j + 1] == -1:
                            self.board_key[i][j] += 1
                else:
                    self.board_key[i][j] = -1

    def ripple(self, visited, grid_x, grid_y):
        """
        When a tile with no adjacent bombs is selected and made visible,
        all tiles connected to it that also have no adjacent bombs will also be made visible.
        """
        self.board[grid_x][grid_y].visible = False
        self.board[grid_x][grid_y].set_flagged(False)

        if self.no_bombs_adjacent(grid_x, grid_y):
            visited[grid_x][grid_y] = True

            if grid_y != self.side - 1:
                if visited[grid_x][grid_y + 1] is not True:
                    self.ripple(visited, grid_x, grid_y + 1)
            if grid_x != self.side - 1 and grid_y != self.side - 1:
                if visited[grid_x + 1][grid_y + 1] is not True:
                    self.ripple(visited, grid_x + 1, grid_y + 1)
            if grid_x != self.side - 1:
                if visited[grid_x + 1][grid_y] is not True:
                    self.ripple(visited, grid_x + 1, grid_y)
            if grid_x != self.side - 1 and grid_y != 0:
                if visited[grid_x + 1][grid_y - 1] is not True:
                    self.ripple(visited, grid_x + 1, grid_y - 1)
            if grid_y != 0:
                if visited[grid_x][grid_y - 1] is not True:
                    self.ripple(visited, grid_x, grid_y - 1)
            if grid_x != 0 and grid_y != 0:
                if visited[grid_x - 1][grid_y - 1] is not True:
                    self.ripple(visited, grid_x - 1, grid_y - 1)
            if grid_x != 0:
                if visited[grid_x - 1][grid_y] is not True:
                    self.ripple(visited, grid_x - 1, grid_y)
            if grid_x != 0 and grid_y != self.side - 1:
                if visited[grid_x - 1][grid_y + 1] is not True:
                    self.ripple(visited, grid_x - 1, grid_y + 1)

    def no_bombs_adjacent(self, grid_x, grid_y):
        """
        Returns True if there are no bombs adjacent to the given grid position. False, otherwise.
        """
        safe = True

        if grid_y != self.side - 1:
            if self.bomb_key[grid_x][grid_y + 1] == -1:
                safe = False
        if grid_x != self.side - 1 and grid_y != self.side - 1:
            if self.bomb_key[grid_x + 1][grid_y + 1] == -1:
                safe = False
        if grid_x != self.side - 1:
            if self.bomb_key[grid_x + 1][grid_y] == -1:
                safe = False
        if grid_x != self.side - 1 and grid_y != 0:
            if self.bomb_key[grid_x + 1][grid_y - 1] == -1:
                safe = False
        if grid_y != 0:
            if self.bomb_key[grid_x][grid_y - 1] == -1:
                safe = False
        if grid_x != 0 and grid_y != 0:
            if self.bomb_key[grid_x - 1][grid_y - 1] == -1:
                safe = False
        if grid_x != 0:
            if self.bomb_key[grid_x - 1][grid_y] == -1:
                safe = False
        if grid_x != 0 and grid_y != self.side - 1:
            if self.bomb_key[grid_x - 1][grid_y + 1] == -1:
                safe = False

        return safe

    def get_flags_remaining(self):
        """
        Returns the number of flags remaining based on the total number of bombs in the game and how many tiles are
        flagged in the Button class.
        """
        if self.side == 9:
            total_flags = 10
        elif self.side == 16:
            total_flags = 40
        else:
            total_flags = 84

        for i in range(self.side):
            for j in range(self.side):
                if self.board[i][j].get_flagged():
                    total_flags -= 1

        return total_flags

    def is_game_over(self):
        """
        Returns the game_over boolean.
        """
        return self.game_over

    def get_win(self):
        """
        Returns the win boolean.
        """
        return self.win

    def game_over_safe(self):
        """
        When the game is over and won, all remaining bombs are made visible.
        """
        if not self.exploded:
            self.exploded = True
            pygame.time.delay(1000)
            for i in range(self.side):
                for j in range(self.side):
                    if self.bomb_key[i][j] == -1:
                        self.board[i][j].visible = False
            pygame.time.delay(1000)

    def game_over_explosion(self):
        """
        When the game is over and lost, all bombs are set to -2 in the bomb key to signal an explosion.
        """
        if not self.exploded:
            self.exploded = True
            self.get_explosion_order()
            pygame.time.delay(1000)
        elif self.exploded:
            if self.explosion_count < len(self.explosion_order):
                for (i, j) in self.explosion_order[self.explosion_count]:
                    self.board[i][j].visible = False
                    self.bomb_key[i][j] = -2
                self.explosion_count += 1
                pygame.time.delay(10)

    def get_explosion_order(self):
        """
        Determines the order in which the bombs should explode, creating a ripple effect.
        bombs_left is initialized to the bomb count minus one to account for the bomb clicked.
        """
        explosion_order = [[self.last_row_col]]
        top = self.last_row_col[0] - 1
        bot = self.last_row_col[0] + 1
        left = self.last_row_col[1] - 1
        right = self.last_row_col[1] + 1

        if self.side == 9:
            bombs_left = 9
        elif self.side == 16:
            bombs_left = 39
        else:
            bombs_left = 83

        while bombs_left > 0:
            bombs = []
            if top >= 0:
                for side in range(self.side):
                    if left <= side <= right:
                        if self.bomb_key[top][side] == -1 and (top, side) not in bombs:
                            bombs.append((top, side))
                            bombs_left -= 1
            if bot < self.side:
                for side in range(self.side):
                    if left <= side <= right:
                        if self.bomb_key[bot][side] == -1 and (bot, side) not in bombs:
                            bombs.append((bot, side))
                            bombs_left -= 1
            if left >= 0:
                for side in range(self.side):
                    if top <= side <= bot:
                        if self.bomb_key[side][left] == -1 and (side, left) not in bombs:
                            bombs.append((side, left))
                            bombs_left -= 1
            if right < self.side:
                for side in range(self.side):
                    if top <= side <= bot:
                        if self.bomb_key[side][right] == -1 and (side, right) not in bombs:
                            bombs.append((side, right))
                            bombs_left -= 1

            if len(bombs) != 0:
                explosion_order.append(bombs)
            top -= 1
            bot += 1
            left -= 1
            right += 1

        self.explosion_order = explosion_order
        self.explosion_num = [0 for _ in range(len(self.explosion_order))]

    def get_exploded(self):
        return self.exploded

    def next_explosion(self):
        """
        This function increments the explosion frame for each slice of explosion_order every tick.
        """
        pygame.time.delay(90)
        for i in range(self.explosion_num_count):
            if self.explosion_num[i] < 9:
                self.explosion_num[i] += 1
        if self.explosion_num_count < len(self.explosion_order):
            self.explosion_num_count += 1

    def set_name_prompt_visibility(self, flag):
        self.show_name_prompt = flag

    def reset(self):
        """
        Resets the game board without creating a new one.
        """
        self.win = False
        self.game_over = False
        self.exploded = False
        self.explosion_order = []
        self.explosion_count = 0
        self.explosion_num = []
        self.explosion_num_count = 0

        self.bomb_key = [[0 for _ in range(self.side)] for _ in range(self.side)]
        self.board_key = [[0 for _ in range(self.side)] for _ in range(self.side)]

        self.initialize_key()

        self.board = [[self.board_button for _ in range(self.side)] for _ in range(self.side)]
        self.board_border, self.board_bg = self.initialize_board()

    def update(self):
        """
        If a left-clicked tile is a bomb, end the game.
        Else if a left-clicked tile is has no adjacent bombs, ripple through all connected empty spaces.
        Else display the number .
        """
        for i in range(self.side):
            for j in range(self.side):
                if self.board[i][j].l_click:
                    self.board[i][j].visible = False
                    if self.bomb_key[i][j]:
                        self.game_over = True
                    elif self.board_key[i][j] == 0:
                        visited = [[False for _ in range(self.side)] for _ in range(self.side)]
                        self.ripple(visited, i, j)

        tile_count = 0

        for i in range(self.side):
            for j in range(self.side):
                if self.board[i][j].visible:
                    tile_count += 1

        if self.get_flags_remaining() == 0:
            if self.side == 9 and tile_count == B_EASY:
                self.game_over = True
                self.win = True
            elif self.side == 16 and tile_count == B_MEDIUM:
                self.game_over = True
                self.win = True
            elif self.side == 22 and tile_count == B_HARD:
                self.game_over = True
                self.win = True

    def draw(self, surface, name):
        """
        The following is the order of items drawn:

        Game panel/border
        Board border/background
        Tiles/Flagged Tiles/Numbers/Bombs
        """
        surface.fill(BLACK, self.game_panel_border)
        surface.fill(SKY_BLUE, self.game_panel_bg)
        surface.fill(BLACK, self.board_border)
        surface.fill(WHITE, self.board_bg)

        for i in range((self.side * 2) - 2):
            surface.fill(LIGHT_GRAY, self.board_bg_lines[i])

        for i in range(self.side):
            for j in range(self.side):
                if self.board[i][j].is_visible():
                    self.board[i][j].draw(surface)
                    if self.board[i][j].get_flagged():
                        surface.blit(FLAG_ICON, self.board[i][j].get_position())
                elif self.bomb_key[i][j] == -1:
                    surface.blit(BOMB_ICON, self.board[i][j].get_position())
                elif self.bomb_key[i][j] == -2:
                    """
                    First implementation shows all bombs, and then explodes them at the same time.
                    Second implementation explodes all bombs in a ripple effect starting from the clicked bomb.
                    """
                    # for x in range(len(self.explosion_order)):
                    #     surface.blit(EXPLOSION_LIST[self.explosion_num[x]], self.board[i][j].get_position())
                    # print(self.explosion_num)

                    for k in range(len(self.explosion_order)):
                        for (x, y) in self.explosion_order[k]:
                            if x == i and y == j:
                                surface.blit(EXPLOSION_LIST[self.explosion_num[k]], self.board[i][j].get_position())
                elif self.board_key[i][j] != 0:
                    surface.blit(self.determine_number_icon(i, j), self.board[i][j].get_position())


class PauseMenu:
    """
    A class to handle the pause menu functionality.
    """
    def __init__(self):
        self.visible = False

        self.game_panel_border = pygame.Rect((GAME_PANEL_X - 1, GAME_PANEL_Y - 1),
                                             (GAME_PANEL_SIDE + 2, GAME_PANEL_SIDE + 2))
        self.menu_rect = pygame.Rect((GAME_PANEL_X, GAME_PANEL_Y), (GAME_PANEL_SIDE, GAME_PANEL_SIDE))

        self.resume_button = button.Button(self.menu_rect.centerx - (PAUSE_MENU_BUTTON_W / 2),
                                           self.menu_rect.centery * (1/4),
                                           PAUSE_MENU_BUTTON_W, PAUSE_MENU_BUTTON_H, GREEN, "Resume")

        self.replay_button = button.Button(self.menu_rect.centerx - (PAUSE_MENU_BUTTON_W / 2),
                                           self.menu_rect.centery * (2/4),
                                           PAUSE_MENU_BUTTON_W, PAUSE_MENU_BUTTON_H, GREEN, "Replay")

        self.main_menu_button = button.Button(self.menu_rect.centerx - (PAUSE_MENU_BUTTON_W / 2),
                                              self.menu_rect.centery * (3/4),
                                              PAUSE_MENU_BUTTON_W, PAUSE_MENU_BUTTON_H, GREEN, "Main Menu")

    def get_visible(self):
        return self.visible

    def toggle_visible(self):
        self.visible = not self.visible

    def check_hover(self, mouse):
        """
        If the mouse position falls within any tile, the tile color changes.
        """
        self.resume_button.check_hover(mouse)
        self.replay_button.check_hover(mouse)
        self.main_menu_button.check_hover(mouse)

    def check_left_click(self, pos):
        """
        Buttons are checked to see if they have been clicked.
        """
        self.resume_button.check_left_click(pos)
        self.replay_button.check_left_click(pos)
        self.main_menu_button.check_left_click(pos)

    def no_click(self):
        """
        Sets l_click on each button to False.
        """
        self.resume_button.l_click = False
        self.replay_button.l_click = False
        self.main_menu_button.l_click = False

    def update(self):
        """
        Returns true if the resume button has been clicked. Otherwise, false.
        """
        if self.resume_button.l_click:
            return 0
        elif self.replay_button.l_click:
            return 1
        elif self.main_menu_button.l_click:
            return 2
        else:
            return -1

    def draw(self, surface):
        """
        The pause menu is drawn to cover the game board.
        """
        surface.fill(BLACK, self.game_panel_border)
        surface.fill(SKY_BLUE, self.menu_rect)
        self.resume_button.draw(surface)
        self.replay_button.draw(surface)
        self.main_menu_button.draw(surface)
