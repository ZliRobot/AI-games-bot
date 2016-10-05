def did_he_win(board, player_id, played_column=0):



    # horizontal
    for raw in range(0, board.shape[0]):
        num_of_consecutive = 0
        for column in range(0, board.shape[1]):
            if board[raw, column] == player_id:
                num_of_consecutive += 1
            else:
                num_of_consecutive = 0
            if num_of_consecutive == 4:
                return 1

    # vertical
    for column in range(0, board.shape[1]):
        num_of_consecutive = 0
        for raw in range(0, board.shape[0]):
            if board[raw, column] == player_id:
                num_of_consecutive += 1
            else:
                num_of_consecutive = 0
            if num_of_consecutive == 4:
                return 1

    # ascending diagonal
    for diagonal_num in range(1, board.shape[0] + board.shape[1]-1):
        if diagonal_num <= board.shape[0]:
            raw = diagonal_num-1
            column = 0
        else:
            raw = board.shape[0] - 1
            column = diagonal_num - board.shape[0]
        num_of_consecutive = 0
        while raw >= 0 and column < board.shape[1]:
            if board[raw, column] == player_id:
                num_of_consecutive += 1
            else:
                num_of_consecutive = 0
            if num_of_consecutive == 4:
                return 1
            raw -= 1
            column += 1

    # descending diagonal
    for diagonal_num in range(1, board.shape[0] + board.shape[1]-1):
        if diagonal_num <= board.shape[0]:
            raw = board.shape[0] - diagonal_num
            column = 0
        else:
            raw = 0
            column = diagonal_num - board.shape[0]
        num_of_consecutive = 0
        while raw < board.shape[0] and column < board.shape[1]:
            if board[raw, column] == player_id:
                num_of_consecutive += 1
            else:
                num_of_consecutive = 0
            if num_of_consecutive == 4:
                return 1
            raw += 1
            column += 1

    return 0
