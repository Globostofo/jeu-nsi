import pygame

class CreateText:
    """Permet de créer un texte à l'aide de pygame"""

    def __init__(self, surface, text, color, size, rotation, position, margin, contours, contour_color):
        """Définition des variables de l'objet"""
        self.font = pygame.font.Font("assets/font.otf", 48)
        self.render = ''
        self.surface = surface
        self.text = text
        self.color = color
        self.size = size
        self.rotation = rotation
        self.position = position
        self.margin = margin
        self.contours = []

        """Création de l'objet"""
        self.set_text()
        self.set_size()
        self.set_rotation()
        self.get_rect()
        self.set_position()
        if contours:
            self.set_contours(surface, contour_color)

    def set_text(self):
        """Crée le texte avec la police d'écriture et la couleur demandée"""
        self.render = self.font.render(self.text, 1, self.color)

    def set_size(self):
        """Modifie la taille du texte"""
        self.render = pygame.transform.scale(self.render, self.size)

    def set_rotation(self):
        """Modifie la rotation du texte"""
        self.render = pygame.transform.rotate(self.render, self.rotation)

    def get_rect(self):
        """Récupère le rectangle du texte"""
        self.rect = self.render.get_rect()

    def set_position(self):
        """Positionne le texte sur la fenêtre"""

        if self.position[0] == "left":
            self.rect.x = self.margin[0]
        elif self.position[0] == "1quarter":
            self.rect.x = round(self.surface.get_width() / 4 - self.render.get_width() / 2) + self.margin[0]
        elif self.position[0] == "center":
            self.rect.x = round(self.surface.get_width() / 2 - self.render.get_width() / 2) + self.margin[0]
        elif self.position[0] == "3quarter":
            self.rect.x = round(self.surface.get_width() * (3/4) - self.render.get_width() / 2) + self.margin[0]
        elif self.position[0] == "right":
            self.rect.x = self.surface.get_width() - self.render.get_width() - self.margin[0]
        else:
            self.rect.x = self.position[0] + self.margin[0]

        if self.position[1] == "top":
            self.rect.y = self.margin[1]
        elif self.position[1] == "center":
            self.rect.y = round(self.surface.get_height() / 2 - self.render.get_height() / 2) - self.margin[1]
        elif self.position[1] == "bottom":
            self.rect.y = self.surface.get_height() - self.render.get_height() - self.margin[1]
        else:
            self.rect.y = self.position[1] + self.margin[1]

        for i in range(0, len(self.contours)):
            self.contours[i].position = self.position
            self.contours[i].set_position()

    def set_contours(self, surface, color):
        self.contours = []
        for i in range(-1, 2, 2):
            for j in range(-1, 2, 2):
                self.contours.append(CreateText(surface, self.text, color, self.size, self.rotation, self.position, (self.margin[0] + i * 2, self.margin[1] + j * 2), False, None))

    def blit(self, screen):
        """Permet d'afficher l'objet sur la fenêtre"""
        for i in range(0, len(self.contours)):
            self.contours[i].blit(screen)
        screen.blit(self.render, self.rect)