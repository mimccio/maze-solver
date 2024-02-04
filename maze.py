from cell import Cell
import time
import random


class Maze:
    def __init__(
        self,
        x1,
        y1,
        num_rows,
        num_cols,
        cell_size_x,
        cell_size_y,
        win=None,
        seed=None
    ):
        self._cells = []
        self._x1 = x1
        self._y1 = y1
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._win = win
        self._seed = seed

        self._create_cells()
        self._break_entrance_and_exit()
        self._break_walls_r(0,0)
        self._reset_cells_visited()

    def _create_cells(self):
        self._cells = [[Cell(self._win) for i in range(self._num_rows)]  for i in range(self._num_cols)]
        for i in range(self._num_cols):
            for j in range(self._num_rows):
                self._draw_cell(i, j)

    def _break_entrance_and_exit(self):
        self._cells[0][0].has_top_wall = False
        self._draw_cell(0,0)
        exit_i = self._num_cols - 1
        exit_j = self._num_rows - 1
        self._cells[exit_i][exit_j].has_bottom_wall = False
        self._draw_cell(exit_i, exit_j)


    def _draw_cell(self,i,j):
        if self._win is None:
            return
        x1 = self._x1 + i * self._cell_size_x
        y1 = self._y1 + j * self._cell_size_y
        x2 = x1 + self._cell_size_x
        y2 = y1 + self._cell_size_y
        self._cells[i][j].draw(x1, y1, x2, y2)
        self._animate()

    def _animate(self):
        if self._win is None:
            return
        self._win.redraw()
        time.sleep(0.05)

    def _break_walls_r(self, i, j):
        self._cells[i][j].visited = True
        random.seed(self._seed)
        while True:
            directions = []
            i_east = i + 1
            i_west = i - 1
            j_north = j - 1
            j_south = j + 1
            # east
            if i_east < self._num_cols and self._cells[i_east][j].visited == False:
                directions.append('east')
            # west
            if i_west >= 0 and self._cells[i_west][j].visited == False:
                directions.append('west')
            # north
            if j_north >= 0 and self._cells[i][j_north].visited == False:
                directions.append('north')
            # south
            if j_south < self._num_rows and self._cells[i][j_south].visited == False:
                directions.append('south')

            if len(directions) == 0:
                return
            
            direction = random.choice(directions)
            if direction == 'east':
                self._cells[i_east][j].has_left_wall = False
                self._draw_cell(i_east,j)
                self._break_walls_r(i_east,j)
            elif direction == 'west':
                self._cells[i_west][j].has_right_wall = False
                self._draw_cell(i_west,j)
                self._break_walls_r(i_west,j)
            elif direction == 'north':
                self._cells[i][j_north].has_bottom_wall = False
                self._draw_cell(i,j_north)
                self._break_walls_r(i,j_north)
            elif direction == 'south':
                self._cells[i][j_south].has_top_wall = False
                self._draw_cell(i, j_south)
                self._break_walls_r(i, j_south)

    def _reset_cells_visited(self):
        for col in self._cells:
            for cell in col:
                cell.visited = False

    def solve(self):
        return self._solve_r(0,0)
    
    def _solve_r(self, i, j):
        self._animate()
        current_cell = self._cells[i][j]
        current_cell.visited = True
        if i == self._num_cols - 1 and j == self._num_rows - 1:
            return True
        directions = ["east", "west", "north", "south"]
        for direction in directions:
            if direction == "east" and i + 1 < self._num_cols and not self._cells[i + 1][j].has_left_wall and not self._cells[i + 1][j].visited:
                current_cell.draw_move(self._cells[i + 1][j])
                result = self._solve_r(i + 1, j)
                if result:
                    return True
                current_cell.draw_move(self._cells[i + 1][j], True)
            if direction == "west" and i - 1 >= 0 and not self._cells[i - 1][j].has_right_wall and not self._cells[i - 1][j].visited:
                current_cell.draw_move(self._cells[i - 1][j])
                result = self._solve_r(i - 1, j)
                if result:
                    return True
                current_cell.draw_move(self._cells[i - 1][j], True)
            if direction == "north" and j - 1 >= 0 and not self._cells[i][j - 1].has_bottom_wall and not self._cells[i][j - 1].visited:
                current_cell.draw_move(self._cells[i][j - 1])
                result = self._solve_r(i, j - 1)
                if result:
                    return True
                current_cell.draw_move(self._cells[i][j - 1], True)
            if direction == "south" and j + 1 < self._num_rows and not self._cells[i][j + 1].has_top_wall and not self._cells[i][j + 1].visited:
                current_cell.draw_move(self._cells[i][j + 1])
                result = self._solve_r(i, j + 1)
                if result:
                    return True
                current_cell.draw_move(self._cells[i][j + 1], True)
        return False
                

                

                
                 