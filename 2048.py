import random, sys, unittest
import os

class Game2048:

    def __init__(self, height, width):
        self.grid = []
        self.coords = []
        for y in range(height):
            newrow = []
            for x in range(width):
                self.coords.append((y,x))
                newrow.append(0)
            self.grid.append(newrow)

        self.set_samples(2)
        
    def set_samples(self, num):
        print('entering set_samples')
        assert num in (1,2)
        newcoords = []
        valid_coords = [item for item in self.coords if self.grid[item[0]][item[1]] == 0]
        samples = random.sample(valid_coords, num)
        for loc in samples:
            tile = random.sample([2,2,2,2,2,2,2,2,2,4], 1)
            print('sample location', loc[0], loc[1])
            self.grid[loc[0]][loc[1]] = tile[0]

    def rotate(self, grid):
        newgrid = [list(reversed(list(item))) for item in zip(*grid)] #<-----!!!
        return newgrid

    def merge_row_left(self, row):
        size = len(row)
        newrow = [item for item in row if item != 0]
    
        i = 0
        while i < (len(newrow) - 1):
            if newrow[i] == newrow[i + 1]: #<-------------------problem here
                newrow[i] = newrow[i] * 2
                del newrow[i + 1]
            i += 1

        while len(newrow) < size:
            newrow.append(0)
        return newrow

    def shift(self, grid):
        newgrid = []
        for item in grid:
            newrow = self.merge_row_left(item)
            newgrid.append(newrow)
        return newgrid
        
    def main(self):
##        os.system('cls')
        d = None
        while d not in ('u d l r'.split(' ')):
            d = input('choose a direction: u, d, l, r: ')
        if d == 'l':
            self.grid = self.shift(self.grid)
        elif d == 'u':
            self.grid = self.rotate(self.shift(self.rotate(self.rotate(self.rotate(self.grid)))))
        elif d == 'd':
            self.grid = self.rotate(self.rotate(self.rotate(self.shift(self.rotate(self.grid)))))
        elif d == 'r':
            self.grid = self.rotate(self.rotate(self.shift(self.rotate(self.rotate(self.grid)))))
        self.set_samples(1) #<----this is overwriting other tiles!!!!
        print(self)
                 
    def __str__(self):
        grid = ''
        for item in self.grid:
            update = str(item) + '\n'
            grid += update
        return grid

class test_game(unittest.TestCase):
    def test_merge_row_left(self):
        grid = Game2048(4,6)

        #test edge cases: list of one item, list of zeros
        self.assertEqual(grid.merge_row_left([2]), [2])
        self.assertEqual(grid.merge_row_left([4]), [4])
        self.assertEqual(grid.merge_row_left([0,0,0,0,0,0]), [0,0,0,0,0,0])
        self.assertEqual(grid.merge_row_left([0]), [0])
        
        #test multiple merges per row
        self.assertEqual(grid.merge_row_left([4,4,4,4]), [8,8,0,0])
        self.assertEqual(grid.merge_row_left([2,2,2,2,2,2]), [4,4,4,0,0,0])
        self.assertEqual(grid.merge_row_left([0,2,2,0,0,2,2,2]), [4,4,2,0,0,0,0,0])
        self.assertEqual(grid.merge_row_left([0,2,0,2,0,2,0,2,2]), [4,4,2,0,0,0,0,0,0])

if __name__ == '__main__':

    #unittest.main()
    
    grid = Game2048(4,6)
    print(grid)
    while True:
        grid.main()
