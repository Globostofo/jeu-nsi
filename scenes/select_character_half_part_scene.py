import pygame
from bibliotheques.create_image import CreateImage
from bibliotheques.create_text import CreateText
from bibliotheques.create_rect import CreateRect
from bibliotheques.input_manager import InputManager
from objets.inventory_cell import InventoryCell

class SelectCharacterHalfPartScene:
    """Objet permettant de gérer la demi-scène du choix des combattants"""

    def __init__(self, screen, parent, pos):
        """Constantes"""
        self.parent = parent

        self.pos = pos
        if self.pos == "left":
            self.center = "1quarter"
            self.margin = 115
            self.ok_btn_pos = -200
            self.set_clavier()
            self.key_down = pygame.K_s
            self.key_right = pygame.K_d
        elif self.pos == "right":
            self.margin = 755
            self.center = "3quarter"
            self.ok_btn_pos = 200
            self.key_up = pygame.K_i
            self.key_left = pygame.K_j
            self.key_down = pygame.K_k
            self.key_right = pygame.K_l

        self.text_skin1_info1 = "Odavaror Trollsbane"
        self.text_skin1_info2 = "le guerrier bûcheron"
        self.text_skin1_info3 = "- Boost d'attaque"
        self.text_skin1_info4 = "- Boost de défense"
        self.text_skin1_info5 = "- Boost de vie"

        self.text_skin2_info1 = "Mary Kinnard"
        self.text_skin2_info2 = "l'aventurière téméraire"
        self.text_skin2_info3 = "- Boost de vitesse"
        self.text_skin2_info4 = "- Boost d'esquive"
        self.text_skin2_info5 = "- Boost de hauteur de saut"

        self.text_skin3_info1 = "Dexton Kersting"
        self.text_skin3_info2 = "le savant fou"
        self.text_skin3_info3 = "- Boost de soin"
        self.text_skin3_info4 = "- Boost de coups critiques"
        self.text_skin3_info5 = "- Boost de force de frappe"

        """Variables"""
        self.selected = 1
        self.skin_selected = self.selected
        self.generate_new_selector(screen)
        self.refresh_skin_info(screen)

        """Création des images de la scène"""
        self.bg_pseudo = CreateImage(screen, "assets/gui/backgrounds_panels/bonus_0.png", (550, 120), 0, 100, (self.center, "top"), (0, 0))

        self.background_choose_skin = CreateImage(screen, "assets/gui/backgrounds_panels/bonus_3.png", (407, 155), 0, 100, (self.center, "top"), (0, 206))
        self.all_inventory_cells = pygame.sprite.Group()
        for i in range(1, 4):
            self.all_inventory_cells.add(InventoryCell(screen, self.center, i))
        self.skin_sprite1 = CreateImage(screen, "assets/players/1 Woodcutter/Woodcutter.png", (78, 96), 0, 100, (self.center, "top"), (-129, 227))
        self.skin_sprite2 = CreateImage(screen, "assets/players/2 GraveRobber/GraveRobber.png", (55, 96), 0, 100, (self.center, "top"), (0, 227))
        self.skin_sprite3 = CreateImage(screen, "assets/players/3 SteamMan/SteamMan.png", (53, 96), 0, 100, (self.center, "top"), (129, 227))

        self.background_skin_info = CreateImage(screen, "assets/gui/backgrounds_panels/description_area.png", (500, 250), 0, 100, (self.center, "top"), (0, 380))

        self.ok_button = CreateImage(screen, "assets/gui/buttons/btn_ok.png", (172, 70), 0, 100, ("center", "bottom"), (self.ok_btn_pos, 10))

        """Récupération des inputs du joueur"""
        self.input_manager = InputManager()

    def blit_part(self, screen):
        """Permet d'afficher les composants de la partie"""

        self.bg_pseudo.blit(screen)
        self.pseudo_text.blit(screen)

        self.background_choose_skin.blit(screen)
        for cell in self.all_inventory_cells:
            cell.sprite.blit(screen)
        self.skin_sprite1.blit(screen)
        self.skin_sprite2.blit(screen)
        self.skin_sprite3.blit(screen)

        self.background_skin_info.blit(screen)
        self.skin_text1.blit(screen)
        self.skin_text2.blit(screen)
        self.rect_text2.blit(screen)
        self.skin_text3.blit(screen)
        self.skin_text4.blit(screen)
        self.skin_text5.blit(screen)

        self.ok_button.blit(screen)
        self.selector.blit(screen)

    def set_clavier(self):
        """Permet de set les touches en fonction du clavier choisi"""

        if self.parent.parent.parent.clavier == "AZERTY":
            self.key_up = pygame.K_z
            self.key_left = pygame.K_q
        elif self.parent.parent.parent.clavier == "QWERTY":
            self.key_up = pygame.K_w
            self.key_left = pygame.K_a

    def event_analyse(self, screen, event, i):
        """Examine les inputs pour agir en conséquence"""

        if event[i][1] == self.key_up:
            if self.selected == 4:
                if self.parent.parent.parent.sounds:
                    self.parent.sound_move_cursor.play()
                self.parent.premier_tour = True
                self.selected = self.skin_selected
                self.generate_new_selector(screen)
        elif event[i][1] == self.key_left:
            if self.selected == 2 or self.selected == 3:
                if self.parent.parent.parent.sounds:
                    self.parent.sound_move_cursor.play()
                self.selected -= 1
                self.generate_new_selector(screen)
                self.skin_selected = self.selected
                self.refresh_skin_info(screen)
        elif event[i][1] == self.key_down:
            if self.selected != 4:
                if self.parent.parent.parent.sounds:
                    self.parent.sound_select_cursor.play()
                self.selected = 4
                self.generate_new_selector(screen)
        elif event[i][1] == self.key_right:
            if self.selected == 1 or self.selected == 2:
                if self.parent.parent.parent.sounds:
                    self.parent.sound_move_cursor.play()
                self.selected += 1
                self.generate_new_selector(screen)
                self.skin_selected = self.selected
                self.refresh_skin_info(screen)

    def generate_new_selector(self, screen):
        """Permet de générer un nouveau sélecteur selon les 4 presets existants"""

        if self.selected == 1:
            self.selector = CreateImage(screen, "assets/gui/icons/inventory_cell_selector.png", (136, 136), 0, 100, (self.center, "top"), (-130, 209))
        elif self.selected == 2:
            self.selector = CreateImage(screen, "assets/gui/icons/inventory_cell_selector.png", (136, 136), 0, 100, (self.center, "top"), (-0, 209))
        elif self.selected == 3:
            self.selector = CreateImage(screen, "assets/gui/icons/inventory_cell_selector.png", (136, 136), 0, 100, (self.center, "top"), (130, 209))
        elif self.selected == 4:
            self.selector = CreateImage(screen, "assets/gui/icons/inventory_cell_selector.png", (172, 69), 0, 100, ("center", "bottom"), (self.ok_btn_pos, 11))

    def refresh_skin_info(self, screen):
        """Met à jour la zone des informations relatives au skin sélectionné"""

        if self.skin_selected == 1:
            self.skin_text1 = CreateText(screen, self.text_skin1_info1, self.parent.parent.parent.colors["DARK_GOLD"], (len(self.text_skin1_info1) * 20, 40), 0, ("left", "top"), (self.margin - 5, 400), False, None)
            self.skin_text2 = CreateText(screen, self.text_skin1_info2, self.parent.parent.parent.colors["DARK_GOLD"], (len(self.text_skin1_info2) * 10, 20), 0, ("left", "top"), (self.margin, 440), False, None)
            self.rect_text2 = CreateRect(screen, self.parent.parent.parent.colors["DARK_GOLD"], (len(self.skin_text2.text) * 10, 2), ("left", "top"), (self.margin + 1, 460))
            self.skin_text3 = CreateText(screen, self.text_skin1_info3, self.parent.parent.parent.colors["WHITE"], (len(self.text_skin1_info3) * 15, 30), 0, ("left", "top"), (self.margin, 500), False, None)
            self.skin_text4 = CreateText(screen, self.text_skin1_info4, self.parent.parent.parent.colors["WHITE"], (len(self.text_skin1_info4) * 15, 30), 0, ("left", "top"), (self.margin, 540), False, None)
            self.skin_text5 = CreateText(screen, self.text_skin1_info5, self.parent.parent.parent.colors["WHITE"], (len(self.text_skin1_info5) * 15, 30), 0, ("left", "top"), (self.margin, 580), False, None)
        elif self.skin_selected == 2:
            self.skin_text1 = CreateText(screen, self.text_skin2_info1, self.parent.parent.parent.colors["DARK_GOLD"], (len(self.text_skin2_info1) * 20, 40), 0, ("left", "top"), (self.margin - 5, 400), False, None)
            self.skin_text2 = CreateText(screen, self.text_skin2_info2, self.parent.parent.parent.colors["DARK_GOLD"], (len(self.text_skin2_info2) * 10, 20), 0, ("left", "top"), (self.margin, 440), False, None)
            self.rect_text2 = CreateRect(screen, self.parent.parent.parent.colors["DARK_GOLD"], (len(self.skin_text2.text) * 10, 2), ("left", "top"), (self.margin + 1, 460))
            self.skin_text3 = CreateText(screen, self.text_skin2_info3, self.parent.parent.parent.colors["WHITE"], (len(self.text_skin2_info3) * 15, 30), 0, ("left", "top"), (self.margin, 500), False, None)
            self.skin_text4 = CreateText(screen, self.text_skin2_info4, self.parent.parent.parent.colors["WHITE"], (len(self.text_skin2_info4) * 15, 30), 0, ("left", "top"), (self.margin, 540), False, None)
            self.skin_text5 = CreateText(screen, self.text_skin2_info5, self.parent.parent.parent.colors["WHITE"], (len(self.text_skin2_info5) * 15, 30), 0, ("left", "top"), (self.margin, 580), False, None)
        elif self.skin_selected == 3:
            self.skin_text1 = CreateText(screen, self.text_skin3_info1, self.parent.parent.parent.colors["DARK_GOLD"], (len(self.text_skin3_info1) * 20, 40), 0, ("left", "top"), (self.margin - 5, 400), False, None)
            self.skin_text2 = CreateText(screen, self.text_skin3_info2, self.parent.parent.parent.colors["DARK_GOLD"], (len(self.text_skin3_info2) * 10, 20), 0, ("left", "top"), (self.margin, 440), False, None)
            self.rect_text2 = CreateRect(screen, self.parent.parent.parent.colors["DARK_GOLD"], (len(self.skin_text2.text) * 10, 2), ("left", "top"), (self.margin + 1, 460))
            self.skin_text3 = CreateText(screen, self.text_skin3_info3, self.parent.parent.parent.colors["WHITE"], (len(self.text_skin3_info3) * 15, 30), 0, ("left", "top"), (self.margin, 500), False, None)
            self.skin_text4 = CreateText(screen, self.text_skin3_info4, self.parent.parent.parent.colors["WHITE"], (len(self.text_skin3_info4) * 15, 30), 0, ("left", "top"), (self.margin, 540), False, None)
            self.skin_text5 = CreateText(screen, self.text_skin3_info5, self.parent.parent.parent.colors["WHITE"], (len(self.text_skin3_info5) * 15, 30), 0, ("left", "top"), (self.margin, 580), False, None)