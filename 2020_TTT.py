import unittest
from math import inf
import sys

debug = False

COMPUTER = 1
HUMAN = -1

def wins(board, player):
    return player == board[0][0] == board[0][1] == board[0][2] or player == board[1][0] == board[1][1] == board[1][2] or \
        player == board[2][0] == board[2][1] == board[2][2] or player == board[0][0] == board[1][0] == board[2][0] or \
        player == board[0][1] == board[1][1] == board[2][1] or player == board[0][2] == board[1][2] == board[2][2] or \
        player == board[0][0] == board[1][1] == board[2][2] or player == board[0][2] == board[1][1] == board[2][0]


def empty_cells(board):
    for x, row in enumerate(board):
        for y, cell in enumerate(row):
            if cell == 0:
                yield x, y

def find_depth(board):
    depth = 0
    for row in board:
        for cell in row:
            if cell == 0:
                depth += 1
    return depth
    
def find_state(board):
    if wins(board, 1):
        return 1
    if wins(board, -1):
        return -1
    return 0

debug = False
COUNT = 0

def minimax(board, depth, is_max):

    global COUNT
    
    state = find_state(board)

    if debug:
        print('DEPTH: ', depth)
        for row in board:
            print(row)
    
    if state == 1:
        COUNT +=1
        if debug: print('\n\nSTEP: {}, COMPUTER WIN, state: {}'.format(COUNT, state))
        return {'score': state, 'depth': depth}
    if state == -1:
        COUNT += 1
        if debug: print('\n\nSTEP: {}, HUMAN WIN, state: {}'.format(COUNT, state))
        return {'score': state, 'depth': depth}
    if depth == 0:
        COUNT += 1
        if debug: print('\n\nSTEP: {}, DRAW, state: {}'.format(COUNT, state))
        return {'score': state, 'depth': depth}

    saved_best = { 'score': -inf if is_max else inf, 'depth': depth }
    for x in range(3):
        for y in range(3):
            if board[x][y] == 0:
            
                COUNT += 1
                player = 1 if is_max else -1
                if debug: print('\n\nSTEP: ', COUNT, 'Placing ', player, ' at ', x, y, ', max: ', is_max)
                
                board[x][y] = 1 if is_max else -1
                
                if is_max:
                    if debug: print('loc: ({},{}): depth: {}, finding MAX between {} and ...'.format(x, y, depth, saved_best['score']))
                    best = minimax(board, depth - 1, not is_max)
                    if debug: print('COMPUTER finding MAX between {} and {}'.format(best['score'], saved_best['score']))
                    if best['score'] > saved_best['score']:
                        saved_best = best
                        
                    if debug: print('loc: ({},{}), COMPUTER REPORTING: {} at depth {}, UP TO DEPTH: {}'.format(x,y,best['score'], best['depth'], depth))
                else:
                    if debug: print('loc: ({}, {}): depth: {}, finding MIN between {} and ...'.format(x, y, depth, saved_best['score']))
                    best = minimax(board, depth - 1, not is_max)
                    if debug: print('HUMAN finding MIN between {} and {}'.format(best['score'], saved_best['score']))
                    if best['score'] < saved_best['score']:
                        saved_best = best
                    if debug: print('loc: ({},{}), HUMAN REPORTING: {} at depth {}, UP TO DEPTH: {}'.format(x,y,best['score'], best['depth'],depth))
                    
                board[x][y] = 0
                
    return saved_best

debug_main = False
def find_best_move(board, player):
    depth = find_depth(board)
    saved_best = {'score': -inf if player == COMPUTER else inf, 'depth': depth} 
    best_move = {'row': -1, 'col': -1}


    if debug: print('find_depth(board): ', depth)
    if debug:
        for row in board:
            print(row)
    for x in range(3):
        for y in range(3):
            if board[x][y] == 0:
                board[x][y] = player

                global COUNT

                if debug_main: print('\n\nSTEP: ', COUNT, 'EVALUATING: ', player, ' AT ', x, y)
                COUNT += 1
                
                if player == 1:
                    best = minimax(board, find_depth(board), False)
                else:
                    best = minimax(board, find_depth(board), True)
                if debug_main: print('\n\nEVALUATED: BEST FOR {}, {} IS: {} AT DEPTH: {}'.format(x,y,best['score'],best['depth']))
                board[x][y] = 0

                if (player == 1 and best['score'] > saved_best['score']) or (player == -1 and best['score'] < saved_best['score']):
                    best_move['row'] = x
                    best_move['col'] = y
                    saved_best = best
                elif best['score'] == saved_best['score']:
                    if best['depth'] > saved_best['depth']:
                        best_move['row'] = x
                        best_move['col'] = y
                        saved_best = best              
    return best_move
                        
    

class TTT:
    
    def __init__(self):
        self.game_not_over = True
        self.grid = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ]
        self.valid_choices = ('x', 'o', -1, 1, 0)

        # 'map-user-choice-to-partial-function' list, where user choice becomes index to list
        self.operations = list()
        self.operations.append(self.make_move(self.grid, 0, 0))
        self.operations.append(self.make_move(self.grid, 0, 1))
        self.operations.append(self.make_move(self.grid, 0, 2))
        self.operations.append(self.make_move(self.grid, 1, 0))
        self.operations.append(self.make_move(self.grid, 1, 1))
        self.operations.append(self.make_move(self.grid, 1, 2))
        self.operations.append(self.make_move(self.grid, 2, 0))
        self.operations.append(self.make_move(self.grid, 2, 1))
        self.operations.append(self.make_move(self.grid, 2, 2))
        
        # self.computer is used in the start_game() method, but im setting it here as an attribute
        # of the TTT class, because I also use it in the execute_computer_logic() method
        
        self.computer = 1
        self.player = -1

        
    # make_move wraps and returns the inner closure function so that make_move can be used
    # as a partial method that accepts row and column, and returns the inner function
    # that accepts player_choice when it is called.
    def make_move(self, board, row, column):

        def inner(player_choice):
            assert player_choice in self.valid_choices
            if board[row][column] == 0:
                board[row][column] = player_choice
                return True
            return False
        
        return inner

    def initialize_game(self):
        
        message_to_user = 'enter x or o \n'
        player_choice = input(message_to_user)

        # check that the user entered x or o and keep asking until they do
        while player_choice not in self.valid_choices: 
            player_choice = input(message_to_user)

        self.computer = 'x' if player_choice == 'o' else 'o'
        self.player = player_choice
        print('ok im ' + self.computer)
        return None
        
    def play_game(self):

        #self.initialize_game()
        #assert self.computer and self.player

        for row in self.grid:
            print(row)
        
        while self.game_not_over:

            while True:
                board_number_choice = int(input('enter choice 1 - 9 \n')) - 1
                # execute the appropriate self.make_move partial function from the operations list
                if self.operations[board_number_choice](self.player):
                    break
                else:
                    print('That spot is taken. Try again')
            
            returned = find_best_move(self.grid, 1)

            self.grid[returned['row']][returned['col']] = self.computer

            state = find_state(self.grid)

            for row in self.grid:
                print(row)

            message = { -1: "You Win!", 0: 'Draw', 1: 'Computer Wins'}
            if state in (-1, 1):
                return message[state]

class test_game(unittest.TestCase):
    
    def test_find_state(self):

        
        self.assertEqual(find_state([[1, 1, -1],[1, -1, -1],[-1, -1, 1]]), -1) # digaonal win
        self.assertEqual(find_state([[-1, 1, 1],[1, -1, -1],[1, -1, -1]]), -1) # digaonal win
        self.assertEqual(find_state([[-1, 1, 1],[1, 1, -1],[1, -1, -1]]), 1)   # digaonal win
        self.assertEqual(find_state([[1, 1, -1],[1, 1, -1],[1, -1, 1]]), 1)    # digaonal win
        
        self.assertEqual(find_state([[-1, 1, -1],[1, 1, -1],[1, -1, 1]]), 0)   # draw
        self.assertEqual(find_state([[-1, 1, -1],[-1, 1, -1],[1, -1, 1]]), 0)  # draw
        
        self.assertEqual(find_state([[-1, -1, -1],[1, 1, -1],[1, -1, 1]]), -1) # row win
        self.assertEqual(find_state([[1, -1, 1],[1, 1, -1],[1, 1, 1]]), 1)     # row win

        self.assertEqual(find_state([[-1, 1, -1],[-1, 1, -1],[-1, -1, 1]]), -1)# column win
        self.assertEqual(find_state([[1, 1, -1],[-1, 1, -1],[1, -1, -1]]), -1) # column win
        

if __name__ == '__main__':
    
    ttt = TTT()
    print(ttt.play_game())

    #unittest.main()
    


    
