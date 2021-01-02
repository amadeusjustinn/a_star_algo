from queue import PriorityQueue
import math
import pygame

""" DEFINE COLOURS IN RGB TUPLE FORM """

BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
GREY = (128, 128, 128)
ORANGE = (255, 165, 0)
PURPLE = (255, 0, 255)
RED = (255, 0, 0)
TURQUOISE = (64, 224, 208)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)


class Cell:
    """
    A class used to represent a Cell object

    Attributes
    ----------
    - row
            int: The row number of the Cell
    - col
            int: The column number of the Cell
    - x
            int: The x-coordinate of the top left corner of the Cell
    - y
            int: The y-coordinate of the top left corner of the Cell
    - side_length
            int: The length of each side of the Cell (each Cell is a square)
    - row_count
            int: The number of rows (and columns) of the grid the Cell is on
    - colour
            tuple(int, int, int): The colour of the Cell
    """

    def __init__(self, row, col, side_length, row_count):
        self.row = row
        self.col = col
        self.x = row * side_length
        self.y = col * side_length
        self.side_length = side_length
        self.row_count = row_count
        self.colour = WHITE

    def draw(self, window: pygame.Surface):
        """
        Draw cell on the grid on window

        Parameters
        ----------
        - window
                pygame.Surface: Window which Cell is to be drawn on
        """
        pygame.draw.rect(window, self.colour, (self.x, self.y,
                                               self.side_length, self.side_length))

    def get_pos(self) -> tuple:
        """ Returns location of cell on grid

        Returns
        -------
        - row, col
                tuple(int, int): A tuple in the form (row, col)
        """
        return self.row, self.col

    def is_barrier(self) -> bool:
        """ Checks if Cell is a barrier/wall/obstacle, i.e. if Cell's colour is black """
        return self.colour == BLACK

    def is_end(self) -> bool:
        """ Checks if Cell is the ending point, i.e. if Cell's colour is blue """
        return self.colour == BLUE

    def is_start(self) -> bool:
        """ Checks if Cell is the starting point, i.e. if Cell's colour is orange """
        return self.colour == ORANGE

    def is_unvisited(self) -> bool:
        """
        Checks if Cell has not been visited by the algorithm,
        i.e. if Cell's colour is green
        """
        return self.colour == GREEN

    def is_visited(self) -> bool:
        """ Checks if Cell has been visited by the algorithm, i.e. if Cell's colour is red """
        return self.colour == RED

    def make_barrier(self) -> None:
        """ Marks selected Cell a barrier/wall/obstacle """
        self.colour = BLACK

    def make_end(self) -> None:
        """ Marks selected Cell the ending point """
        self.colour = BLUE

    def make_path(self) -> None:
        """
        Marks selected Cell part of the path from the starting point
        to the ending point
        """
        self.colour = YELLOW

    def make_start(self) -> None:
        """ Marks selected Cell the starting point """
        self.colour = ORANGE

    def make_unvisited(self) -> None:
        """ Marks selected Cell unvisited """
        self.colour = GREEN

    def make_visited(self) -> None:
        """ Marks selected Cell the ending point """
        self.colour = RED

    def reset(self) -> None:
        """ Marks selected Cell empty """
        self.colour = WHITE

    def update_neighbours(self, grid) -> None:
        """
        Lists every neighbour of Cell in an array

        Parameters
        ----------
        - grid
                list of lists of Cells: Grid that contains Cell
        """
        self.neighbours = []

        # up
        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():
            self.neighbours.append(grid[self.row - 1][self.col])

        # down
        if self.row < self.row_count - 1 and not grid[self.row + 1][self.col].is_barrier():
            self.neighbours.append(grid[self.row + 1][self.col])

        # left
        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():
            self.neighbours.append(grid[self.row][self.col - 1])

        # RIGHT
        if self.col < self.row_count - 1 and not grid[self.row][self.col + 1].is_barrier():
            self.neighbours.append(grid[self.row][self.col + 1])


""" EXTERNAL FUNCTIONS BELOW """


def distance(c1: tuple, c2: tuple) -> float:
    """
    Calculates the Euclidean distance between two Cells on a grid

    Parameters
    ----------
    - c1
            tuple(int, int): The coordinates of a Cell on its grid
    - c2
            tuple(int, int): The coordinates of another Cell on the same grid

    Returns
    -------
    - dist
            float: Euclidean distance between two Cells on a grid
    """
    x1, y1 = c1
    x2, y2 = c2
    dist_sq = (x1 - x2) ** 2 + (y1 - y2) ** 2
    dist = math.sqrt(dist_sq)
    return dist


def draw_grid(cells_in_row: int, win_side_length: int, window: pygame.Surface) -> None:
    """
    Draws a grid of a certain size on a given Surface

    Parameters
    ----------
    - cells_in_row
            int: Number of Cells in each row (and column) of the grid
    - win_side_length
            int: Number of pixels of each side of the Surface
    - window
            pygame.Surface: Window on which the grid is to be drawn
    """
    cell_side_length = win_side_length // cells_in_row
    for i in range(cells_in_row):
        pygame.draw.line(window, GREY, (0, i * cell_side_length),
                         (win_side_length, i * cell_side_length))
        for j in range(cells_in_row):
            pygame.draw.line(window, GREY, (j * cell_side_length, 0),
                             (j * cell_side_length, win_side_length))


def draw_path(came_from: dict, curr: Cell, draw) -> None:
    """
    Draws the path from the starting point to the ending point

    Parameters
    ----------
    - came_from
            dict: Collection of key-value pairs, with each key being a Cell and each value being the
            Cell that preceded it in the finished path
    - curr
            Cell: The ending point of the finished path
    - draw
            lambda: A lambda function
    """
    while curr in came_from:
        curr = came_from[curr]
        curr.make_path()
        draw()


def draw_window(cells_in_row: int, win_side_length: int, window: pygame.Surface, grid) -> None:
    """

    Parameters
    ----------
    - cells_in_row
            int: Number of Cells in each row (and column) of the grid
    - win_side_length
            int: Number of pixels of each side of the Surface
    - window
            pygame.Surface: Window on which the grid is to be drawn
    - grid
            list of lists of Cells: Grid that contains Cell
    """
    window.fill(WHITE)
    for row in grid:
        for cell in row:
            cell.draw(window)
    draw_grid(cells_in_row, win_side_length, window)
    pygame.display.update()


def get_mouse_pos(cells_in_row: int, win_side_length: int, pos: tuple) -> tuple:
    """

    Parameters
    ----------
    - cells_in_row
            int: Number of Cells in each row (and column) of the grid
    - win_side_length
            int: Number of pixels of each side of the Surface
    - pos
            tuple(int, int): Coordinates of mouse cursor/pointer relative to top left corner of window

    Returns
    -------
    - row, col
            tuple(int, int): Coordinates of Cell selected by mouse cursor/pointer
    """
    cell_side_length = win_side_length // cells_in_row
    x, y = pos
    row = x // cell_side_length
    col = y // cell_side_length
    return row, col


def make_grid(cells_in_row, win_side_length) -> list:
    """

    Parameters
    ----------
    - cells_in_row
            int: Number of Cells in each row (and column) of the grid
    - win_side_length
            int: Number of pixels of each side of the Surface

    Returns
    -------
    - grid
            list of lists of Cells: Grid that contains Cells
    """
    grid = []
    cell_side_length = win_side_length // cells_in_row
    for i in range(cells_in_row):
        grid.append([])
        for j in range(cells_in_row):
            cell = Cell(i, j, cell_side_length, cells_in_row)
            grid[i].append(cell)
    return grid


def pathfinder(draw, grid, start, end) -> None:
    """

    Parameters
    ----------
    -
    """
    came_from = {}
    count = 0
    f_score = {cell: float("inf") for row in grid for cell in row}
    f_score[start] = distance(start.get_pos(), end.get_pos())
    g_score = {cell: float("inf") for row in grid for cell in row}
    g_score[start] = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    open_set_hash = {start}
    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        curr = open_set.get()[2]
        open_set_hash.remove(curr)
        if curr == end:
            draw_path(came_from, end, draw)
            start.make_start()
            end.make_end()
            return
        for neighbour in curr.neighbours:
            temp_g = g_score[curr] + 1
            if temp_g < g_score[neighbour]:
                came_from[neighbour] = curr
                f_score[neighbour] = temp_g + \
                    distance(neighbour.get_pos(), end.get_pos())
                g_score[neighbour] = temp_g
                if neighbour not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbour], count, neighbour))
                    open_set_hash.add(neighbour)
                    neighbour.make_unvisited()
        draw()
        if curr != start:
            curr.make_visited()
