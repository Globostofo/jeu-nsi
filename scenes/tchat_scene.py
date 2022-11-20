import pygame
from bibliotheques.create_image import CreateImage
from bibliotheques.create_text import CreateText
from bibliotheques.input_manager import InputManager
from serveur.client import Tchat

class TchatScene:
    """Objet permettant de gérer la scène du tchat"""

    def __init__(self, screen, parent):
        """Initialisation du tchat"""
        Tchat.start()

        """Variables"""
        self.blit = False
        self.parent = parent
        self.tchat_text = ""
        self.tchat_bar_active = False
        self.tempTchatlistemsg=[]
        self.Tchatlistemsg=[]

        """Création des images de la scène"""
        self.black_background = pygame.Rect(0, 0, screen.get_width(), screen.get_height())
        self.background = CreateImage(screen, "assets/gui/backgrounds_panels/bg.png", (screen.get_width(), screen.get_height()), 0, 60, ("left", "top"), (0, 0))
        self.return_tchat_button = CreateImage(screen, "assets/gui/buttons/btn_back.png", (154, 70), 0, 100, ("left", "top"), (15, 15))
        self.bg_tchat = CreateImage(screen, "assets/gui/backgrounds_panels/setting_panel.png", (555, 693), 0, 100, ("center", "center"), (0, 0))
        self.channel_text = CreateText(screen, "GLOBAL", self.parent.colors["DARK_GOLD"], (225, 65), 0, ("center", "top"), (0, 47), False, None)
        self.ligne = ""
        self.input_Rect_tchat_bar = pygame.Rect(int(screen.get_width() / 2) - 250, screen.get_height() - 65, 500, 35)
        self.text = CreateText(screen, self.tchat_text, self.parent.colors["WHITE"], (len(self.tchat_text) * 10, 25), 0, ("left", "bottom"), (395, 33), False, None)

        """Récupération des inputs du joueur"""
        self.input_manager = InputManager()

    def blit_scene(self, screen):
        """Permet d'afficher les composants de la scène"""
        if self.blit:
            self.Tchatlistemsg=Tchat.listemsg()
            if self.Tchatlistemsg != self.tempTchatlistemsg:
                pygame.draw.rect(screen, self.parent.colors["BLACK"], self.black_background)
                self.background.blit(screen)
                self.return_tchat_button.blit(screen)
            if self.Tchatlistemsg != self.tempTchatlistemsg:
                self.bg_tchat.blit(screen)
                self.blit_tchat(screen)
                self.channel_text.blit(screen)
            pygame.draw.rect(screen, self.parent.colors["DISCORD_DARK_GRAY"], self.input_Rect_tchat_bar)
            if self.tchat_bar_active:
                pygame.draw.rect(screen, self.parent.colors["DARK_GOLD"], self.input_Rect_tchat_bar, 3)
            self.text.blit(screen)
            self.tempTchatlistemsg=self.Tchatlistemsg

    def action(self, screen):
        """Check les events puis agit en conséquence"""

        if self.blit:
            event = self.input_manager.check_inputs()

            for i in range(0, len(event)):
                if event[i][0] == "leftclickdown":
                    if self.return_tchat_button.rect.collidepoint(event[i][1]):
                        self.parent.blit = True
                        self.blit = False
                        self.tchat_bar_active = False
                    elif self.input_Rect_tchat_bar.collidepoint(event[i][1]):
                        self.tchat_bar_active = True
                    else:
                        self.tchat_bar_active = False

                elif event[i][0] == "keydown":
                    if self.tchat_bar_active:
                        if event[i][1] == pygame.K_BACKSPACE:
                            self.tchat_text = self.tchat_text[:-1]
                        elif event[i][1] == 27:
                            self.tchat_bar_active = False
                        elif event[i][1] == 13 or event[i][1] == 271:
                            if self.tchat_text != "":
                                Tchat.envoi(self.parent.pseudo1, self.tchat_text)
                                self.tchat_text = ""
                        elif len(self.tchat_text) <= 100:
                            self.tchat_text += event[i][2]
                        self.text = CreateText(screen, self.tchat_text[-48:], self.parent.colors["WHITE"], (len(self.tchat_text[:48]) * 10, 23), 0, ("left", "bottom"), (395, 33), False, None)
                    else:
                        if event[i][1] == 27:
                            self.parent.blit = True
                            self.blit = False

    def blit_tchat(self, screen):
        """Affiche le tchat online / communique avec le serveur"""



        i=0
        px=i+1
        while i<len(self.Tchatlistemsg) and px<8 :
            i=i+1


            pseudo = self.Tchatlistemsg[len(self.Tchatlistemsg)-i][1][0]
            date = self.Tchatlistemsg[len(self.Tchatlistemsg)-i][0]
            texte = self.Tchatlistemsg[len(self.Tchatlistemsg)-i][1][1]
            # try:
            if pseudo == self.parent.pseudo1:
                pos = "right"
            else:
                pos = "left"
            temp=TchatScene.ALaLinge(texte)
            for j in range(len(temp)):
                ligne_texte = CreateText(screen, temp[len(temp)-j-1], self.parent.colors["WHITE"], ((len(temp[len(temp)-j-1])) * 15, 30), 0, (pos, "top"), (390, (px-1) * -75 + 605), False, None)
                if ligne_texte.margin[1] >= 100:
                    ligne_texte.blit(screen)
                px=px+0.5

            px=px-0.5

            ligne_pseudo = CreateText(screen, pseudo, self.parent.colors["DARK_GOLD"], (len(pseudo) * 10, 20), 0, (pos, "top"), (390, (px-1) * -75 + 585), False, None)
            ligne_date = CreateText(screen, date, self.parent.colors["DISCORD_LIGHT_GRAY"], (len(date) * 8, 16), 0, (pos, "top"), (390 + len(pseudo) * 10 + 10, (px -1) * -75 + 587), False, None)
            px=px+1
            if ligne_pseudo.margin[1] >= 100:
                ligne_pseudo.blit(screen)
            if ligne_date.margin[1] >= 100:
                ligne_date.blit(screen)



            # except:

                # pass


    def ALaLinge(txte):
        espace=30
        msg=[]
        if len(txte) > 30 :
            for i in range(8,30):
                if txte[i]==" ":
                    espace=i
                if txte[espace]==" ":
                    temp=TchatScene.ALaLinge(txte[espace+1:])
                else:
                    temp=TchatScene.ALaLinge(txte[espace:])
            msg.append(txte[:espace])
            for i in range(len(temp)):
                msg.append(temp[i])

            return msg
        return [txte]

