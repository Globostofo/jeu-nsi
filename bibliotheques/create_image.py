import pygame

class CreateImage:
    """Permet de créer une image à l'aide de pygame"""

    def __init__(self, screen, path, size, rotation, opacity, position, margin):
        """Définition des variables de l'objet"""
        self.path = path
        self.size = size
        self.rotation = rotation
        self.opacity = opacity
        self.position = position
        self.margin = margin

        """Création de l'objet"""
        self.set_image()
        self.set_size()
        self.set_rotation()
        self.set_opacity()
        self.get_rect()
        self.set_position(screen)

    def set_image(self):
        """Crée l'image en fonction du chemin"""
        self.image = pygame.image.load(self.path)

    def set_size(self):
        """Modifie la taille de l'image"""
        self.image = pygame.transform.scale(self.image, self.size)

    def set_rotation(self):
        """Modifie la rotation de l'image"""
        self.image = pygame.transform.rotate(self.image, self.rotation)

    def set_opacity(self):
        """Modifie l'opacité de l'image"""
        self.image.set_alpha((self.opacity / 100) * 255)

    def get_rect(self):
        """Récupère le rectangle de l'image"""
        self.rect = self.image.get_rect()

    def set_position(self, screen):
        """Positionne l'image sur la fenêtre"""
        if self.position[0] == "left":
            self.rect.x = self.margin[0]
        elif self.position[0] == "1quarter":
            self.rect.x = round(screen.get_width() / 4 - self.image.get_width() / 2) + self.margin[0]
        elif self.position[0] == "center":
            self.rect.x = round(screen.get_width() / 2 - self.image.get_width() / 2) + self.margin[0]
        elif self.position[0] == "3quarter":
            self.rect.x = round(screen.get_width() * (3/4) - self.image.get_width() / 2) + self.margin[0]
        elif self.position[0] == "right":
            self.rect.x = screen.get_width() - self.image.get_width() - self.margin[0]
        else:
            self.rect.x = self.position[0] + self.margin[0]

        if self.position[1] == "top":
            self.rect.y = self.margin[1]
        elif self.position[1] == "center":
            self.rect.y = round(screen.get_height() / 2 - self.image.get_height() / 2) - self.margin[1]
        elif self.position[1] == "bottom":
            self.rect.y = screen.get_height() - self.image.get_height() - self.margin[1]
        else:
            self.rect.y = self.position[1] + self.margin[1]

    def flip_image(self, h, v):
        """Permet de retourner horizontalement ou verticalement l'image"""
        image_temp = pygame.image.load(self.path)
        self.image = pygame.transform.flip(image_temp, h, v)
        self.set_size()

    def blit(self, screen):
        """Permet d'afficher l'objet sur la fenêtre"""
        screen.blit(self.image, self.rect)