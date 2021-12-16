import numpy as np
import pandas as pd

with open("Day04/input_AJRF.txt", "r") as f:
    lines = f.readlines()

number_seq = np.array(lines[0].replace("\n", "").split(","), dtype = "int")

boards = []
for board_start in np.arange(2, len(lines), 6):
    board = [line.replace("\n", "").split() for line in lines[board_start:(board_start+5)]]
    #print(board)
    board = np.array(board, dtype="int")
    boards.append(board)

winning_board = None
for number in number_seq:
    for board_id, board in enumerate(boards):
        board = boards[board_id]
        board = np.where(board == number, np.nan, board)
        boards[board_id] = board
        for r in np.arange(5):
            if all([np.isnan(x) for x in board[r,:]]):
                winning_board = board_id
                print("Bingo! Board", board_id, "row", r)
                break
        
        for c in np.arange(5):
            if all([np.isnan(x) for x in board[:,c]]):
                winning_board = board_id
                print("Bingo! Board", board_id, "column", c)
                break
        
        if winning_board != None:
            break

    if winning_board != None:
            break


print(np.nansum(board), number, np.nansum(board) * number)

## Part 2  which wins last?

boards = []
for board_start in np.arange(2, len(lines), 6):
    board = [line.replace("\n", "").split() for line in lines[board_start:(board_start+5)]]
    #print(board)
    board = np.array(board, dtype="int")
    boards.append(board)

winning_boards = []
last_board_id = None
for number in number_seq:
    for board_id, board in enumerate(boards):
        board = np.where(board == number, np.nan, board)
        boards[board_id] = board
        for r in np.arange(5):
            if all([np.isnan(x) for x in board[r,:]]):
                if not(board_id in winning_boards):
                    winning_boards.append(board_id)
        
        for c in np.arange(5):
            if all([np.isnan(x) for x in board[:,c]]):
                if not(board_id in winning_boards):
                    winning_boards.append(board_id)

        if len(winning_boards) == len(boards):
            last_board_id = board_id
            print("Last board is #", last_board_id)
            break

    if last_board_id != None:
        break

print(np.nansum(boards[last_board_id]), number, np.nansum(boards[last_board_id]) * number)



