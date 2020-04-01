import pygame

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (150, 150, 150)
LIGHT_GRAY = (175, 175, 175)
GREEN = (150, 225, 75)
LIGHT_GREEN = (175, 240, 140)


class Button:
    """
    A class to handle button functionality.
    """
    def __init__(self, x, y, width, height, color, msg = None):
        """
        x and y are saved for easier recall.
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.msg = msg

        self.rect = pygame.Rect((x, y), (width, height))
        if msg is not None:
            self.text, self.text_rect = self.setup_font()
        if msg == "Play" or msg == "Rules" or msg == "Quit" or msg == "Easy" or msg == "Medium" or msg == "Hard":
            self.rect_border = pygame.Rect((x - 1, y - 1), (width + 1, height + 2))
        else:
            self.rect_border = pygame.Rect((x - 1, y - 1), (width + 2, height + 2))

        self.l_click = False
        self.visible = True
        self.flagged = False

    def setup_font(self):
        """
        A method to center the text and create a text label.
        """
        font = pygame.font.SysFont("verdana", 20)
        text = font.render(self.msg, True, BLACK)
        text_rect = text.get_rect()
        text_rect.center = ((self.x + self.width/2), (self.y + self.height/2))
        return text, text_rect

    def get_position(self):
        """
        Returns the x and y positions.
        """
        return [self.x, self.y]

    def set_position(self, pos):
        """
        Sets the x and y positions.
        """
        self.x = pos[0]
        self.y = pos[1]

    def get_flagged(self):
        """
        Returns the flagged boolean.
        """
        return self.flagged

    def set_flagged(self, flagged):
        """
        Sets the flagged boolean.
        """
        self.flagged = flagged

    def is_visible(self):
        """
        Returns the visible boolean.
        """
        return self.visible

    def check_hover(self, mouse):
        """
        If the mouse position falls within a button, the button color changes.
        """
        if self.x < mouse[0] < self.x + self.width and self.y < mouse[1] < self.y + self.height:
            self.color = LIGHT_GREEN
        else:
            self.color = GREEN

    def check_left_click(self, pos):
        """
        Returns true if the left mouse button has been clicked.
        """
        if self.rect.collidepoint(pos[0], pos[1]) and not self.flagged:
            self.l_click = True
            return True

    def check_right_click(self, pos):
        """
        Flips flagged if the right mouse button has been clicked.
        """
        if self.rect.collidepoint(pos[0], pos[1]):
            self.flagged = not self.flagged

    def draw(self, surface):
        """
        Blits the buttons.
        """
        if self.visible:
            surface.fill(BLACK, self.rect_border)
            surface.fill(self.color, self.rect)
            if self.msg is not None:
                surface.blit(self.text, self.text_rect)
