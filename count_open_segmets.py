def count_open_segments(board, player_id, segment_size):

    margine = 3 - segment_size

    def count_now(raw, column, direction, num_of_consecutive, b_open):
        # direction: [0,1] horizontal, [1,0] vertical, [-1,1] ascending diagonal, [1,1] descending diagonal

        new_segments_found = 0

        if board[raw, column] == 0:
            if num_of_consecutive == segment_size:  # segment open on right side
                new_segments_found = 1
                num_of_consecutive = 0
                b_open = True
            else:
                b_open = True
                num_of_consecutive = 0
        elif board[raw, column] == player_id:
            num_of_consecutive += 1
            if b_open and num_of_consecutive == segment_size:  # segment open on left side
                if column == board.shape[1] - 1 or raw == board.shape[0] - 1 or raw == 0:  # only segments of given size, make sure that neighbour is not our
                    new_segments_found = 1
                elif board[raw + direction[0], column + direction[1]] != player_id:
                    new_segments_found = 1
        else:
            num_of_consecutive = 0
            b_open = False


        return new_segments_found, num_of_consecutive, b_open

    open_segments_num = 0

    # horizontal
    for raw in range(0, board.shape[0]):
        num_of_consecutive = 0
        b_left_open = False
        for column in range(margine, board.shape[1] - margine):
            new_segments_found, num_of_consecutive, b_left_open = count_now(raw, column, [0,1], num_of_consecutive,
                                                                            b_left_open)
            open_segments_num += new_segments_found

    # vertical
    for column in range(0, board.shape[1]):
        num_of_consecutive = 0
        b_upper_open = False
        for raw in range(margine, board.shape[0]):
            new_segments_found, num_of_consecutive, b_upper_open = count_now(raw, column, [1,0], num_of_consecutive,
                                                                            b_upper_open)
            open_segments_num += new_segments_found

    # ascending diagonal
    for diagonal_num in range(margine, board.shape[0] + board.shape[1]-1 - margine):
        if diagonal_num <= board.shape[0]:
            raw = diagonal_num-1
            column = 0
        else:
            raw = board.shape[0] - 1
            column = diagonal_num - board.shape[0]
        num_of_consecutive = 0
        b_bottom_left_open = 0
        while raw > margine and column < board.shape[1] - margine:
            new_segments_found, num_of_consecutive, b_bottom_left_open = count_now(raw, column, [-1, 1],
                                                                                   num_of_consecutive,
                                                                                   b_bottom_left_open)
            open_segments_num += new_segments_found

            raw -= 1
            column += 1

    # descending diagonal
    for diagonal_num in range(margine, board.shape[0] + board.shape[1]-1 - margine):
        if diagonal_num <= board.shape[0]:
            raw = board.shape[0] - diagonal_num
            column = 0
        else:
            raw = 0
            column = diagonal_num - board.shape[0]
        num_of_consecutive = 0
        b_upper_left_open = 0
        while raw < board.shape[0] - margine and column < board.shape[1] - margine:
            new_segments_found, num_of_consecutive, b_upper_left_open = count_now(raw, column, [1, 1],
                                                                                    num_of_consecutive,
                                                                                    b_upper_left_open)
            open_segments_num += new_segments_found

            raw += 1
            column += 1

    return open_segments_num


def merit_function(board, player_id):

    mf_my1 = count_open_segments(board, player_id, 1)
    mf_my2 = count_open_segments(board, player_id, 2)
    mf_my3 = count_open_segments(board, player_id, 3)

    mf_e1 = count_open_segments(board, 3 - player_id, 1)
    mf_e2 = count_open_segments(board, 3 - player_id, 2)
    mf_e3 = count_open_segments(board, 3 - player_id, 3)

    return 0 * mf_my1 + 1 * mf_my2 + 5 * mf_my3 - ( mf_e1 + 3 * mf_e2)
