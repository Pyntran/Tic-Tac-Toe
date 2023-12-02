import pygame
import math
import random


class TicTacToe:
    def __init__(self):
        pygame.font.init()
        pygame.display.set_caption("Tic Tac Toe")
        self.WIDTH = 1080
        self.HEIGHT = 608
        self.SQUARE_SIZE = 200
        self.board = [['' for _ in range(3)] for _ in range(3)]
        self.player = 'X'
        self.game_over = False
        self.font = pygame.font.SysFont("comicsans", 100)
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.RED = (255, 0, 0)
        self.BLUE = (0, 0, 255)
        self.font = pygame.font.SysFont("comicsans", 100)
        self.gameD = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.grid_offset_x = (self.WIDTH - (self.SQUARE_SIZE * 3)) // 2
        self.grid_offset_y = (self.HEIGHT - (self.SQUARE_SIZE * 3)) // 2

    def draw_grid(self):
        for i in range(1, 3):
            pygame.draw.line(self.gameD, self.BLACK,
                             (self.grid_offset_x, i * self.SQUARE_SIZE + self.grid_offset_y),
                             (self.WIDTH - self.grid_offset_x, i * self.SQUARE_SIZE + self.grid_offset_y))
            pygame.draw.line(self.gameD, self.BLACK,
                             (i * self.SQUARE_SIZE + self.grid_offset_x, self.grid_offset_y),
                             (i * self.SQUARE_SIZE + self.grid_offset_x, self.HEIGHT - self.grid_offset_y))

    def draw_board(self):
        for row in range(3):
            for col in range(3):
                if self.board[row][col] != '':
                    text = self.font.render(self.board[row][col], True,
                                            self.BLACK if self.board[row][col] == 'X' else self.RED)
                    text_rect = text.get_rect(center=(
                        col * self.SQUARE_SIZE + self.grid_offset_x + self.SQUARE_SIZE // 2,
                        row * self.SQUARE_SIZE + self.grid_offset_y + self.SQUARE_SIZE // 2))
                    self.gameD.blit(text, text_rect)

    def check_winner(self):
        for row in range(3):
            if self.board[row][0] == self.board[row][1] == self.board[row][2] != '':
                return self.board[row][0]
        for col in range(3):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] != '':
                return self.board[0][col]
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != '':
            return self.board[0][0]
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != '':
            return self.board[0][2]
        return None

    def is_board_full(self):
        for row in range(3):
            for col in range(3):
                if self.board[row][col] == '':
                    return False
        return True

    def get_empty_cells(self):
        empty_cells = []
        for row in range(3):
            for col in range(3):
                if self.board[row][col] == '':
                    empty_cells.append((row, col))
        return empty_cells

    def minimax(self, board, depth, is_maximizing):
        winner = self.check_winner()

        if winner == 'O':
            return 1
        elif winner == 'X':
            return -1
        elif self.is_board_full():
            return 0

        if is_maximizing:
            best_score = -math.inf
            for row in range(3):
                for col in range(3):
                    if board[row][col] == '':
                        board[row][col] = 'O'
                        score = self.minimax(board, depth + 1, False)
                        board[row][col] = ''
                        best_score = max(score, best_score)
            return best_score
        else:
            best_score = math.inf
            for row in range(3):
                for col in range(3):
                    if board[row][col] == '':
                        board[row][col] = 'X'
                        score = self.minimax(board, depth + 1, True)
                        board[row][col] = ''
                        best_score = min(score, best_score)
            return best_score

    def ai_move(self):
        best_score = -math.inf
        best_move = None
        for row in range(3):
            for col in range(3):
                if self.board[row][col] == '':
                    self.board[row][col] = 'O'
                    if self.check_winner() == 'O':
                        return row, col
                    self.board[row][col] = ''

        for row in range(3):
            for col in range(3):
                if self.board[row][col] == '':
                    self.board[row][col] = 'X'
                    if self.check_winner() == 'X':
                        self.board[row][col] = 'O'
                        return row, col
                    self.board[row][col] = ''
        for row in range(3):
            for col in range(3):
                if self.board[row][col] == '':
                    self.board[row][col] = 'O'
                    score = self.minimax(self.board, 0, False)
                    self.board[row][col] = ''
                    if score > best_score:
                        best_score = score
                        best_move = (row, col)

        return best_move

    def play_game(self):
        pygame.init()
        pygame.display.set_caption("Tic Tac Toe")

        running = True
        while running:
            self.gameD.fill('#CCFFFF')
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if not self.game_over and self.player == 'X' and event.type == pygame.MOUSEBUTTONDOWN:
                    mouseX, mouseY = pygame.mouse.get_pos()
                    clicked_row = (mouseY - self.grid_offset_y) // self.SQUARE_SIZE
                    clicked_col = (mouseX - self.grid_offset_x) // self.SQUARE_SIZE

                    if (0 <= clicked_row < 3) and (0 <= clicked_col < 3) and self.board[clicked_row][clicked_col] == '':
                        self.board[clicked_row][clicked_col] = 'X'
                        self.player = 'O'

            if self.is_board_full():
                text = self.font.render("TIE!", True, self.BLUE)
                self.gameD.blit(text, (self.WIDTH // 2 - 150, self.HEIGHT // 2 - 50))
                self.game_over = True

            empty_cell = self.get_empty_cells()
            if len(empty_cell) == (3 * 3 - 1):
                ai_row, ai_col = random.choice(empty_cell)
                self.board[ai_row][ai_col] = 'O'
                self.player = 'X'

            self.draw_grid()
            self.draw_board()

            winner = self.check_winner()
            if winner:
                text = self.font.render(f"{winner} wins!", True, self.BLUE)
                self.gameD.blit(text, (self.WIDTH // 2 - 150, self.HEIGHT // 2 - 50))
                self.game_over = True

            if not self.game_over and self.player == 'O':
                ai_row, ai_col = self.ai_move()
                self.board[ai_row][ai_col] = 'O'
                self.player = 'X'
            pygame.display.update()
        pygame.quit()
