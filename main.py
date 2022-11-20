import pygame
import os
from bibliotheques.create_text import CreateText
from scenes.menu_scene import MenuScene

"""Création de la fenêtre"""
pygame.init()
pygame.display.set_caption("Un jeu de NSI plutôt cool :)")
os.environ['SDL_VIDEO_WINDOW_POS']="0,30"
pygame.display.set_icon(pygame.image.load("assets/gui/icons/icon.png"))
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()

"""Création des constantes"""
colors = {"DARK_GOLD"          : (154, 122,  37),
          "BLACK"              : (  0,   0,   0),
          "WHITE"              : (255, 255, 255),
          "DISCORD_LIGHT_GRAY" : ( 90,  93,  90),
          "DISCORD_GRAY"       : ( 60,  63,  60),
          "DISCORD_DARK_GRAY"  : ( 30,  33,  30),
          "GREEN"              : (111, 210,  46),
          "YELLOW"             : (210, 200,  46),
          "RED"                : (210,  46,  46)}


"""Création de la première scène"""
menu_scene = MenuScene(screen, colors)

"""Boucle principale du jeu"""
while True:

    menu_scene.blit_scene(screen)
    menu_scene.action(screen)

    dt = clock.tick(60)
    menu_scene.dt = dt

    if menu_scene.show_fps and menu_scene.battle_mode_scene.select_character_scene.fight_scene.blit:
        dt= round(1000/dt)
        txtFps = CreateText(screen, "%s FPS"%int(dt), colors["DARK_GOLD"], ((6 + len(str(int(dt)))) * 10, 20), 0, ("right", "bottom"), (5, 5), False, None)
        txtFps.blit(screen)

    pygame.display.flip()