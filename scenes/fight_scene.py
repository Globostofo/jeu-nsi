import pygame
import random
from bibliotheques.create_image import CreateImage
from bibliotheques.create_text import CreateText
from bibliotheques.create_button import CreateButton
from bibliotheques.create_rect import CreateRect
from bibliotheques.input_manager import InputManager
from scenes.fight_half_part_scene import FightHalfPartScene
from objets.projectile import Projectile

class FightScene:
    """Objet permettant de gérer la scène du combat"""

    def __init__(self, screen, parent):
        """Constantes"""
        self.parent = parent

        """Variables"""
        self.blit = False
        self.text_color = self.parent.parent.parent.colors["WHITE"]

        """Création des images de la scène"""
        self.tiny_menu_button = CreateImage(screen, "assets/gui/buttons/tiny_btn_menu.png", (66, 32), 0, 100, ("center", "top"), (0, 10))
        self.pause_panel = CreateImage(screen, "assets/gui/backgrounds_panels/pause_panel.png", (438, 549), 0, 100, ("center", "center"), (0, 0))
        self.pause_text = CreateText(screen, "Que voulez-vous faire ?", self.parent.parent.parent.colors["WHITE"], (23 * 15, 30), 0, ("center", "center"), (0, 120), False, None)
        self.pause_continue_button = CreateButton(screen, "assets/gui/buttons/btn_bg.png", (300, 72), ("center", "center"), (0, 0), "CONTINUER", self.parent.parent.parent.colors["DARK_GOLD"], (15 * 9, 24), ("center", "center"), (0, 0))
        self.pause_restart_button = CreateButton(screen, "assets/gui/buttons/btn_bg.png", (300, 72), ("center", "center"), (0, -90), "RECOMMENCER", self.parent.parent.parent.colors["DARK_GOLD"], (15 * 11, 24), ("center", "center"), (0, 0))
        self.pause_menu_button = CreateButton(screen, "assets/gui/buttons/btn_bg.png", (300, 72), ("center", "center"), (0, -180), "MENU", self.parent.parent.parent.colors["DARK_GOLD"], (15 * 4, 24), ("center", "center"), (0, 0))

        self.victory_panel = CreateImage(screen, "assets/gui/backgrounds_panels/victory_panel.png", (432, 366), 0, 100, ("center", "center"), (0, 0))
        self.left_star = CreateImage(screen, "assets/gui/icons/star_icon.png", (39, 36), 0, 100, ("center", "center"), (-100, 144))
        self.right_star = CreateImage(screen, "assets/gui/icons/star_icon.png", (39, 36), 0, 100, ("center", "center"), (100, 144))
        self.replay_button = CreateButton(screen, "assets/gui/buttons/btn_bg.png", (200, 48), ("center", "center"), (-105, -175), "REJOUER", self.parent.parent.parent.colors["DARK_GOLD"], (15 * 7, 24), ("center", "center"), (0, 0))
        self.menu_button = CreateButton(screen, "assets/gui/buttons/btn_bg.png", (200, 48), ("center", "center"), (105, -175), "MENU", self.parent.parent.parent.colors["DARK_GOLD"], (15 * 4, 24), ("center", "center"), (0, 0))
        self.filet = CreateRect(screen, self.parent.parent.parent.colors["WHITE"], (20, 160), ("center", "bottom"), (0, 30))

        """Sons de la scène"""
        self.sound_esquive = pygame.mixer.Sound("assets/sounds/esquive.wav")
        self.sound_coup_crit = pygame.mixer.Sound("assets/sounds/coup_crit.wav")
        self.sound_hurt = pygame.mixer.Sound("assets/sounds/hurt.wav")
        self.sound_death = pygame.mixer.Sound("assets/sounds/death.wav")

        self.sound_pause = pygame.mixer.Sound("assets/sounds/pause.wav")
        self.sound_unpause = pygame.mixer.Sound("assets/sounds/unpause.wav")

        """Récupération des inputs du joueur"""
        self.input_manager = InputManager()

        """Création des sous-parties de la scène"""
        self.left_part = FightHalfPartScene(screen, self, "left")
        self.right_part = FightHalfPartScene(screen, self, "right")

    def init_scene(self, screen):
        """Regénère la scène de combat"""

        bg = random.randint(1, 4)
        self.background = CreateImage(screen, "assets/backgrounds/City%s/City%s.png"%(bg, bg), (screen.get_width(), screen.get_height()), 0, 100, ("left", "top"), (0, 0))

        self.ground_height = 670

        k, sommeR, sommeG, sommeB = 0, 0, 0, 0
        for i in range(0, self.background.image.get_width()):
            for j in range(0, 60):
                k += 1
                sommeR += self.background.image.get_at((i, j))[0]
                sommeG += self.background.image.get_at((i, j))[1]
                sommeB += self.background.image.get_at((i, j))[2]
        moyenne = (sommeR / k, sommeG / k, sommeB / k)

        if moyenne[0] < 150 and moyenne[1] < 150 and moyenne[2] < 150:
            self.text_color = self.parent.parent.parent.colors["WHITE"]
        else:
            self.text_color = self.parent.parent.parent.colors["BLACK"]

        self.refresh_settings(screen)

        self.phase = "engagement"
        self.nbr_retours = 0
        self.balle = Projectile(screen, self, "middle")

    def blit_scene(self, screen):
        """Permet d'afficher les composants de la scène"""

        if self.blit:
            self.background.blit(screen)
            self.filet.blit(screen)
            self.left_part.blit_part(screen)
            self.right_part.blit_part(screen)
            if self.phase != "pause" and self.phase != "fin":
                self.tiny_menu_button.blit(screen)
            self.balle.sprite.blit(screen)

            if self.phase == "pause":
                self.pause_panel.blit(screen)
                self.pause_text.blit(screen)
                self.pause_continue_button.blit(screen)
                self.pause_restart_button.blit(screen)
                self.pause_menu_button.blit(screen)

            if self.phase == "fin":
                self.victory_panel.blit(screen)
                self.left_star.blit(screen)
                self.right_star.blit(screen)
                self.end_game_info1.blit(screen)
                self.end_game_info2.blit(screen)
                self.replay_button.blit(screen)
                self.menu_button.blit(screen)

    def action(self, screen):
        """Check les events puis agit en conséquence (et sers aussi de _physics_process)"""

        if self.blit:
            event = self.input_manager.check_inputs()

            for i in range(0, len(event)):
                if event[i][0] == "leftclickdown":
                    if self.phase == "engagement" or self.phase == "combat":
                        if self.tiny_menu_button.rect.collidepoint(event[i][1]):
                            if self.parent.parent.parent.sounds:
                                self.sound_pause.play()
                            self.temp = self.phase
                            self.phase = "pause"
                    elif self.phase == "pause":
                        if self.pause_continue_button.rect.collidepoint(event[i][1]):
                            if self.parent.parent.parent.sounds:
                                self.sound_unpause.play()
                            self.phase = self.temp
                        elif self.pause_restart_button.rect.collidepoint(event[i][1]):
                            self.parent.blit = True
                            self.blit = False
                        elif self.pause_menu_button.rect.collidepoint(event[i][1]):
                            self.parent.parent.parent.blit = True
                            self.blit = False
                    elif self.phase == "fin":
                        if self.replay_button.rect.collidepoint(event[i][1]):
                            self.parent.blit = True
                            self.blit = False
                        elif self.menu_button.rect.collidepoint(event[i][1]):
                            self.parent.parent.parent.blit = True
                            self.blit = False

                elif event[i][0] == "keydown":
                    if self.phase == "engagement" or self.phase == "combat":
                        print(event[i][1])
                        if event[i][1] == 27:
                            self.temp = self.phase
                            self.phase = "pause"
                        elif event[i][1] == self.left_part.key_up:
                            self.left_part.player.jump()
                        elif event[i][1] == self.right_part.key_up:
                            self.right_part.player.jump()
                        elif event[i][1] == self.left_part.key_attack or event[i][1] == self.right_part.key_attack:
                            self.balle.set_new_velocity(event[i][1])

            if self.phase == "combat":
                self.balle.move(screen)

            elif self.phase == "end_point":
                self.end_point(screen)

            elif self.phase == "death":
                self.end_game()

    def init_end_point(self, screen, loser):
        """S'active quand la balle touche le sol"""

        self.loser = loser
        self.nbr_retours += self.balle.nbr_retours
        self.phase = "end_point"

        if loser == "left":
            esquive = self.left_part.player.check_for_esquive()
            coup_crit = self.right_part.player.check_for_coup_crit()

            if not esquive:
                if coup_crit:
                    if self.parent.parent.parent.sounds:
                        self.sound_coup_crit.play()
                    self.left_part.player.damage(screen, 10 * self.right_part.player.attack * 2)
                    self.right_part.player.set_commentaire(screen, "coup crit.", 1)
                else:
                    if self.parent.parent.parent.sounds:
                        self.sound_hurt.play()
                    self.left_part.player.damage(screen, 10 * self.right_part.player.attack)
            else:
                if self.parent.parent.parent.sounds:
                    self.sound_esquive.play()
                self.left_part.player.set_commentaire(screen, "esquive", 1)
                if coup_crit:
                    self.right_part.player.set_commentaire(screen, "coup crit.", 1)

            self.right_part.player.heal_player()

            if self.phase == "end_point":
                self.left_part.player.anims_manager.set_current_anim("hurt")
                self.right_part.player.anims_manager.set_current_anim("idle")

        elif loser == "right":
            esquive = self.right_part.player.check_for_esquive()
            coup_crit = self.left_part.player.check_for_coup_crit()

            if not esquive:
                if coup_crit:
                    if self.parent.parent.parent.sounds:
                        self.sound_coup_crit.play()
                    self.right_part.player.damage(screen, 10 * self.left_part.player.attack * 2)
                    self.left_part.player.set_commentaire(screen, "coup crit.", 1)
                else:
                    self.right_part.player.damage(screen, 10 * self.left_part.player.attack)
                    if self.phase == "end_point":
                        if self.parent.parent.parent.sounds:
                            self.sound_hurt.play()
            else:
                if self.parent.parent.parent.sounds:
                    self.sound_esquive.play()
                self.right_part.player.set_commentaire(screen, "esquive", 1)
                if coup_crit:
                    self.left_part.player.set_commentaire(screen, "coup crit.", 1)

            self.left_part.player.heal_player()

            if self.phase == "end_point":
                self.right_part.player.anims_manager.set_current_anim("hurt")
                self.left_part.player.anims_manager.set_current_anim("idle")

    def end_point(self, screen):
        if self.left_part.player.anims_manager.end or self.right_part.player.anims_manager.end:
            self.phase = "engagement"
            self.left_part.player.sprite.rect.x = 150
            self.left_part.player.sprite.rect.y = self.ground_height - self.left_part.player.sprite.rect.h
            self.left_part.player.flip = False
            self.left_part.player.anims_manager.set_current_anim("idle")
            self.left_part.player.velocity.x = 0
            self.left_part.player.velocity.y = 0

            self.right_part.player.sprite.rect.x = screen.get_width() - self.right_part.player.sprite.rect.w - 150
            self.right_part.player.sprite.rect.y = self.ground_height - self.right_part.player.sprite.rect.h
            self.right_part.player.flip = True
            self.right_part.player.anims_manager.set_current_anim("idle")
            self.right_part.player.velocity.x = 0
            self.right_part.player.velocity.y = 0

            self.balle = Projectile(screen, self, self.loser)

    def init_end_game(self, screen, loser):
        """S'active quand un joueur n'a plus de vie"""

        self.loser = loser
        self.phase = "death"
        if loser == "left":
            winner = self.parent.parent.parent.pseudo2
            self.left_part.player.anims_manager.set_current_anim("death")
            self.right_part.player.anims_manager.set_current_anim("idle")
        elif loser == "right":
            winner = self.parent.parent.parent.pseudo1
            self.right_part.player.anims_manager.set_current_anim("death")
            self.left_part.player.anims_manager.set_current_anim("idle")
        if self.nbr_retours > 1:
            pluriel = "s"
        else:
            pluriel = ""
        self.end_game_info1 = CreateText(screen, "%s a gagné !"%winner, self.parent.parent.parent.colors["WHITE"], (len(winner) * 15 + 150, 30), 0, ("center", "center"), (0, 50), False, None)
        self.end_game_info2 = CreateText(screen, "%s échange%s"%(self.nbr_retours, pluriel), self.parent.parent.parent.colors["WHITE"], ((len(str(self.nbr_retours)) + 9 + len(pluriel)) * 15, 30), 0, ("center", "center"), (0, 0), False, None)
        if self.parent.parent.parent.sounds:
            self.sound_death.play()

    def end_game(self):

        if self.left_part.player.anims_manager.end or self.right_part.player.anims_manager.end:
            self.phase = "fin"

    def refresh_settings(self, screen):
        """Permet de mettre à jour les paramètres"""

        self.left_part.pseudo_text = CreateText(screen, self.parent.parent.parent.pseudo1, self.text_color, (len(self.parent.parent.parent.pseudo1) * 20, 35), 0, ("left", "top"), (30, 20), False, None)
        self.right_part.pseudo_text = CreateText(screen, self.parent.parent.parent.pseudo2, self.text_color, (len(self.parent.parent.parent.pseudo2) * 20, 35), 0, ("right", "top"), (30, 20), False, None)

        self.left_part.set_clavier()

    def check_collision(self, sprite1, sprite2):
        """Check les collisions entre sprite1 et sprite2 (retourne un bool)"""
        return pygame.sprite.collide_rect(sprite1, sprite2)