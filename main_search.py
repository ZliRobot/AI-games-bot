# ------------------------------------------------------------------- #
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
# ------------------------------------------------------------------- #

from sys import stdin, stdout
import count_open_segmets_full as csf
import did_he_win as dhw
import numpy as np
import time
import os


class Bot(object):

    settings = dict()
    round = -1
    board = np.zeros((6, 7), dtype=np.uint8)  # Access with [row_nr, col_nr]. [0,0] is on the top left.
    timeout = -1
    mf_coeff = np.array([0., 1., 5., 1., 3., 100.])

    def make_turn(self):
        """ This method is for calculating and executing the next play.
            Make the play by calling place_disc exactly once.
        """

        # if play first, start in the middle
        if np.count_nonzero(self.board) == 0:
            self.place_disc(self.board.shape[1] / 2, "middle")
            return 1

        # else
        max_search_level = 2
        start_level = 0  # start search from level 0

        move, merit = self.search_tree(self.id(), self.board, start_level, max_search_level)

        self.place_disc(move, merit)
        return 1

    def search_tree(self, player, board, level, max_level):
        level += 1
        mf_value = np.ones(self.board.shape[1]) * -10000

        for try_column in [3, 4, 2, 5, 1, 6, 0]:
            if board[0, try_column] == 0:

                new_board = self.simulate_place_disc(board, try_column, player)
                if level < max_level:
                    if dhw.did_he_win(new_board, player, try_column):
                        mf_value[try_column] = 1000
                    else:
                        potential_move, mf_value[try_column] = self.search_tree(3-player, new_board, level, max_level)
                        mf_value[try_column] *= -1
                else:
                    if dhw.did_he_win(new_board, player, try_column):
                        mf_value[try_column] = 1000
                    else:
                        mf_value[try_column] = csf.merit_function(new_board, player, self.mf_coeff)

        return np.argmax(mf_value), np.max(mf_value)

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
            self.make_turn()

        elif command == 'mf_coeff':
            self.mf_coeff = np.fromstring(args[0], sep=',')

    def parse_field(self, str_field):
        self.board = np.fromstring(str_field.replace(';', ','), sep=',', dtype=np.uint8).reshape(self.rows(), self.cols())

    class ColumnFullException(Exception):
        """ Raised when attempting to place disk in full column. """


if __name__ == '__main__':
    """ Run the bot! """

    Bot().run()
