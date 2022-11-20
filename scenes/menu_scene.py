import pygame
from bibliotheques.create_image import CreateImage
from bibliotheques.create_button import CreateButton
from bibliotheques.input_manager import InputManager
from scenes.battle_mode_scene import BattleModeScene
from scenes.settings_scene import SettingsScene
from scenes.tchat_scene import TchatScene
from bibliotheques.create_text import CreateText
from serveur.client import Tchat

class MenuScene:
    """Objet permettant de gérer la scène du menu principal"""

    def __init__(self, screen, colors):
        """Constantes"""
        self.colors = colors

        """Variables"""
        self.blit = True
        self.pseudo1 = "PLAYER 1"
        self.pseudo2 = "PLAYER 2"
        self.clavier = "QWERTY"
        self.show_fps = True
        self.sounds = False

        """Création des images de la scène"""
        VARIABLE=Tchat.nobredexonexions()
        self.background = CreateImage(screen, "assets/gui/backgrounds_panels/bg.png", (screen.get_width(), screen.get_height()), 0, 100, ("left", "top"), (0, 0))
        self.btn_play = CreateButton(screen, "assets/gui/buttons/btn_bg.png", (300, 72), ("center", "center"), (0, 50), "PLAY", self.colors["DARK_GOLD"], (4 * 15, 24), ("center", "center"), (0, 0))
        self.btn_settings = CreateButton(screen, "assets/gui/buttons/btn_bg.png", (300, 72), ("center", "center"), (0, -50), "SETTINGS", self.colors["DARK_GOLD"], (8 * 15, 24), ("center", "center"), (0, 0))
        self.tchat_button = CreateImage(screen, "assets/gui/buttons/btn_tchat.png", (64, 64), 0, 100, ("left", "top"), (15, 15))
        self.exit_button = CreateImage(screen, "assets/gui/buttons/btn_exit.png", (32, 32), 0, 100, ("right", "top"), (15, 15))
        self.text_nbr_connectes = CreateText(screen, "%s connecté(s)"%VARIABLE, self.colors["WHITE"], ((10 + len(str(VARIABLE))) * 15, 30), 0, ("right", "bottom"), (5, 5), False, None)

        """Récupération des inputs du joueur"""
        self.input_manager = InputManager()

        """Création des scènes suivantes"""
        self.battle_mode_scene = BattleModeScene(screen, self)
        self.settings_scene = SettingsScene(screen, self)
        self.tchat_scene = TchatScene(screen, self)

    def blit_scene(self, screen):
        """Permet d'afficher tous les composants de la scène et des scènes suivantes"""

        if self.blit:
            self.background.blit(screen)
            self.btn_play.blit(screen)
            self.btn_settings.blit(screen)
            self.tchat_button.blit(screen)
            self.exit_button.blit(screen)
            self.refresh_nbr_connection(screen)
            self.text_nbr_connectes.blit(screen)
        else:
            self.battle_mode_scene.blit_scene(screen)
            self.settings_scene.blit_scene(screen)
            self.tchat_scene.blit_scene(screen)

    def action(self, screen):
        """Check les events puis agit en conséquence"""

        if self.blit:
            event = self.input_manager.check_inputs()

            for i in range(0, len(event)):
                if event[i][0] == "leftclickdown":
                    if self.btn_play.rect.collidepoint(event[i][1]):
                        self.battle_mode_scene.blit = True
                        self.blit = False
                    elif self.btn_settings.rect.collidepoint(event[i][1]):
                        self.settings_scene.blit = True
                        self.blit = False
                    elif self.tchat_button.rect.collidepoint(event[i][1]):
                        self.tchat_scene.blit = True
                        self.tchat_scene.tempTchatlistemsg=[" "]
                        self.blit = False
                    elif self.exit_button.rect.collidepoint(event[i][1]):
                        pygame.quit()

                elif event[i][0] == "keydown":
                    if event[i][1] == 27:
                        pygame.quit()
        else:
            self.battle_mode_scene.action(screen)
            self.settings_scene.action(screen)
            self.tchat_scene.action(screen)

    def refresh_nbr_connection(self,screen):
        """Permet de mettre à jour le texte du nombre de joueurs connectés en bas à droite"""

        connectes = int(Tchat.nobredexonexions())
        if connectes > 1:
            pluriel = "s"
        else:
            pluriel = ""
        self.text_nbr_connectes = CreateText(screen, "%s connecté%s"%(connectes, pluriel), self.colors["WHITE"], ((10 + len(str(connectes))) * 15, 30), 0, ("right", "bottom"), (5, 5), False, None)