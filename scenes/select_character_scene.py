import pygame
import time
from bibliotheques.create_image import CreateImage
from bibliotheques.create_text import CreateText
from bibliotheques.input_manager import InputManager
from scenes.select_character_half_part_scene import SelectCharacterHalfPartScene
from scenes.fight_scene import FightScene

class SelectCharacterScene:
    """Objet permerttant de gérer la scène du choix des combattants"""

    def __init__(self, screen, parent):
        """Variables"""
        self.blit = False
        self.parent = parent
        self.premier_tour = True

        """Création des images de la scène"""
        self.background = self.parent.background
        self.separation_bar = CreateImage(screen, "assets/gui/icons/separation_bar.png", (720, 8), 90, 100, ("center", "top"), (0, 0))
        self.timer = CreateText(screen, "", self.parent.parent.colors["WHITE"], (70, 100), 0, ("center", "center"), (0, 0), False, None)
        self.return_button = CreateImage(screen, "assets/gui/buttons/btn_back.png", (154, 70), 0, 100, ("center", "bottom"), (0, 10))

        """Sons de la scène"""
        self.sound_move_cursor = pygame.mixer.Sound("assets/sounds/move.wav")
        self.sound_select_cursor = pygame.mixer.Sound("assets/sounds/select.wav")

        """Récupération des inputs du joueur"""
        self.input_manager = InputManager()

        """Création des sous-parties de la scène"""
        self.left_part = SelectCharacterHalfPartScene(screen, self, "left")
        self.right_part = SelectCharacterHalfPartScene(screen, self, "right")
        self.refresh_settings(screen)

        """Création des scènes suivantes"""
        self.fight_scene = FightScene(screen, self)

    def blit_scene(self, screen):
        """Permet d'afficher les composants de la scène"""

        if self.blit:
            self.background.blit(screen)
            self.separation_bar.blit(screen)
            self.timer.blit(screen)
            self.return_button.blit(screen)
            self.left_part.blit_part(screen)
            self.right_part.blit_part(screen)

            self.timer = CreateText(screen, "", self.parent.parent.colors["WHITE"], (70, 100), 0, ("center", "center"), (0, 0), False, None)
        else:
            self.fight_scene.blit_scene(screen)

    def action(self, screen):
        """Check les events puis agit en conséquence"""

        if self.blit:
            event = self.input_manager.check_inputs()

            for i in range(0, len(event)):
                if event[i][0] == "leftclickdown":
                    if self.return_button.rect.collidepoint(event[i][1]):
                        self.parent.blit = True
                        self.blit = False

                elif event[i][0] == "keydown":

                    if event[i][1] == 27:
                        self.left_part.selected = self.left_part.skin_selected
                        self.left_part.generate_new_selector(screen)
                        self.right_part.selected = self.right_part.skin_selected
                        self.right_part.generate_new_selector(screen)
                        self.premier_tour = True
                        self.timer = CreateText(screen, "", self.parent.parent.colors["WHITE"], (70, 100), 0, ("center", "center"), (0, 0), False, None)
                        self.parent.blit = True
                        self.blit = False

                    else:
                        self.left_part.event_analyse(screen, event, i)
                        self.right_part.event_analyse(screen, event, i)

            if self.left_part.selected == 4 and self.right_part.selected == 4:

                if self.premier_tour:
                    self.premier_temps = time.time()
                    self.premier_tour = False

                self.temps = time.time()

                self.timer = CreateText(screen, str(3 - int(self.temps - self.premier_temps)), self.parent.parent.colors["WHITE"], (70, 100), 0, ("center", "center"), (0, 0), False, None)

                if self.temps - self.premier_temps >= 3:
                    """Lancement du combat !"""

                    self.left_part.selected = self.left_part.skin_selected
                    self.left_part.generate_new_selector(screen)
                    self.right_part.selected = self.right_part.skin_selected
                    self.right_part.generate_new_selector(screen)
                    self.premier_tour = True
                    self.timer = CreateText(screen, "", self.parent.parent.colors["WHITE"], (70, 100), 0, ("center", "center"), (0, 0), False, None)
                    self.fight_scene.init_scene(screen)
                    self.fight_scene.left_part.player.set_stats(screen, self.left_part.skin_selected)
                    self.fight_scene.right_part.player.set_stats(screen, self.right_part.skin_selected)
                    self.fight_scene.blit = True
                    self.blit = False
        else:
            self.fight_scene.action(screen)

    def refresh_settings(self, screen):
        """Permet de mettre à jour les paramètres"""

        self.left_part.pseudo_text = CreateText(screen, self.parent.parent.pseudo1, self.parent.parent.colors["DARK_GOLD"], (len(self.parent.parent.pseudo1) * 30, 50), 0, ("1quarter", "top"), (0, 50), False, None)
        self.right_part.pseudo_text = CreateText(screen, self.parent.parent.pseudo2, self.parent.parent.colors["DARK_GOLD"], (len(self.parent.parent.pseudo2) * 30, 50), 0, ("3quarter", "top"), (0, 50), False, None)

        self.left_part.set_clavier()