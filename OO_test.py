import numpy as np
import matplotlib.pyplot as plt
import subprocess
from did_he_win import did_he_win
import time
import os
start_time = time.time()


class Player(object):

    show_moves = 0
    i_round = 1
    t_move = 1000
    board = np.zeros((6, 7), dtype=np.uint8)

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
            print "test_OO.py: Error - full column"

        raw = cls.board.shape[0] - 1
        while cls.board[raw, column] != 0:
            raw -= 1

        cls.board[raw, column] = player_id
        if cls.show_moves == "yes":
            cls.display_board(cls.board, column, player_id)

    @classmethod
    def display_board(cls, new_board, column, player_id):
        # display board

        print column
        plt.imshow(cls.board, interpolation="nearest")
        plt.show(block=False)
        plt.pause(0.3)

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
            result = self.input_method.stdout.readline()
            if len(result) < 250:
                return result
            else:
                for line in range(1, 20):
                    print result
                    result = self.input_method.stdout.readline()
                return -1
        else:
            input_column = input("Column:")
            check = "wrong"
            while check != "ok":
                if 0 <= input_column < self.board.shape[1]:
                    if self.board[0, input_column] == 0:
                        check = "ok"
                else:
                    print "Number of column must be in range 0-6, column must have at last one free space"
                    input_column = input("Column:")

            return "place_disc %s" % input_column

# main - test behaviour
num_of_games = 10
wins1 = 0
wins2 = 0
rounds = 0.0
Player.show_moves = "no"
player1 = Player(1, type="bot", filename="main_search.py")
player2 = Player(2, type="bot", filename="main_rnd.py")


for game_num in range(0, num_of_games):
    Player.reset_board()

    if Player.show_moves == "yes":
        Player.display_board(Player.board, 0, 0)

    for Player.i_round in range(1, 43):

        player_id = 2 - (Player.i_round + game_num) % 2
        if player_id == 1:
            curr_player = player1
        else:
            curr_player = player2

        move = curr_player.player_play().rstrip()
        Player.board_update(move, player_id)

        if did_he_win(Player.board, player_id, int(move.split()[1])):
            print "Game %i: player %i win" % (game_num, player_id)
            if player_id == 1:
                wins1 += 1
                if Player.show_moves == "yes":
                    os.system('say "Human wins"')
            elif player_id == 2:
                wins2 += 1
                if Player.show_moves == "yes":
                    os.system('say "Computer wins"')
            rounds += Player.i_round
            break
        if Player.i_round == 42:
            print "Game %i: Draw" % game_num

print "player1 won %i times" % wins1
print "player2 won %i times" % wins2
print "%.2f rounds average" % (rounds/num_of_games)

if player1.type == "bot":
    player1.input_method.kill()
if player2.type == "bot":
    player2.input_method.kill()
plt.ioff()
plt.show()

print "time elapsed: {:.2f}s".format(time.time() - start_time)

os.system('say "your program has finished"')
