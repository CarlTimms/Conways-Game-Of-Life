"""

    Conway's Game of Life
    
    
    CT
    2022-08-28


    Left click grid to add seed patterns, then hit space to run.

"""


# Import libraries
import time
import pygame
import numpy as np
import random


# Declare constants
COLOR_BG = (10, 10, 10)
COLOR_GRID = (25, 25, 25)
COLOR_DIE_NEXT = (50, 50, 50)
COLOR_ALIVE_NEXT = (255, 255, 255)
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
CELL_SIZE = 7
SLEEP_TIME = 0.00


def add_seed(cells, pos):
    # Dictionary of well-know Game of Life patterns
    patterns = {
          "R-pentomino": [(0, 0), (-1, 0), (0, 1), (0, -1), (1, -1)]
        , "Diehard": [(-3, 0), (-2, 0), (-2, 1), (2, 1), (3, 1), (4, 1), (3, -1)]
        , "Acorn": [(0, 0), (-3, 1), (-2, 1), (-2, -1), (1, 1), (2, 1), (3, 1)]
        , "Bunnies": [(-4, -1), (-3, 2), (-2, 0), (-2, 1), (-1, 2), (1, 1), (2, 0), (2, -1), (3, 1)]
        , "B-heptomino": [(0, 0), (-1, 0), (-1, -1), (0, 1), (1, 0), (1, -1), (2, -1)]
        , "Pi-heptomino": [(-1, 0), (-1, -1), (-1, 1), (0, -1), (1, 0), (1, -1), (1, 1)]
        , "Gliders by the dozen": [(-2, 0), (-2, -1), (-2, 1), (-1, -1), (1, 1), (2, 0), (2, -1), (2, 1)]
    }

    for x, y in random.choice(list(patterns.values())):
        cells[(pos[1] // CELL_SIZE) + y, (pos[0] // CELL_SIZE) + x] = 1

    return cells


def update(screen, cells, size, with_progress=False):
    """
        Applies game rules and updates animation.

        Rules:
            Any live cell with two or three live neighbours survives.
            Any dead cell with three live neighbours becomes a live cell.
            All other live cells die in the next generation. Similarly, all other dead cells stay dead.
    """

    updated_cells = np.zeros((cells.shape[0], cells.shape[1]))

    for row, col in np.ndindex(cells.shape):
        alive = np.sum(cells[row - 1:row + 2, col - 1:col + 2]) - cells[row, col]  # Count number of neighbours
        color = COLOR_BG if cells[row, col] == 0 else COLOR_ALIVE_NEXT

        # Live cell
        if cells[row, col] == 1:
            # A live cell with less than 2 or more than 3 living neighbours dies
            if alive < 2 or alive > 3:
                if with_progress:
                    color = COLOR_DIE_NEXT
            # A live cell with 2 or 3 living neighbours survives
            elif 2 <= alive <= 3:
                updated_cells[row, col] = 1
                if with_progress:
                    color = COLOR_ALIVE_NEXT
        # Dead cell
        else:
            #  Any dead cell with three live neighbours becomes a live cell
            if alive == 3:
                updated_cells[row, col] = 1
                if with_progress:
                    color = COLOR_ALIVE_NEXT

        # Draw cell
        pygame.draw.rect(screen, color, (col * size, row * size, size - 1, size - 1))

    return updated_cells


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    cells = np.zeros((SCREEN_HEIGHT // CELL_SIZE, SCREEN_WIDTH // CELL_SIZE))
    screen.fill(COLOR_GRID)
    update(screen, cells, CELL_SIZE)

    pygame.display.flip()
    pygame.display.update()

    running = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    running = not running
                    update(screen, cells, CELL_SIZE)
                    pygame.display.update()

            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                cells = add_seed(cells, pos)
                update(screen, cells, CELL_SIZE)
                pygame.display.update()

            screen.fill(COLOR_GRID)

        if running:
            cells = update(screen, cells, CELL_SIZE, with_progress=True)
            pygame.display.update()

        time.sleep(SLEEP_TIME)


if __name__ == '__main__':
    main()
