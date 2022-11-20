import pygame
from bibliotheques.create_image import CreateImage

class InventoryCell(pygame.sprite.Sprite):
    """Objet qui gère les cellules d'inventaire"""

    def __init__(self, screen, pos, i):
        super().__init__()
        self.number = i
        self.is_selected = False

        if self.number == 1:
            pos_x = -129
            self.is_selected = True
        elif self.number == 2:
            pos_x = 0
        elif self.number == 3:
            pos_x = 129
        self.sprite = CreateImage(screen, "assets/gui/icons/inventory_cell.png", (128, 128), 0, 100, (pos, "top"), (pos_x, 213))