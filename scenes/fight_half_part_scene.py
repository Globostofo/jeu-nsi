import pygame
from objets.player import Player

class FightHalfPartScene:
    """Objet permettant de gérer la demi-scène du combat"""

    def __init__(self, screen, parent, pos):
        """Constantes"""
        self.parent = parent

        """Variables"""
        self.pos = pos
        if self.pos == "left":
            self.center = "1quarter"
            self.set_clavier()
            self.key_down = pygame.K_s
            self.key_right = pygame.K_d
            self.key_attack = pygame.K_SPACE
        elif self.pos == "right":
            self.center = "3quarter"
            self.key_up = pygame.K_i
            self.key_left = pygame.K_j
            self.key_down = pygame.K_k
            self.key_right = pygame.K_l
            self.key_attack = pygame.K_n
        self.i = 0

        """Création des objets de la scène"""
        self.player = Player(screen, self, self.pos)

    def blit_part(self, screen):
        """Permet d'afficher les composants de cette partie"""

        self.pseudo_text.blit(screen)
        self.player.refresh_health_bar(screen)
        self.health_text.blit(screen)
        self.health_bar_border.blit(screen)
        self.health_bar_bg.blit(screen)
        self.health_bar.blit(screen)
        if self.parent.phase != "pause":
            self.player.anims_manager.set_frame(screen)
        if self.parent.phase == "engagement" or self.parent.phase == "combat":
            self.action(screen)
        self.player.sprite.blit(screen)
        if self.player.afficher_commentaire:
            self.player.commentaire.position = (self.player.sprite.rect.x + self.player.sprite.rect.w / 2, self.player.sprite.rect.y)
            self.player.commentaire.set_position()
            self.player.blit_commentaire(screen)

    def action(self, screen):
        """Fonction qui se répète à l'infini (quand on est dans la bonne phase de jeu) pour gérer les inputs et les déplacements du joueur ainsi que le mouvement des projectiles"""

        try : left = self.parent.input_manager.pressed[self.key_left]
        except : left = 0
        try : right = self.parent.input_manager.pressed[self.key_right]
        except : right = 0

        self.player.input_vector = pygame.math.Vector2(right - left, 0)

        if self.player.input_vector != [0, 0]:
            if self.i < 5:
                self.i += 1
            self.player.refresh_sprite_position(self.player.input_vector * self.player.max_speed, self.player.acceleration, self.i)
        else:
            if self.i > 0:
                self.i -= 1
            self.player.refresh_sprite_position(self.player.velocity, self.player.friction, self.i)

    def set_clavier(self):
        """Permet de set les touches en fonction du clavier choisi"""

        if self.parent.parent.parent.parent.clavier == "AZERTY":
            self.key_up = pygame.K_z
            self.key_left = pygame.K_q
        elif self.parent.parent.parent.parent.clavier == "QWERTY":
            self.key_up = pygame.K_w
            self.key_left = pygame.K_a