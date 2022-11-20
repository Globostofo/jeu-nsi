import pygame

class InputManager:
    """Gère les inputs du joueur"""

    def __init__(self):
        self.pressed = {}

    def check_inputs(self):
        """Retourne la liste de tous les événements de la frame (leur type ainsi que leur valeur)"""

        event_info = []

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            elif event.type == pygame.KEYDOWN:
                event_info.append(["keydown", event.key, event.unicode])
                self.pressed[event.key] = 1

            elif event.type == pygame.KEYUP:
                event_info.append(["keyup", event.key])
                self.pressed[event.key] = 0

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                event_info.append(["leftclickdown", event.pos])

        return event_info