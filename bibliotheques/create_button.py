from bibliotheques.create_image import CreateImage
from bibliotheques.create_text import CreateText

class CreateButton:
    """Permet de créer un bouton en créant son fond et son texte"""

    def __init__(self, screen, path, image_size, btn_position, btn_margin, text, color, text_size, text_position, text_margin):
        """Définition des variables de l'objet"""
        self.bg_image = CreateImage(screen, path, image_size, 0, 20, btn_position, btn_margin)
        self.text = CreateText(self.bg_image.image, text, color, text_size, 0, text_position, text_margin, False, None)
        self.text.rect.x += self.bg_image.rect.x
        self.text.rect.y += self.bg_image.rect.y

        self.rect = self.bg_image.rect

    def blit(self, screen):
        """Permet d'afficher l'objet sur la fenêtre"""
        self.bg_image.blit(screen)
        self.text.blit(screen)