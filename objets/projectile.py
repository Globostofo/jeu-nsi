import pygame
from bibliotheques.create_image import CreateImage

class Projectile():
    """Objet que gère la balle pendant un combat"""

    def __init__(self, screen, parent, spawn_pos):
        """Constantes"""
        self.parent = parent
        self.nbr_retours = 0

        """Variables"""
        self.set_new_speed()

        if spawn_pos == "middle":
            self.sprite = CreateImage(screen, "assets/balle.png", (50, 50), 0, 100, ("center", "center"), (0, -100))
        elif spawn_pos == "left":
            self.sprite = CreateImage(screen, "assets/balle.png", (50, 50), 0, 100, ("center", "center"), (-100, -100))
        elif spawn_pos == "right":
            self.sprite = CreateImage(screen, "assets/balle.png", (50, 50), 0, 100, ("center", "center"), (100, -100))

        """Sons de l'objet"""
        self.sound_hit_ball = pygame.mixer.Sound("assets/sounds/hit_ball.wav")

    def move(self, screen):
        """Déplace l'objet"""

        self.sprite.rect.x += self.velocity.x
        if self.sprite.rect.x < 0 or self.sprite.rect.x + self.sprite.rect.w > screen.get_width() or self.parent.check_collision(self.sprite, self.parent.filet):
            self.velocity.x *= -1
            self.sprite.rect.x += self.velocity.x

        self.sprite.rect.y += self.velocity.y
        self.velocity.y += 0.5
        if self.sprite.rect.y < 0 or self.parent.check_collision(self.sprite, self.parent.filet):
            self.velocity.y *= -0.8
            self.sprite.rect.y += self.velocity.y
        elif self.sprite.rect.y >= 720 - self.sprite.rect.h:
            if self.sprite.rect.x < screen.get_width() / 2:
                self.parent.init_end_point(screen, "left")
            elif self.sprite.rect.x > screen.get_width() / 2:
                self.parent.init_end_point(screen, "right")

    def set_new_velocity(self, player_attack_key):
        """Permet de modifier la trajectoire de la balle"""

        if self.parent.check_collision(self.sprite, self.parent.left_part.player.sprite) and player_attack_key == 32:
            self.parent.phase = "combat"
            self.nbr_retours += 1
            self.set_new_speed()

            pivot = (self.parent.left_part.player.sprite.rect.x, self.parent.left_part.player.sprite.rect.y + self.parent.left_part.player.sprite.rect.h / 2)

            deltaX = (self.sprite.rect.x - pivot[0])
            deltaY = (self.sprite.rect.y - pivot[1])

            vel = pygame.math.Vector2(deltaX, deltaY)
            vel = vel.normalize()
            self.velocity = pygame.math.Vector2(vel.x * self.speed * self.parent.left_part.player.hit_speed, vel.y * self.speed * self.parent.left_part.player.hit_speed)

            if self.parent.parent.parent.parent.sounds:
                self.sound_hit_ball.play()

        if self.parent.check_collision(self.sprite, self.parent.right_part.player.sprite) and player_attack_key == pygame.K_n:
            self.parent.phase = "combat"
            self.nbr_retours += 1
            self.set_new_speed()

            pivot = (self.parent.right_part.player.sprite.rect.x + self.parent.right_part.player.sprite.rect.w, self.parent.right_part.player.sprite.rect.y + self.parent.right_part.player.sprite.rect.h / 2)

            deltaX = (self.sprite.rect.x - pivot[0])
            deltaY = (self.sprite.rect.y - pivot[1])

            vel = pygame.math.Vector2(deltaX, deltaY)
            vel = vel.normalize()
            self.velocity = pygame.math.Vector2(vel.x * self.speed, vel.y * self.speed)

            if self.parent.parent.parent.parent.sounds:
                self.sound_hit_ball.play()

    def set_new_speed(self):
        """Permet d'augmenter la vitesse de la balle selon la suite croissante qui converge (très) lentement vers 35 et de premier terme u(0) = 15 : u(n) = (-50000 / (x+50)²) + 35"""
        self.speed = (-50000 / (self.nbr_retours + 50) ** 2) + 35