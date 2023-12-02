import pygame
from network import Network
from button import Button
import sys


def get_font(size):
    return pygame.font.Font("assets/font.ttf", size)


class Client:
    def __init__(self):
        pygame.init()
        pygame.font.init()

        self.WIDTH = 1080
        self.HEIGHT = 608
        self.gameD = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Client")
        self.SQUARE_SIZE = 200
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.RED = (255, 0, 0)
        self.BLUE = (0, 0, 255)
        self.grid_offset_x = (self.WIDTH - (self.SQUARE_SIZE * 3)) // 2
        self.grid_offset_y = (self.HEIGHT - (self.SQUARE_SIZE * 3)) // 2
        self.font = pygame.font.SysFont("comicsans", 100)

        # Initialize buttons
        self.PLAY_AGAIN = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(120, 500),
                                 text_input="PLAY AGAIN", font=get_font(20), base_color="#0099CC",
                                 hovering_color="White")
        self.QUIT_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(950, 500),
                                  text_input="QUIT", font=get_font(20), base_color="#FF6699",
                                  hovering_color="White")

    def draw_grid(self):
        for i in range(1, 3):
            pygame.draw.line(self.gameD, self.BLACK,
                             (self.grid_offset_x, i * self.SQUARE_SIZE + self.grid_offset_y),
                             (self.WIDTH - self.grid_offset_x, i * self.SQUARE_SIZE + self.grid_offset_y))
            pygame.draw.line(self.gameD, self.BLACK,
                             (i * self.SQUARE_SIZE + self.grid_offset_x, self.grid_offset_y),
                             (i * self.SQUARE_SIZE + self.grid_offset_x, self.HEIGHT - self.grid_offset_y))

    def draw_board(self, game):
        for row in range(3):
            for col in range(3):
                if game.board[row][col] != '':
                    text = self.font.render(game.board[row][col], True,
                                            self.BLACK if game.board[row][col] == 'X' else self.RED)
                    text_rect = text.get_rect(center=(
                        col * self.SQUARE_SIZE + self.grid_offset_x + self.SQUARE_SIZE // 2,
                        row * self.SQUARE_SIZE + self.grid_offset_y + self.SQUARE_SIZE // 2))
                    self.gameD.blit(text, text_rect)

    def redrawwindow(self, gameD, game, player):
        gameD.fill('#CCFFFF')
        font = pygame.font.SysFont("comicsans", 80)
        if not (game.connected()):
            text = font.render("Waiting for Player...", 1, (255, 0, 0), True)
            gameD.blit(text, (self.WIDTH / 2 - text.get_width() / 2, self.HEIGHT / 2 - text.get_height() / 2))
        else:
            self.draw_grid()
            self.draw_board(game)
            if not game.game_over():
                if game.current_player == player:
                    font = pygame.font.SysFont("comicsans", 25)
                    text = font.render("Your Move", 1, '#0099CC')
                    gameD.blit(text, (50, self.HEIGHT / 2))
                else:
                    font = pygame.font.SysFont("comicsans", 25)
                    text = font.render("Opponent's Move", 1, "#FF6699")
                    gameD.blit(text, (850, self.HEIGHT / 2))
            else:
                if game.game_over():
                    for button in [self.PLAY_AGAIN, self.QUIT_BUTTON]:
                        pos = pygame.mouse.get_pos()
                        button.changeColor(pos)
                        button.update(gameD)

                winner = game.check_winner()
                if winner:
                    if winner == 'X':
                        if player == 0:
                            text = font.render("YOU WON!", True, self.BLUE)
                        else:
                            text = font.render("YOU LOST!", True, self.BLUE)
                        gameD.blit(text, (
                            self.WIDTH / 2 - text.get_width() / 2, self.HEIGHT / 2 - text.get_height() / 2))
                    else:
                        if player == 1:
                            text = font.render("YOU WON!", True, self.BLUE)
                        else:
                            text = font.render("YOU LOST!", True, self.BLUE)
                        gameD.blit(text, (
                            self.WIDTH / 2 - text.get_width() / 2, self.HEIGHT / 2 - text.get_height() / 2))

                else:
                    text = font.render("TIE!", True, self.BLUE)
                    gameD.blit(text, (self.WIDTH / 2 - text.get_width() / 2, self.HEIGHT / 2 - text.get_height() / 2))

        pygame.display.update()

    def run(self):
        run = True
        clock = pygame.time.Clock()
        n = Network()
        player = int(n.getP())
        print("You are player", player)

        while run:
            clock.tick(60)
            try:
                game = n.send("get")
            except:
                run = False
                print("Couldn't get game")
                break

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()
                if not game.game_over() and game.current_player == player:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        pos = pygame.mouse.get_pos()
                        clicked_row = (pos[1] - self.grid_offset_y) // self.SQUARE_SIZE
                        clicked_col = (pos[0] - self.grid_offset_x) // self.SQUARE_SIZE

                        if (0 <= clicked_row < 3) and (0 <= clicked_col < 3):
                            move_location = str(clicked_row * 3 + clicked_col)
                            game.make_move(clicked_row * 3 + clicked_col)
                            n.send(move_location)
                if game.game_over():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        pos = pygame.mouse.get_pos()
                        if self.PLAY_AGAIN.checkForInput(pos):
                            game = n.send("reset")
                        if self.QUIT_BUTTON.checkForInput(pos):
                            pygame.quit()
                            sys.exit()

            self.redrawwindow(self.gameD, game, player)

    def menu_screen(self):
        run = True
        clock = pygame.time.Clock()

        while run:
            clock.tick(60)
            self.gameD.fill('#CCFFFF')
            font = pygame.font.SysFont("comicsans", 60)
            text = font.render("Click to Play!", 1, (255, 0, 0))
            self.gameD.blit(text, (100, 200))
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    run = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    run = False

        self.run()
