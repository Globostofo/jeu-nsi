import pygame.math
import time
import random
from bibliotheques.create_image import CreateImage
from bibliotheques.create_text import CreateText
from bibliotheques.create_rect import CreateRect
from bibliotheques.sprites_anims_manager import SpritesAnimsManager

class Player:
    """Objet qui gère les joueur pendant un combat"""

    def __init__(self, screen, parent, pos):
        """Constantes"""
        self.parent = parent
        self.pos = pos
        if self.pos == "left":
            self.limits = (5, screen.get_width() / 2 - 10)
            self.recul = -1
            self.projectile_velocity = 8
        elif self.pos == "right":
            self.limits = (screen.get_width() / 2 + 10, screen.get_width() - 5)
            self.recul = 1
            self.projectile_velocity = -8
        self.acceleration = 0.2
        self.friction = 0.2

        """Variables"""
        self.velocity = pygame.math.Vector2(0, 0)
        self.v_speed = 0
        self.afficher_commentaire = False

        """Gère l'animation du sprite"""
        self.anims_manager = SpritesAnimsManager(self)

    def set_stats(self, screen, skin):
        """Permet de modifier les stats du joueur en fonction du personnage choisi"""

        self.anims_manager.reset_anims()

        self.max_health = 100
        self.attack = 1
        self.defense = 1
        self.max_speed = 10
        self.esquive = 0
        self.jump_height = 1
        self.heal = 0
        self.coup_crit = 0
        self.hit_speed = 1

        if skin == 1:
            self.sprite = CreateImage(screen, "assets/players/1 Woodcutter/Woodcutter.png", (26 * 4, 32 * 4), 0, 100, (self.pos, "bottom"), (150, 50))
            self.anims_manager.create_new_anim("idle", "assets/players/1 Woodcutter/Woodcutter_idle%s.png", (27, 32), 4, 1, True)
            self.anims_manager.create_new_anim("walk", "assets/players/1 Woodcutter/Woodcutter_walk%s.png", (26, 34), 6, 10, True)
            self.anims_manager.create_new_anim("run", "assets/players/1 Woodcutter/Woodcutter_run%s.png", (32, 30), 6, 10, True)
            self.anims_manager.create_new_anim("jump", "assets/players/1 Woodcutter/Woodcutter_jump%s.png", (26, 31), 6, 10, False)
            self.anims_manager.create_new_anim("hurt", "assets/players/1 Woodcutter/Woodcutter_hurt%s.png", (26, 33), 3, 8, False)
            self.anims_manager.create_new_anim("death", "assets/players/1 Woodcutter/Woodcutter_death%s.png", (32, 32), 6, 3, False)
            self.max_health = 135
            self.attack = 1.5
            self.defense = 1.25
        elif skin == 2:
            self.sprite = CreateImage(screen, "assets/players/2 GraveRobber/GraveRobber.png", (19 * 4, 33 * 4), 0, 100, (self.pos, "bottom"), (150, 50))
            self.anims_manager.create_new_anim("idle", "assets/players/2 GraveRobber/GraveRobber_idle%s.png", (20, 33), 4, 1, True)
            self.anims_manager.create_new_anim("walk", "assets/players/2 GraveRobber/GraveRobber_walk%s.png", (23, 35), 6, 12, True)
            self.anims_manager.create_new_anim("run", "assets/players/2 GraveRobber/GraveRobber_run%s.png", (26, 33), 6, 12, True)
            self.anims_manager.create_new_anim("jump", "assets/players/2 GraveRobber/GraveRobber_jump%s.png", (20, 39), 6, 8, False)
            self.anims_manager.create_new_anim("hurt", "assets/players/2 GraveRobber/GraveRobber_hurt%s.png", (21, 33), 3, 8, False)
            self.anims_manager.create_new_anim("death", "assets/players/2 GraveRobber/GraveRobber_death%s.png", (35, 33), 6, 3, False)
            self.max_speed = 12
            self.esquive = 25
            self.jump_height = 1.2
        elif skin == 3:
            self.sprite = CreateImage(screen, "assets/players/3 SteamMan/SteamMan.png", (20 * 4, 36 * 4), 0, 100, (self.pos, "bottom"), (150, 50))
            self.anims_manager.create_new_anim("idle", "assets/players/3 SteamMan/SteamMan_idle%s.png", (21, 36), 4, 1, True)
            self.anims_manager.create_new_anim("walk", "assets/players/3 SteamMan/SteamMan_walk%s.png", (23, 38), 6, 10, True)
            self.anims_manager.create_new_anim("run", "assets/players/3 SteamMan/SteamMan_run%s.png", (31, 34), 6, 10, True)
            self.anims_manager.create_new_anim("jump", "assets/players/3 SteamMan/SteamMan_jump%s.png", (26, 37), 6, 10, False)
            self.anims_manager.create_new_anim("hurt", "assets/players/3 SteamMan/SteamMan_hurt%s.png", (22, 37), 3, 8, False)
            self.anims_manager.create_new_anim("death", "assets/players/3 SteamMan/SteamMan_death%s.png", (40, 36), 6, 3, False)
            self.heal = 5
            self.coup_crit = 20
            self.hit_speed = 1.25

        self.health = self.max_health
        self.len = self.health

        if self.pos == "left":
            self.flip = False
        elif self.pos == "right":
            self.flip = True

        self.anims_manager.set_current_anim("idle")

    def damage(self, screen, value):
        """Fonction activée pour retirer de la vie au joueur"""

        value /= self.defense

        self.health -= value

        if self.health <= 0:
            """Fin du combat !"""
            self.parent.parent.init_end_game(screen, self.pos)

    def heal_player(self):
        """Fonction activée pour ajouter de la vie au joueur"""

        if self.health + self.heal < self.max_health:
            self.health += self.heal
        else:
            self.health = self.max_health

    def refresh_sprite_position(self, vector, value, i):
        """Modifie la position du sprite"""

        self.velocity = vector * (value * i) * (self.parent.parent.parent.parent.parent.dt / (1000/60))

        if self.sprite.rect.x + self.velocity.x < self.limits[0]:
            self.sprite.rect.x = self.limits[0]
        elif self.sprite.rect.x + self.sprite.rect.w + self.velocity.x > self.limits[1]:
            self.sprite.rect.x = self.limits[1] - self.sprite.rect.w
        else:
            self.sprite.rect.x += self.velocity.x

        if self.velocity.x > 0:
            self.flip = False
        elif self.velocity.x < 0:
            self.flip = True

        if self.anims_manager.current_anim[0] == "jump":
            if self.anims_manager.end:
                self.anims_manager.set_current_anim("idle")
        else:
            if self.velocity.x == 0:
                self.anims_manager.set_current_anim("idle")
            elif abs(self.velocity.x) < self.max_speed:
                self.anims_manager.set_current_anim("walk")
            elif abs(self.velocity.x) >= self.max_speed:
                self.anims_manager.set_current_anim("run")

        self.velocity.y = self.v_speed
        self.sprite.rect.y -= self.velocity.y

        if self.sprite.rect.y + self.sprite.rect.h <= self.parent.parent.ground_height:
            self.v_speed -= 1
        else:
            self.sprite.rect.y = self.parent.parent.ground_height - self.sprite.rect.h

    def jump(self):
        """Ajoute de la vitesse verticale au joueur pour sauter (s'il touche le sol)"""

        if self.sprite.rect.y + self.sprite.rect.h >= self.parent.parent.ground_height:
            self.v_speed = 15 * self.jump_height
            self.anims_manager.set_current_anim("jump")

    def set_commentaire(self, screen, text, temps):
        """Créer un commentaire (zone de texte qui s'affiche lors d'une esquive ou d'un coup critique)"""
        self.afficher_commentaire = True
        self.end_time = time.time() + temps
        self.commentaire = CreateText(screen, text, self.parent.parent.parent.parent.parent.colors["WHITE"], (len(text) * 20, 40), 0, (self.sprite.rect.x + self.sprite.rect.w / 2, self.sprite.rect.y), (len(text) * 20 / -2, -40), True, self.parent.parent.parent.parent.parent.colors["BLACK"])

    def blit_commentaire(self, screen):
        """Affiche le commentaire créé dans la méthode ci-dessus"""
        if self.end_time >= time.time():
            self.commentaire.blit(screen)
        else:
            self.afficher_commentaire = False

    def refresh_health_bar(self, screen):
        """Met à jour la barre de vie pour pouvoir l'afficher depuis la scène parente"""

        if self.health < 0:
            self.health = 0

        if self.len >= self.max_health / 2:
            bar_color = self.parent.parent.parent.parent.parent.colors["GREEN"]
        elif self.len >= self.max_health / 4:
            bar_color = self.parent.parent.parent.parent.parent.colors["YELLOW"]
        else:
            bar_color = self.parent.parent.parent.parent.parent.colors["RED"]

        if int(self.health) < self.len:
            self.len -= 1
        elif int(self.health) > self.len:
            self.len += 1

        health_text = "%s/%s"%(self.len, self.max_health)
        self.parent.health_text = CreateText(screen, health_text, self.parent.parent.text_color, (len(health_text) * 15, 20), 0, (self.pos, "top"), (500 - len(health_text) * 15, 35), False, None)
        self.parent.health_bar_border = CreateRect(screen, self.parent.parent.parent.parent.parent.colors["BLACK"], (498, 28), (self.pos, "top"), (11, 56))
        self.parent.health_bar_bg = CreateRect(screen, self.parent.parent.parent.parent.parent.colors["DISCORD_DARK_GRAY"], (490, 20), (self.pos, "top"), (15, 60))
        self.parent.health_bar = CreateRect(screen, bar_color, (self.len * (490 / self.max_health), 20), (self.pos, "top"), (15, 60))

    def check_for_esquive(self):
        """Permet de générer une probabilité d'esquiver"""
        temp = random.randint(0, 100)
        if 0 <= temp < self.esquive:
            return True
        else:
            return False

    def check_for_coup_crit(self):
        """Permet de générer une probabilité d'infliger un coup critique"""
        temp = random.randint(0, 100)
        if 0 <= temp < self.coup_crit:
            return True
        else:
            return False