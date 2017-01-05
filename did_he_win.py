def did_he_win(board, player_id, played_column):
    # tests for victory
    # board - updated board, move already played
    # played column - last played column

    height = board.shape[0]
    width = board.shape[1]

    # find landing raw
    if board[0, played_column] != 0:
        played_raw = 0
    else:
        played_raw = height - 1
        while board[played_raw - 1, played_column] != 0:
            played_raw -= 1

    # horizontal
    raw = played_raw
    num_of_consecutive = 0
    for column in range(0, width):
        if board[raw, column] == player_id:
            num_of_consecutive += 1
        else:
            num_of_consecutive = 0
        if num_of_consecutive == 4:
            return 1

    # vertical
    column = played_column
    num_of_consecutive = 0
    for raw in range(0, height):
        if board[raw, column] == player_id:
            num_of_consecutive += 1
        else:
            num_of_consecutive = 0
        if num_of_consecutive == 4:
            return 1

    # ascending diagonal
    diagonal_num = played_raw + played_column + 1
    if diagonal_num <= height:
        raw = diagonal_num-1
        column = 0
    else:
        raw = height - 1
        column = diagonal_num - height
    num_of_consecutive = 0
    while raw >= 0 and column < width:
        if board[raw, column] == player_id:
            num_of_consecutive += 1
        else:
            num_of_consecutive = 0
        if num_of_consecutive == 4:
            return 1
        raw -= 1
        column += 1

    # descending diagonal
    diagonal_num = played_column + height - played_raw
    if diagonal_num <= height:
        raw = height - diagonal_num
        column = 0
    else:
        raw = 0
        column = diagonal_num - height
    num_of_consecutive = 0
    while raw < height and column < width:
        if board[raw, column] == player_id:
            num_of_consecutive += 1
        else:
            num_of_consecutive = 0
        if num_of_consecutive == 4:
            return 1
        raw += 1
        column += 1

    return 0
