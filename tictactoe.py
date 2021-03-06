import random

class Board:
    def __init__(self):
        self.board = [[None] * 3 for _ in range(3)]

    def render(self):
        rendList = [["  0 1 2"], [" -------"]]
        rlapp = rendList.append
        for i, b in enumerate(self.board):
            temp = (
                str(i)
                + "|"
                + (b[0] if b[0] else " ")
                + " "
                + (b[1] if b[1] else " ")
                + " "
                + (b[2] if b[2] else " ")
                + "|"
            )
            rlapp([temp])
        rlapp([" -------"])
        print("\n".join(["".join(a) for a in rendList]))

    def is_coord_empty(self, coord):
        return not self.board[coord[0]][coord[1]]

    @staticmethod
    def is_empty(board):
        return not any(any(_) for _ in board)

    @staticmethod
    def is_full(board):
        return all(all(_) for _ in board)

    @staticmethod
    def is_win(board):
        if (
            board[0][0]
            and board[0][0] == board[1][1] == board[2][2]
        ):
            return board[0][0]
        elif (
            board[2][0]
            and board[2][0] == board[1][1] == board[0][2]
        ):
            return board[2][0]

        for i in range(3):
            if (
                board[i][0]
                and board[i][0] == board[i][1] == board[i][2]
            ):
                return board[i][0]
            elif (
                board[0][i]
                and board[0][i] == board[1][i] == board[2][i]
            ):
                return board[0][i]

        return False

    @staticmethod
    def get_legal_moves(board):
        return [(i, j) for i, a in enumerate(board) for j, b in enumerate(a) if not b]


class Game:
    def __init__(self, player, first):
        self.board = Board()
        self.win = None
        self.draw = False
        self.board.render()
        self.playerId = player if player != "" else "X"
        self.aiId = "X" if player == "O" else "O"
        self.playerTurn = first in "Y"
        self.coords = ("0", "1", "2")
    def get_move(self):
        while 1:
            x = input("What is your move's X co-ordinate?: ").strip()
            while x not in self.coords:
                print("Invalid co-ordinate")
                x = input("What is your move's X co-ordinate?: ").strip()
            y = input("What is your move's Y co-ordinate?: ").strip()
            while y not in self.coords:
                print("Invalid co-ordinate")
                y = input("What is your move's Y co-ordinate?: ").strip()

            if self.board.is_coord_empty((int(y), int(x))):
                break
            print(f"Can't make move ({x}, {y}), square already taken!")
        return (int(y), int(x))

    def make_move(self, board, coord, c):
        new_board = [x[:] for x in board]
        new_board[coord[0]][coord[1]] = c
        return new_board

    @staticmethod
    def get_opponent(player):
        return "X" if player == "O" else "O"

    def minimax_ai(self, board, whoami):
        best_move = None
        best_score = None
        if self.board.is_empty(board):
            return random.choice(self.board.get_legal_moves(board))
        mkmv = self.make_move
        getop = self.get_opponent
        mmaxscr = self.minimax_score
        for move in self.board.get_legal_moves(board):
            b = [x[:] for x in board]
            b = mkmv(b, move, whoami)
            opponent = getop(whoami)
            score = mmaxscr(b, opponent, whoami)
            if best_score is None or score > best_score:
                best_move = move
                best_score = score

        return best_move

    def minimax_score(self, board, curr, ai):
        winner = self.board.is_win(board)
        if winner:
            return +10 if winner == ai else -10
        elif self.board.is_full(board):
            return 0
        legal_moves = self.board.get_legal_moves(board)
        scores = []
        mkmv = self.make_move
        getop = self.get_opponent
        mmaxscr = self.minimax_score
        scapp = scores.append
        for move in legal_moves:
            new_board = mkmv(board, move, curr)
            opponent = getop(curr)
            score = mmaxscr(new_board, opponent, ai)
            scapp(score)
        return max(scores) if curr == ai else min(scores)

    def update(self):
        print(f"{self.playerId if self.playerTurn else self.aiId}'s turn...")
        if self.playerTurn:
            self.board.board = self.make_move(
                self.board.board, self.get_move(), self.playerId
            )
            self.playerTurn = False
        else:
            aiMove = self.minimax_ai(self.board.board, self.aiId)
            self.board.board = self.make_move(
                self.board.board, aiMove, self.aiId
            )
            self.playerTurn = True
        winner = self.board.is_win(self.board.board)
        if winner:
            self.board.render()
            print(f"The winner is {winner}")
            self.win = winner
        elif self.board.is_full(self.board.board):
            self.board.render()
            print("It's a draw !")
            self.draw = True
        else:
            self.board.render()


def play():
    player = input("Which side are you?(X/O) ").upper().strip()
    while player not in "XO":
        print("Invalid input !")
        player = input("Which side are you?(X/O) ").upper().strip()
    first = input("Want to play first?(y/n) ").upper().strip()
    while first not in "YN":
        print("Invalid input !")
        first = input("Want to play first?(y/n) ").upper().strip()
    game = Game(player, first)
    while not game.win and not game.draw:
        game.update()
    
    if game.win == game.playerId:
        print("Impossible...")
    elif game.win == game.aiId:
        print("Haha loser")

    return main()


def main():
    print("<---Welcome to the Perfect TicTacToe--->")
    ans = input("Shall we begin?(y/n) ").upper().strip()
    while ans not in "YN":
        print("Invalid input !")
        ans = input("Shall we begin?(y/n) ").upper().strip()

    play() if ans in "Y" else print("Bye !")


if __name__ == "__main__":
    main()
