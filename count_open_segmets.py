def count_open_segments(board, player_id, played_column, segment_size):
    margin = 3 - segment_size

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
                if column == board.shape[1] - 1 or raw == board.shape[0] - 1 or raw == 0:
                    # only segments of given size, make sure that neighbour is not our
                    new_segments_found = 1
                elif board[raw + direction[0], column + direction[1]] != player_id:
                    new_segments_found = 1
        else:
            num_of_consecutive = 0
            b_open = False

        return new_segments_found, num_of_consecutive, b_open

    # find landing raw
    if board[0, played_column] != 0:
        played_raw = 0
    else:
        played_raw = board.shape[0] - 1
        while board[played_raw - 1, played_column] != 0:
            played_raw -= 1

    open_segments_num = 0

    # horizontal
    raw = played_raw
    num_of_consecutive = 0
    b_left_open = False
    for column in range(margin, board.shape[1] - margin):
        new_segments_found, num_of_consecutive, b_left_open = count_now(raw, column, [0, 1], num_of_consecutive,
                                                                        b_left_open)
        open_segments_num += new_segments_found

    # vertical
    column = played_column
    num_of_consecutive = 0
    b_upper_open = False
    for raw in range(margin, board.shape[0]):
        new_segments_found, num_of_consecutive, b_upper_open = count_now(raw, column, [1, 0], num_of_consecutive,
                                                                         b_upper_open)
        open_segments_num += new_segments_found

    # ascending diagonal
    diagonal_num = played_raw + played_column + 1
    if diagonal_num <= board.shape[0]:
        raw = diagonal_num - 1
        column = 0
    else:
        raw = board.shape[0] - 1
        column = diagonal_num - board.shape[0]
    num_of_consecutive = 0
    b_bottom_left_open = 0
    while raw > margin and column < board.shape[1] - margin:
        new_segments_found, num_of_consecutive, b_bottom_left_open = count_now(raw, column, [-1, 1],
                                                                               num_of_consecutive,
                                                                               b_bottom_left_open)
        open_segments_num += new_segments_found

        raw -= 1
        column += 1

    # descending diagonal
    diagonal_num = played_column + board.shape[0] - played_raw
    if diagonal_num <= board.shape[0]:
        raw = board.shape[0] - diagonal_num
        column = 0
    else:
        raw = 0
        column = diagonal_num - board.shape[0]
    num_of_consecutive = 0
    b_upper_left_open = 0
    while raw < board.shape[0] - margin and column < board.shape[1] - margin:
        new_segments_found, num_of_consecutive, b_upper_left_open = count_now(raw, column, [1, 1],
                                                                              num_of_consecutive,
                                                                              b_upper_left_open)
        open_segments_num += new_segments_found

        raw += 1
        column += 1

    return open_segments_num


def merit_function(board, player_id, played_column, coeff=None):
    if coeff is None: coeff = [0., 1., 5., -1., -3., 0.]

    mf_my1 = count_open_segments(board, player_id, played_column, 1)
    mf_my2 = count_open_segments(board, player_id, played_column, 2)
    mf_my3 = count_open_segments(board, player_id, played_column, 3)

    mf_e1 = count_open_segments(board, 3 - player_id, played_column, 1)
    mf_e2 = count_open_segments(board, 3 - player_id, played_column, 2)
    mf_e3 = count_open_segments(board, 3 - player_id, played_column, 3)

    mf_value = coeff[0] * mf_my1 + coeff[1] * mf_my2 + coeff[2] * mf_my3 + coeff[3] * mf_e1 \
               + coeff[4] * mf_e2 + coeff[5] * mf_e3

    return mf_value
