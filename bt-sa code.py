import random
from math import exp
import time
from copy import deepcopy

N_QUEENS = 8
TEMPERATURE = 4000


def threat_calculate(n):
    '''Combination formula. It is choosing two queens in n queens'''
    if n < 2:
        return 0
    if n == 2:
        return 1
    return (n - 1) * n / 2


def is_safe(board, row, col, N):
    '''Check if placing a queen at (row, col) is safe'''
    # Check the column
    for i in range(row):
        if board[i][col] == 1:
            return False
    # Check the left diagonal
    for i, j in zip(range(row, -1, -1), range(col, -1, -1)):
        if board[i][j] == 1:
            return False
    # Check the right diagonal
    for i, j in zip(range(row, -1, -1), range(col, N)):
        if board[i][j] == 1:
            return False
    return True


def backtracking(N):
    '''Solve the N Queens problem and return the board'''
    board = [[0 for _ in range(N)] for _ in range(N)]
    if solve_util(board, 0, N):
        return board
    else:
        print("No solution exists")
        return None


def solve_util(board, row, N):
    '''Utility function to solve N Queens problem recursively'''
    if row == N:
        return True  # All queens are placed successfully
    for col in range(N):
        if is_safe(board, row, col, N):
            board[row][col] = 1
            if solve_util(board, row + 1, N):
                return True
            board[row][col] = 0  # Backtrack if no solution found
    return False


def print_solution(board):
    '''Print the chess board'''
    for row in board:
        print(' '.join('Q' if val == 1 else '.' for val in row))


def cost(chess_board):
    '''Calculate how many pairs of threatened queens'''
    N = len(chess_board)
    threat = 0
    for i in range(N):
        for j in range(N):
            if chess_board[i][j] == 1:
                for k in range(N):
                    if k != j and chess_board[i][k] == 1:
                        threat += 1
                    if k != i and chess_board[k][j] == 1:
                        threat += 1
                    if 0 <= i - k < N and 0 <= j - k < N and k != 0 and chess_board[i - k][j - k] == 1:
                        threat += 1
                    if 0 <= i - k < N and j + k < N and k != 0 and chess_board[i - k][j + k] == 1:
                        threat += 1
    return threat // 2


def simulated_annealing():
    '''Simulated Annealing'''
    solution_found = False
    answer = backtracking(N_QUEENS)

    if answer is None:
        return

    # To avoid recounting when can not find a better state
    cost_answer = cost(answer)

    t = TEMPERATURE
    sch = 0.99

    while t > 0:
        t *= sch
        successor = deepcopy(answer)
        row = random.randrange(0, N_QUEENS)
        col = random.randrange(0, N_QUEENS)
        while True:
            if successor[row][col] == 1:
                successor[row][col] = 0
                break
            row = random.randrange(0, N_QUEENS)
            col = random.randrange(0, N_QUEENS)
        successor[row][col] = 1  # Move the queen
        delta = cost(successor) - cost_answer
        if delta < 0 or random.uniform(0, 1) < exp(-delta / t):
            answer = deepcopy(successor)
            cost_answer = cost(answer)
        if cost_answer == 0:
            solution_found = True
            print_solution(answer)
            break
    if not solution_found:
        print("Failed")


def main():
    start = time.time()
    simulated_annealing()
    print("Runtime in second:", time.time() - start)


if __name__ == "__main__":
    main()
