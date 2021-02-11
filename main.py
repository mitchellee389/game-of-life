import numpy as np
import pygame
from random import randint

class Grid:

    def __init__(self, width, height, scale, offset, dead_colour, alive_colour):
        self.rows = width // 2
        self.columns = height // 2
        self.scale = scale
        self.offset = offset
        self.dead_colour = dead_colour
        self.alive_colour = alive_colour
        self.grid = np.ndarray(shape=(self.rows, self.columns))
    
    def create_random_grid(self):
        for r in range(0,self.rows):
            for c in range (0,self.columns):
                self.grid[r][c]=randint(0,1)

    def update(self,screen):
        for r in range(self.rows):
            for c in range(self.columns):
                x = r * self.scale
                y = c * self.scale
                rect = [x, y, self.scale - self.offset, self.scale - self.offset]
                if self.grid[r][c] == 1:
                    pygame.draw.rect(screen, self.alive_colour, rect)
                else: 
                    pygame.draw.rect(screen, self.dead_colour, rect)
        next_gen = np.ndarray(shape=(self.rows, self.columns))
        for r in range(self.rows):
            for c in range(self.columns):
                num_live_neighbors = self.get_num_live_neighbours(r,c)
                cell = self.grid[r][c]
                if cell == 0 and num_live_neighbors == 3:
                    next_gen[r][c] = 1
                elif cell == 1 and (num_live_neighbors < 2 or num_live_neighbors > 3):
                    next_gen[r][c]= 0
                else:
                    next_gen[r][c]= cell
        self.grid = next_gen

    def get_num_live_neighbours(self, r, c):
        num_live_neighbours = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                x_edge = (r + i + self.rows) % self.rows
                y_edge = (c + j + self.columns) % self.columns
                num_live_neighbours += self.grid[x_edge][y_edge]
        num_live_neighbours -= self.grid[r][c]
        return num_live_neighbours

def main():
    width, height = 500,500 
    fps = 60
    scale = 20
    offset = 1
    dead_colour = (50, 50, 50)
    alive_colour = (20, 250, 250)

    while True:
        print("Choose colour scheme 1 or 2: ", end="")
        colour_scheme = input()
        if colour_scheme == "2":
            alive_colour = (150, 50, 50)
            break
        elif colour_scheme == "1":
            break

    grid = Grid(width, height, scale, offset, dead_colour, alive_colour)
    grid.create_random_grid()

    pygame.init()
    pygame.display.set_caption("Conway's Game of Life")
    screen = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()

    run = True
    while run:
        clock.tick(fps)
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        grid.update(screen)
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()
