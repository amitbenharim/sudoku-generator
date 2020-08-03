import random
from copy import deepcopy


file = open("sudoku.txt", "w")
def new_sudoku():
    initial = [1,4,7,2,5,8,3,6,9]
    sudoku = []
    for i in initial:
        row = [i]
        for j in range(8):
            row.append(i%9+1)
            i += 1
        sudoku.append(row)
    return sudoku

def print_sudoku(sudoku):
    for i in range(len(sudoku)):
        row = ""
        if i%3 == 0 and i > 0:
                print(" - - - - - - - - - - -")
        for j in range(len(sudoku[i])):
            if j%3 == 0 and j > 0:
                row = row + " |"
            row = row + " " + str(sudoku[i][j])
        print(row)

def write_sudoku(sudoku1, sudoku2, sudoku3):
    for i in range(len(sudoku1)):
        row1 = ""
        row2 = ""
        row3 = ""
        if i%3 == 0 and i > 0:
                file.write(" - - - - - - - - - - -\t      - - - - - - - - - - -\t      - - - - - - - - - - -\n")
        for j in range(len(sudoku1[i])):
            if j%3 == 0 and j > 0:
                row1 = row1 + " |"
                row2 = row2 + " |"
                row3 = row3 + " |"
            row1 = row1 + " " + str(sudoku1[i][j])
            row2 = row2 + " " + str(sudoku2[i][j])
            row3 = row3 + " " + str(sudoku3[i][j])
        file.write(row1+"\t     " + row2+"\t     " + row3+"\n")

def swap(board):
    section = random.randint(0, 2)
    line = random.randint(0, 2)
    row1 = random.randint(0, 2)
    row2 = row1
    while row2 == row1:
        row2 = random.randint(0, 2)
    number1 = board[section*3+row1][line]
    number2 = board[section*3+row2][line]
    board[section*3+row1][line] = number2
    board[section*3+row2][line] = number1
    for cycle in range(1,3):
        positions1 = (0, 0)
        positions2 = (0, 0)
        for row in range(section*3, (section+1)*3):
            for column in range(cycle*3, (cycle+1)*3):
                if board[row][column] == number1:
                    position1 = (row, column)
                elif board[row][column] == number2:
                    position2 = (row, column)
        board[position1[0]][position1[1]] = number2
        board[position2[0]][position2[1]] = number1
    return board
def organise(board):
    times = random.randint(0, 3)
    for i in range(times):
        section = random.randint(0, 2)
        line = random.randint(0, 2)
        line2 = line
        while line2 == line:
            line2 = random.randint(0, 2)
        for row in range(9):
            value1 = board[row][section*3 + line]
            value2 = board[row][section*3 + line2]
            board[row][section*3 + line] = value2
            board[row][section*3 + line2] = value1
    for turn in range(40):
        num1 = random.randint(1, 9)
        num2 = num1
        while num2 == num1:
            num2 = random.randint(1, 9)
        for row in range(9):
            for col in range(9):
                if board[row][col] == num1:
                    board[row][col] = num2
                elif board[row][col] == num2:
                    board[row][col] = num1
    return board
def sudoku_solution():
    sudoku = new_sudoku()
    for i in range(500):
        sudoku = swap(sudoku)
    sudoku = organise(sudoku)
    return sudoku

def valid_moves(board):
    valid = []
    options = []
    for i in range(9):
        options.append([])
        for j in range(9):
            options[i].append([])
            for k in range(1, 10):
                options[i][j].append(k)
    for row in range(9):
        for column in range(9):
            value = board[row][column]
            if value != " ":
                for remove in range(9):
                    if value in options[remove][column]:
                        options[remove][column].remove(value)
                    if value in options[row][remove]:
                        options[row][remove].remove(value)
                lower_row = (row//3)*3
                lower_column = (column//3)*3
                for row_remove in range(lower_row, lower_row+3):
                    for column_remove in range(lower_column, lower_column+3):
                        if value in options[row_remove][column_remove]:
                            options[row_remove][column_remove].remove(value)
    rows = []
    columns = []
    squares = []
    track = {}
    for i in range(1, 10):
        track[str(i)] = []
    for i in range(9):
        rows.append(deepcopy(track))
        columns.append(deepcopy(track))
        squares.append(deepcopy(track))

    for row in range(9):
        for column in range(9):
            number = board[row][column]
            if number == " ":
                for value in options[row][column]:
                    columns[column][str(value)].append((row, column))
                    rows[row][str(value)].append((row, column))
                    squares[(row//3)*3+(column//3)][str(value)].append((row, column))
            else:
                columns[column][str(number)].append((row, column))
                rows[row][str(number)].append((row, column))
                squares[(row//3)*3+(column//3)][str(number)].append((row, column))
                columns[column][str(number)].append((row, column))
                rows[row][str(number)].append((row, column))
                squares[(row//3)*3+(column//3)][str(number)].append((row, column))
            if board[row][column] == " " and len(options[row][column]) == 1:
                valid.append((row, column))
    for direction in [rows, columns, squares]:
        for specific in direction:
            for value in specific:
                if len(specific[value]) == 1 and specific[value][0] not in valid:
                    valid.append(specific[value][0])
    return valid

def take_out(board):
    options = []
    for row in range(9):
        for column in range(9):
            new_board = deepcopy(board)
            if new_board[row][column] != " ":
                new_board[row][column] = " "
                if (row, column) in valid_moves(new_board):
                    options.append((row, column))
    return options

def create_sudoku():
    board = sudoku_solution()
    for i in range(80):
        options = take_out(board)
        if len(options) == 0:
            return board
        else:
            index = random.randint(0, len(options)-1)
            final = options[index]
            board[final[0]][final[1]] = " "
    return board

def run():
    print_sudoku(create_sudoku())

##for i in range(50):
##    for j in range(4):
##        write_sudoku(create_sudoku(), create_sudoku(), create_sudoku())
##        file.write("\n")
##    file.write("\n\n")
##file.close()
