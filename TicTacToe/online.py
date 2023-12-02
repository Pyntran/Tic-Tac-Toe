class Game:
    def __init__(self, id):
        self.ready = False
        self.id = id
        self.board = [['' for _ in range(3)] for _ in range(3)]
        self.current_player = 0

    def is_board_full(self):
        for row in range(3):
            for col in range(3):
                if self.board[row][col] == '':
                    return False
        return True

    def game_over(self):
        winner = self.check_winner()
        if self.is_board_full() or winner:
            return True
        return False

    def reset_game(self):
        self.board = [['' for _ in range(3)] for _ in range(3)]

    def connected(self):
        return self.ready

    def make_move(self, move):
        row = move // 3
        col = move % 3
        if self.board[row][col] == '':
            self.board[row][col] = 'X' if self.current_player == 0 else 'O'
            self.current_player = 1 - self.current_player

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

