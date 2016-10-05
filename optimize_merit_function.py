import numpy as np
import matplotlib.pyplot as plt
import subprocess
import did_he_win as dhw
import multiprocessing
import time
start_time = time.time()


class Player(object):

    show_moves = 0
    i_round = 1
    t_move = 1000
    board = np.zeros((6, 7), dtype=np.uint8)
    wins1 = 0
    wins2 = 0
    total_rounds = 0.0

    def __init__(self, player_id, type="bot", filename="main.py"):
        self.type = type
        self.filename = filename
        self.player_id = player_id
        if self.type == "bot":
            self.input_method = self.bot_init()
            self.input_method.stdin.write(self.start_string())

    # transform matrix to string to communicate with bot like engine
    @classmethod       # applies to board, independently of player
    def mat2str(cls):
        a = cls.board
        s = repr(a).replace('array', '')
        s = s.replace(']]', '')
        s = s.replace('],', ';')
        s = ''.join([c for c in s if c not in ('(', ')', '[', ']', '\n', ' ')])
        return s[:2 * a.size - 1]

    # updates board after move
    @classmethod
    def board_update(cls, move, player_id):
        column = move.split()[1]

        if 0 != cls.board[0, column]:
            print "test.py: Error - full column"

        raw = cls.board.shape[0] - 1
        new_board = np.copy(cls.board)
        while new_board[raw, column] != 0:
            raw -= 1

        new_board[raw, column] = player_id
        cls.display_board(new_board, column, player_id)

    @classmethod
    def display_board(cls, new_board, column, player_id):
        # display board

        if cls.show_moves == "yes":
            print column
            cls.board = new_board
            plt.imshow(cls.board, interpolation="nearest")
            plt.show(block=False)
            plt.pause(0.3)
        elif cls.show_moves == "animate":
            print column
            temp_board = np.copy(cls.board)
            temp_board[0, column] = player_id
            plt.imshow(temp_board, interpolation="nearest")
            plt.show(block=False)
            plt.pause(0.01)
            raw = 1
            while raw < temp_board.shape[0] and temp_board[raw, column] == 0:
                temp_board[raw - 1, column] = 0
                temp_board[raw, column] = player_id
                plt.imshow(temp_board, interpolation="nearest")
                plt.pause(0.00001)
                raw += 1
            cls.board = new_board
        else:
            cls.board = new_board

    @classmethod
    def reset_board(cls):
        cls.board = np.zeros((6, 7), dtype=np.uint8)

    # run bot and open communication
    def bot_init(self):
        input_method = subprocess.Popen("python %s" % self.filename,
                                        shell=True,
                                        stdout=subprocess.PIPE,
                                        stdin=subprocess.PIPE,
                                        stderr=subprocess.STDOUT)
        return input_method

    # starting settings, sent at the beginning of game
    def start_string(self):
        return ("settings timebank 10000\n"
                "settings time_per_move 500\n"
                "settings player_names player1,player2\n"
                "settings your_bot player%c\n"
                "settings your_botid %c\n"
                "settings field_columns 7\n"
                "settings field_rows 6\n" % (str(self.player_id), str(self.player_id)))

    # communicate with bot to play move
    def player_play(self):
        if self.type == "bot":
            self.input_method.stdin.write("update game round %i\n" % self.i_round)
            self.input_method.stdin.write("update game field %s\n" % self.mat2str())
            self.input_method.stdin.write("action move %i\n" % self.t_move)
            return self.input_method.stdout.readline()
        else:
            input_column = input("Column:")
            while input_column not in range(0, self.board.shape[1]) and self.board[0,input_column] != 0:
                print "Number of column must be in range 0-6, column must have at last one free space"
                input_column = input("Column:")

            return "place_disc %s" % input_column


def run_oo_test(game_num):

    Player.reset_board()

    for Player.i_round in range(1, 43):

        player_id = 2 - (Player.i_round + game_num) % 2
        if player_id == 1:
            curr_player = player1
        else:
            curr_player = player2

        move = curr_player.player_play().rstrip()
        Player.board_update(move, player_id)

        if dhw.did_he_win(Player.board, player_id, int(move.split()[1])):
            print "Game %i: player %i win" % (game_num, player_id)
            if player_id == 1: Player.wins1 += 1
            if player_id == 2: Player.wins2 += 1
            Player.total_rounds += Player.i_round
            break

if __name__ == '__main__':

    # main - test behaviour
    num_of_games = 100
    Player.show_moves = "no"
    player1 = Player(1, type="bot", filename="main_rnd.py")
    player2 = Player(2, type="bot", filename="main.py")
    Player.display_board(Player.board, 0, 0)

    for game in range(0, num_of_games):
        run_oo_test(game)

    print "player1 won %i times" % Player.wins1
    print "player2 won %i times" % Player.wins2
    print "%.2f rounds average" % (Player.total_rounds/num_of_games)

    if player1.type == "bot":
        player1.input_method.kill()
    if player2.type == "bot":
        player2.input_method.kill()
    plt.ioff()
    plt.show()

    print "time elapsed: {:.2f}s".format(time.time() - start_time)
    #  beep at the end
    import os
    os.system('say -v "Whisper" "your program has finished"')
