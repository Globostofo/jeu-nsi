import pygame

class CreateRect:
    """Permet de créer un rectangle comme pygame mais en plus cool pour gérer la position"""

    def __init__(self, screen, color, size, position, margin):
        """Définition des variables de l'objet"""
        self.color = color
        self.size = size
        self.position = position
        self.margin = margin

        self.set_rect(screen)

    def set_rect(self, screen):
        """Crée le rectangle de l'objet"""
        width = self.size[0]
        height = self.size[1]

        if self.position[0] == "left":
            x_pos = self.margin[0]
        elif self.position[0] == "1quarter":
            x_pos = round(screen.get_width() / 4 - width / 2) + self.margin[0]
        elif self.position[0] == "center":
            x_pos = round(screen.get_width() / 2 - width / 2) + self.margin[0]
        elif self.position[0] == "3quarter":
            x_pos = round(screen.get_width() * (3/4) - width / 2) + self.margin[0]
        elif self.position[0] == "right":
            x_pos = screen.get_width() - width - self.margin[0]
        else:
            x_pos = self.position[0] + self.margin[0]

        if self.position[1] == "top":
            y_pos = self.margin[1]
        elif self.position[1] == "center":
            y_pos = round(screen.get_height() / 2 - height / 2) - self.margin[1]
        elif self.position[1] == "bottom":
            y_pos = screen.get_height() - height - self.margin[1]
        else:
            y_pos = self.position[1] + self.margin[1]

        self.rect = pygame.Rect(x_pos, y_pos, width, height)

    def blit(self, screen):
        """Permet d'afficher l'objet sur la fenêtre"""
        pygame.draw.rect(screen, self.color, self.rect)