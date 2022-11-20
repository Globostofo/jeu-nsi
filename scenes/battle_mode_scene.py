from bibliotheques.create_image import CreateImage
from bibliotheques.create_button import CreateButton
from bibliotheques.input_manager import InputManager
from scenes.select_character_scene import SelectCharacterScene

class BattleModeScene:
    """Objet permerttant de gérer la scène du choix de bataille"""

    def __init__(self, screen, parent):
        """Variables"""
        self.blit = False
        self.parent = parent

        """Création des images de la scène"""
        self.background = self.parent.background
        self.btn_back = CreateImage(screen, "assets/gui/buttons/btn_back.png", (154, 70), 0, 100, ("left", "top"), (15, 15))
        self.btn_singleplayer = CreateButton(screen, "assets/gui/buttons/btn_bg.png", (300, 72), ("center", "center"), (0, 100), "SINGLE PLAYER", self.parent.colors["DARK_GOLD"], (13 * 15, 24), ("center", "center"), (0, 0))
        self.btn_2players = CreateButton(screen, "assets/gui/buttons/btn_bg.png", (300, 72), ("center", "center"), (0, 0), "2 PLAYERS", self.parent.colors["DARK_GOLD"], (9 * 15, 24), ("center", "center"), (0, 0))
        self.btn_multiplayer = CreateButton(screen, "assets/gui/buttons/btn_bg.png", (300, 72), ("center", "center"), (0, -100), "MULTIPLAYER", self.parent.colors["DARK_GOLD"], (11 * 15, 24), ("center", "center"), (0, 0))

        """Récupération des inputs du joueur"""
        self.input_manager = InputManager()

        """Création des scènes suivantes"""
        self.select_character_scene = SelectCharacterScene(screen, self)

    def blit_scene(self, screen):
        """Permet d'afficher les composants de la scène"""

        if self.blit:
            self.background.blit(screen)
            self.btn_back.blit(screen)
            self.btn_singleplayer.blit(screen)
            self.btn_2players.blit(screen)
            self.btn_multiplayer.blit(screen)
        else:
            self.select_character_scene.blit_scene(screen)

    def action(self, screen):
        """Check les events puis agit en conséquence"""

        if self.blit:
            event = self.input_manager.check_inputs()

            for i in range(0, len(event)):
                if event[i][0] == "leftclickdown":
                    if self.btn_back.rect.collidepoint(event[i][1]):
                        self.parent.blit = True
                        self.blit = False
                    elif self.btn_singleplayer.rect.collidepoint(event[i][1]):
                        print("bouton 1")
                    elif self.btn_2players.rect.collidepoint(event[i][1]):
                        self.select_character_scene.blit = True
                        self.blit = False
                    elif self.btn_multiplayer.rect.collidepoint(event[i][1]):
                        print("bouton 3")

                elif event[i][0] == "keydown":
                    if event[i][1] == 27:
                        self.parent.blit = True
                        self.blit = False
        else:
            self.select_character_scene.action(screen)