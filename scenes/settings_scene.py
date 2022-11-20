import pygame
from bibliotheques.create_image import CreateImage
from bibliotheques.create_text import CreateText
from bibliotheques.input_manager import InputManager

class SettingsScene:
    """Objet permettant de gérer la scène des paramètres"""

    def __init__(self, screen, parent):
        """Variables"""
        self.blit = False
        self.parent = parent
        self.refresh_settings(screen)
        self.active1 = False
        self.active2 = False

        """Création des images de la scène"""
        self.black_background = pygame.Rect(0, 0, screen.get_width(), screen.get_height())
        self.background = CreateImage(screen, "assets/gui/backgrounds_panels/bg.png", (screen.get_width(), screen.get_height()), 0, 60, ("left", "top"), (0, 0))
        self.settings_background = CreateImage(screen, "assets/gui/backgrounds_panels/setting_panel.png", (444, 693), 0, 100, ("center", "center"), (0, 0))
        self.settings_text = CreateText(screen, "SETTINGS", self.parent.colors["DARK_GOLD"], (300, 65), 0, ("center", "top"), (0, 47), False, None)

        self.bg_set_pseudo1 = CreateImage(screen, "assets/gui/backgrounds_panels/description_area.png", (400, 50), 0, 100, ("center", "top"), (0, 130))
        self.pseudo1_change_text = CreateText(screen, "Pseudo du joueur 1", self.parent.colors["DARK_GOLD"], (18 * 15, 30), 0, ("center", "top"), (0, 145), False, None)
        self.input_Rect1 = pygame.Rect(460, 192, 360, 40)
        self.pseudo_player1 = CreateText(screen, self.parent.pseudo1, self.parent.colors["WHITE"], (len(self.parent.pseudo1) * 20, 30), 0, ("center", "top"), (2, 200), False, None)

        self.bg_set_pseudo2 = CreateImage(screen, "assets/gui/backgrounds_panels/description_area.png", (400, 50), 0, 100, ("center", "top"), (0, 245))
        self.pseudo2_change_text = CreateText(screen, "Pseudo du joueur 2", self.parent.colors["DARK_GOLD"], (18 * 15, 30), 0, ("center", "top"), (0, 260), False, None)
        self.input_Rect2 = pygame.Rect(460, 307, 360, 40)
        self.pseudo_player2 = CreateText(screen, self.parent.pseudo2, self.parent.colors["WHITE"], (len(self.parent.pseudo2) * 20, 30), 0, ("center", "top"), (2, 315), False, None)

        self.bg_set_clavier = CreateImage(screen, "assets/gui/backgrounds_panels/description_area.png", (400, 50), 0, 100, ("center", "top"), (0, 360))
        self.text_clavier = CreateText(screen, "Clavier", self.parent.colors["DARK_GOLD"], (7 * 15, 30), 0, ("center", "top"), (0, 375), False, None)
        self.text_azerty = CreateText(screen, "AZERTY", self.parent.colors["WHITE"], (130, 30), 0, ("center", "top"), (-95, 430), False, None)
        self.rect_azerty = pygame.Rect(470, 423, 150, 40)
        self.text_qwerty = CreateText(screen, "QWERTY", self.parent.colors["WHITE"], (130, 30), 0, ("center", "top"), (95, 430), False, None)
        self.rect_qwerty = pygame.Rect(660, 423, 150, 40)

        self.bg_set_show_fps = CreateImage(screen, "assets/gui/backgrounds_panels/description_area.png", (400, 50), 0, 100, ("center", "top"), (0, 475))
        self.text_show_fps = CreateText(screen, "Montrer les fps", self.parent.colors["DARK_GOLD"], (15 * 15, 30), 0, ("left", "top"), (480, 490), False, None)
        self.check_box_bg_show_fps = CreateImage(screen, "assets/gui/icons/checkbox_bg.png", (16, 16), 0, 100, ("center", "top"), (150, 495))
        self.mark_show_fps = CreateImage(screen, "assets/gui/icons/mark_icon.png", (16, 16), 0, 100, ("center", "top"), (150, 495))

        self.bg_set_sound = CreateImage(screen, "assets/gui/backgrounds_panels/description_area.png", (400, 50), 0, 100, ("center", "top"), (0, 545))
        self.text_sound = CreateText(screen, "Sons", self.parent.colors["DARK_GOLD"], (4 * 15, 30), 0, ("left", "top"), (480, 560), False, None)
        self.check_box_bg_sound= CreateImage(screen, "assets/gui/icons/checkbox_bg.png", (16, 16), 0, 100, ("center", "top"), (150, 565))
        self.mark_sound = CreateImage(screen, "assets/gui/icons/mark_icon.png", (16, 16), 0, 100, ("center", "top"), (150, 565))

        self.settings_ok_button = CreateImage(screen, "assets/gui/buttons/btn_ok.png", (172, 74), 0, 100, ("center", "bottom"), (0, 15))

        """Récupération des inputs du joueur"""
        self.input_manager = InputManager()

    def blit_scene(self, screen):
        """Permet d'afficher les composants de la scène"""

        if self.blit:
            pygame.draw.rect(screen, self.parent.colors["BLACK"], self.black_background)
            self.background.blit(screen)
            self.settings_background.blit(screen)
            self.bg_set_pseudo1.blit(screen)
            self.settings_text.blit(screen)
            self.pseudo1_change_text.blit(screen)
            if self.active1:
                pygame.draw.rect(screen, self.parent.colors["WHITE"], self.input_Rect1, 2)
            self.pseudo_player1.blit(screen)
            self.bg_set_pseudo2.blit(screen)
            self.pseudo2_change_text.blit(screen)
            if self.active2:
                pygame.draw.rect(screen, self.parent.colors["WHITE"], self.input_Rect2, 2)
            self.pseudo_player2.blit(screen)
            self.bg_set_clavier.blit(screen)
            self.text_clavier.blit(screen)
            self.text_azerty.blit(screen)
            if self.parent.clavier == "AZERTY":
                pygame.draw.rect(screen, self.parent.colors["WHITE"], self.rect_azerty, 2)
            self.text_qwerty.blit(screen)
            if self.parent.clavier == "QWERTY":
                pygame.draw.rect(screen, self.parent.colors["WHITE"], self.rect_qwerty, 2)
            self.bg_set_show_fps.blit(screen)
            self.text_show_fps.blit(screen)
            self.check_box_bg_show_fps.blit(screen)
            if self.parent.show_fps:
                self.mark_show_fps.blit(screen)
            self.bg_set_sound.blit(screen)
            self.text_sound.blit(screen)
            self.check_box_bg_sound.blit(screen)
            if self.parent.sounds:
                self.mark_sound.blit(screen)
            self.settings_ok_button.blit(screen)

    def action(self, screen):
        """Check les events puis agit en conséquence"""

        if self.blit:
            event = self.input_manager.check_inputs()
            for i in range(0, len(event)):
                if event[i][0] == "leftclickdown":
                    if self.settings_ok_button.rect.collidepoint(event[i][1]):
                        self.refresh_settings(screen)
                        self.parent.blit = True
                        self.blit = False
                        self.set_active_input(False, False)
                    elif self.input_Rect1.collidepoint(event[i][1]):
                        self.set_active_input(True, False)
                    elif self.input_Rect2.collidepoint(event[i][1]):
                        self.set_active_input(False, True)
                    elif self.rect_azerty.collidepoint(event[i][1]):
                        self.parent.clavier = "AZERTY"
                        self.set_active_input(False, False)
                    elif self.rect_qwerty.collidepoint(event[i][1]):
                        self.parent.clavier = "QWERTY"
                        self.set_active_input(False, False)
                    elif self.check_box_bg_show_fps.rect.collidepoint(event[i][1]):
                        self.parent.show_fps = not self.parent.show_fps
                        self.set_active_input(False, False)
                    elif self.check_box_bg_sound.rect.collidepoint(event[i][1]):
                        self.parent.sounds = not self.parent.sounds
                        self.set_active_input(False, False)
                    else:
                        self.set_active_input(False, False)

                elif event[i][0] == "keydown":
                    if self.active1:
                        if event[i][1] == pygame.K_BACKSPACE:
                            self.parent.pseudo1 = self.parent.pseudo1[:-1]
                        elif event[i][1] == 27:
                            self.set_active_input(False, False)
                        elif event[i][1] == 9 or event[i][1] == 13 or event[i][1] == 271:
                            self.set_active_input(False, True)
                        elif len(self.parent.pseudo1) <= 16:
                            self.parent.pseudo1 += event[i][2]
                        self.pseudo_player1 = CreateText(screen, self.parent.pseudo1, self.parent.colors["WHITE"], (len(self.parent.pseudo1) * 20, 30), 0, ("center", "top"), (2, 200), False, None)

                    elif self.active2:
                        if event[i][1] == pygame.K_BACKSPACE:
                            self.parent.pseudo2 = self.parent.pseudo2[:-1]
                        elif event[i][1] == 27:
                            self.set_active_input(False, False)
                        elif event[i][1] == 9 or event[i][1] == 13 or event[i][1] == 271:
                            self.set_active_input(False, False)
                        elif len(self.parent.pseudo2) <= 16:
                            self.parent.pseudo2 += event[i][2]
                        self.pseudo_player2 = CreateText(screen, self.parent.pseudo2, self.parent.colors["WHITE"], (len(self.parent.pseudo2) * 20, 30), 0, ("center", "top"), (2, 315), False, None)

                    else:
                        if event[i][1] == 27:
                            self.refresh_settings(screen)
                            self.parent.blit = True
                            self.blit = False

    def set_active_input(self, a1, a2):
        """Modifie les zones de texte sélectionnées"""
        self.active1 = a1
        self.active2 = a2

    def refresh_settings(self, screen):
        """Permet de mettre à jour les paramètres"""

        self.parent.battle_mode_scene.select_character_scene.refresh_settings(screen)
        self.parent.battle_mode_scene.select_character_scene.fight_scene.refresh_settings(screen)