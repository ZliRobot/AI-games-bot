import numpy as np
import matplotlib.pyplot as plt
import subprocess
import did_he_win as dhw


# transform matrix to string to communicate with bot like engine 
def mat2str(board):
    a = board
    s = repr(a).replace('array', '')
    s = s.replace(']]', '')
    s = s.replace('],', ';')
    s = ''.join([c for c in s if c not in ('(', ')', '[', ']', '\n', ' ')])
    return s


# communicate with bot to play move
def player_play(player_id, i_round, board, t_move):
    if player_id == 1:
        player = player1
    else:
        player = player2

    player.stdin.write("update game round %i\n" % i_round)
    player.stdin.write("update game field %s\n" % mat2str(board))
    player.stdin.write("action move %i\n" % t_move)
    return player.stdout.readline()


# starting settings, sent at the beginning of game
def start_string(player_id):
    return ("settings timebank 10000\n"
            "settings time_per_move 500\n"
            "settings player_names player1,player2\n"
            "settings your_bot player%c\n"
            "settings your_botid %c\n"
            "settings field_columns 7\n"
            "settings field_rows 6\n" % (str(player_id), str(player_id)))


# updates board after move
def board_update(board, move, player_id):
    if 0 != board[0, int(move.split()[1])]:
        print "test.py: Error - full column"

    raw = board.shape[0] - 1

    while board[raw, move.split()[1]] != 0:
        raw -= 1

    board[raw, move.split()[1]] = player_id
    return board


# run bots and open communication
def bot_init(filename):
    player = subprocess.Popen("python %s" % filename,
                           shell=True,
                           stdout=subprocess.PIPE,
                           stdin=subprocess.PIPE,
                           stderr=subprocess.STDOUT)
    return player

# main - test behaviour
i_round = 1
t_move = 1000
show_moves = 1

player1 = bot_init("main_rnd.py")
player2 = bot_init("main.py")
board = np.zeros((6, 7), dtype=np.int)

player1.stdin.write(start_string(1))
player2.stdin.write(start_string(2))

for i_round in range(1, 43):

    player_id = 2 - i_round % 2
    move = player_play(player_id, i_round, board, t_move).rstrip()
    board = board_update(board, move, player_id)
    if show_moves:
        print move
        plt.imshow(board, interpolation="nearest")
        plt.show(block=False)
        plt.pause(0.3)
    if dhw.did_he_win(board, player_id):
        print "player %i win" % player_id
        break


print("round %i" % i_round)
player1.kill()
player2.kill()
plt.ioff()
plt.show()
