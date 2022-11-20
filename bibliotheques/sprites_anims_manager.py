from bibliotheques.create_image import CreateImage

class SpritesAnimsManager:
    """Permet de gérer les animations d'un sprite"""

    def __init__(self, parent):
        """Constantes"""
        self.parent = parent

        """Variables"""
        self.reset_anims()

    def reset_anims(self):
        """Remet à 0 les animations (pour un nouveau combat)"""
        self.current_anim = []
        self.current_frame = 1
        self.anims_liste = []
        self.end = False

    def create_new_anim(self, name, patron_path, frame_size, nb_frames, fps, loop):
        """Crée une nouvelle animation"""
        self.anims_liste.append([name, patron_path, frame_size, nb_frames, fps, loop])

    def set_current_anim(self, name):
        """Change l'animation que le sprite doit jouer"""
        for i in range(0, len(self.anims_liste)):
            if self.anims_liste[i][0] == name:
                self.current_anim = self.anims_liste[i]
        if not self.current_anim[5]:
            self.current_frame = 1
        self.end = False

    def set_frame(self, screen):
        """Met à jour la frame en fonction de l'animation actuelle"""

        self.current_frame += self.current_anim[4] / 60

        if int(self.current_frame) > self.current_anim[3] and self.end == False:
            if self.current_anim[5]:
                self.current_frame -= self.current_anim[3]
            else:
                self.end = True

        if not self.end:
            width = self.parent.sprite.rect.w
            self.parent.sprite = CreateImage(screen, self.current_anim[1]%int(self.current_frame), (self.current_anim[2][0] * 4, self.current_anim[2][1] * 4), 0, 100, (self.parent.sprite.rect.x, self.parent.sprite.rect.y), (0, 0))
            if self.parent.flip:
                self.parent.sprite.rect.x -= self.parent.sprite.rect.w - width
            self.parent.sprite.flip_image(self.parent.flip, False)