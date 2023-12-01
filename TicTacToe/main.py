import pygame
import sys
from tictactoe import TicTacToe
from button import Button
from client import Client


pygame.init()

WIDTH = 1080
HEIGHT = 608


pygame.display.set_caption("Tic Tac Toe")

gameD = pygame.display.set_mode((WIDTH, HEIGHT))
menu_screen = pygame.image.load("assets/menu.png")


def get_font(size):
    return pygame.font.Font("assets/font.ttf", size)


def single_player():
    play = TicTacToe()
    play.play_game()


def main_menu():
    while True:
        gameD.blit(menu_screen, (0, 0))
        MENU_MOUSE_POS = pygame.mouse.get_pos()

        SINGLEPLAYER_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(160, 550),
                                     text_input="SinglePlayer", font=get_font(20), base_color="#339966",
                                     hovering_color="White")
        MULTIPLAYER_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(450, 550),
                                    text_input="2 Player", font=get_font(20), base_color="#0099CC",
                                    hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(740, 550),
                             text_input="QUIT", font=get_font(20), base_color="#FF6699", hovering_color="White")

        for button in [SINGLEPLAYER_BUTTON, MULTIPLAYER_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(gameD)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if SINGLEPLAYER_BUTTON.checkForInput(MENU_MOUSE_POS):
                    single_player()
                if MULTIPLAYER_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play = Client()
                    play.run()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()


main_menu()
