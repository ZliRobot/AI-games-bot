#---------------------------------------------------------------------#
# Zli Robot by Dusan                                                  #
# ============                                                        #
# Last update: 26 Sep 2016                                            #
# plays random, wins when 3 in raw, avoids to loose when 3 in raw     #
#                                                                     #
# Based on:                                                           #
# Four In A Row AI Challenge - Starter Bot                            #
# @author Lukas Knoepfel <shylux@gmail.com>                           #
# @version 1.0                                                        #
# @license MIT License (http://opensource.org/licenses/MIT)           #
#---------------------------------------------------------------------#

from sys import stdin, stdout
import numpy as np
import random
import time
import did_he_win as dhw
import count_open_segmets as cs

class Bot(object):

    settings = dict()
    round = -1
    board = np.zeros((6, 7), dtype=np.uint8)  # Access with [row_nr, col_nr]. [0,0] is on the top left.
    timeout = -1

    @property
    def make_turn(self):
        """ This method is for calculating and executing the next play.
            Make the play by calling place_disc exactly once.
        """
        # if play first, start in the middle
        if np.count_nonzero(self.board) == 0:
            self.place_disc(self.board.shape[1] / 2, "middle")
            return 1

        # win if possible
        for try_column in range(0,self.board.shape[1]):
            if 0 == self.board[0, try_column]:
                new_board = self.simulate_place_disc(self.board, try_column, self.id())
                if dhw.did_he_win(new_board, self.id()):
                    self.place_disc(try_column, "win")
                    return 1

        # don't loose if in danger
        for try_column in range(0, self.board.shape[1]):
            if 0 == self.board[0,try_column]:
                new_board = self.simulate_place_disc(self.board, try_column, 3 - self.id())
                if dhw.did_he_win(new_board, 3 - self.id()):
                    self.place_disc(try_column, "don't loose")
                    return 1

        # don't fall in trap!
        forbidden_columns = []
        for try_column in range(0, self.board.shape[1]):
            if 0 == self.board[0,try_column]:
                new_board = self.simulate_place_disc(self.board, try_column, self.id())         # my move
                new_board = self.simulate_place_disc(new_board, try_column, 3 - self.id())      # enemy move
                if dhw.did_he_win(new_board, 3 - self.id()):
                    forbidden_columns.append(try_column)

        # don't ruin my trap
        less_forbidden_columns = []
        for try_column in range(0, self.board.shape[1]):
            if 0 == self.board[0,try_column]:
                new_board = self.simulate_place_disc(self.board, try_column, 3 - self.id())         # 'my' move
                new_board = self.simulate_place_disc(new_board, try_column, self.id())              # my move
                if dhw.did_he_win(new_board, self.id()):
                    if try_column not in forbidden_columns:
                        less_forbidden_columns.append(try_column)

        # allow forbidden columns if no other choice
        if np.count_nonzero(self.board[0, :]) == self.board.shape[1] - (len(forbidden_columns) + len(less_forbidden_columns)):
            if 0 != len(less_forbidden_columns):
                less_forbidden_columns = []     # ruin your trap
            else:
                forbidden_columns = []      # loose

        # maximize merit function
        merit_function = np.ones(self.board.shape[1]) * (-1E100)
        for try_column in range(0,self.board.shape[1]):
            if try_column not in forbidden_columns \
                            and try_column not in less_forbidden_columns \
                            and self.board[0,try_column] == 0:
                new_board = self.simulate_place_disc(self.board, try_column, self.id())
                merit_function[try_column] = cs.merit_function(new_board, self.id())

        if np.nonzero(merit_function) == 0:     # merit function useless, play randomly
            rannum = random.randrange(7)
            while 0 != self.board[0, rannum] or rannum in forbidden_columns or rannum in less_forbidden_columns:
                rannum = random.randrange(7)
            self.place_disc(rannum, "random")
            return 1
        else:
            self.place_disc(np.argmax(merit_function), "max merit")
            return 1

    def place_disc(self, column, message):
        """ Writes your next play in stdout. """
        stdout.write("place_disc %d %s\n" % (column, message))
        stdout.flush()

    def simulate_place_disc(self, board, col_nr, curr_player):
        """ Returns a board state after curr_player placed a disc in col_nr.
            This is a simulation and doesn't update the actual playing board. """
        if board[0, col_nr] != 0:
            return board
        new_board = np.copy(board)
        for row_nr in reversed(range(self.rows())):
            if new_board[row_nr, col_nr] == 0:
                new_board[row_nr, col_nr] = curr_player
                return new_board

    def id(self):
        """ Returns own bot id. """
        return self.settings['your_botid']

    def rows(self):
        """ Returns amount of rows. """
        return self.settings['field_rows']

    def cols(self):
        """ Returns amount of columns. """
        return self.settings['field_columns']

    def current_milli_time(self):
        """ Returns current system time in milliseconds. """
        return int(round(time.time() * 1000))

    def set_timeout(self, millis):
        """ Sets time left until timeout in milliseconds. """
        self.timeout = self.current_milli_time() + millis

    def time_left(self):
        """ Get how much time is left until a timeout. """
        return self.timeout - self.current_milli_time()

    def run(self):
        """ Main loop.
        """
        while not stdin.closed:
            try:
                rawline = stdin.readline()

                # End of file check
                if len(rawline) == 0:
                    break

                line = rawline.strip()

                # Empty lines can be ignored
                if len(line) == 0:
                    continue

                parts = line.split()

                command = parts[0]

                self.parse_command(command, parts[1:])

            except EOFError:
                return

    def parse_command(self, command, args):
        if command == 'settings':
            key, value = args
            if key in ('timebank', 'time_per_move', 'your_botid', 'field_columns', 'field_rows'):
                value = int(value)
            self.settings[key] = value

        elif command == 'update':
            sub_command = args[1]
            args = args[2:]

            if sub_command == 'round':
                self.round = int(args[0])
            elif sub_command == 'field':
                self.parse_field(args[0])

        elif command == 'action':
            self.set_timeout(int(args[1]))
            self.make_turn

    def parse_field(self, str_field):
        self.board = np.fromstring(str_field.replace(';', ','), sep=',', dtype=np.uint8).reshape(self.rows(), self.cols())

    class ColumnFullException(Exception):
        """ Raised when attempting to place disk in full column. """


if __name__ == '__main__':
    """ Run the bot! """

    Bot().run()