import pygame

# A cell has 2 attributes:
# alive -> a boolean that represents if the cell is alive
# score -> the number of neighbour cells that are alive
class Cell:
    alive = False
    score = 0

    # Rules:
    # If the cell is alive and has either a score of less than 2 or more than 3, the cell dies
    # If the cell is dead and has exactly 3 neighbours the cell becomes alive
    # All other cells remain the same
    def change_state(self):
        if self.alive and (self.score < 2 or self.score > 3):
            self.alive = False
        elif not self.alive and self.score == 3:
            self.alive = True
        self.score = 0
    

# Initializes pygame
pygame.init()

# Declares variables for display of game
width, height = 800, 800
size = (width, height)
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Conway\'s Game of Life")

clock = pygame.time.Clock()

# How many cells make up the length of a cell
# Minimum is 1 wich means that each pixel is an individual cell
px_per_cell = 10

# The border of black pixels around each cell
border = 1

grid = []

# Gets the positions of the neighbour cells of the cell at the pos position
def get_neighbours_pos(pos):
    return ((pos[0] - 1, pos[1] - 1),
            (pos[0] - 1, pos[1]),
            (pos[0] - 1, pos[1] + 1),
            (pos[0], pos[1] - 1),
            (pos[0], pos[1] + 1),
            (pos[0] + 1, pos[1] - 1),
            (pos[0] + 1, pos[1]),
            (pos[0] + 1, pos[1] + 1))

# Checks if there exists with a cell in the grid with a position of pos
def is_in_grid(pos):
    x, y = pos
    return x >= 0 and x < len(grid[0]) and y >= 0 and y < len(grid)

# Creates grid of cells of length px_to_cells that fits on the screen
def create_grid():
    global grid
    grid_w, grid_h = int((width - 2 * border) / px_per_cell), int((height - 2 * border) / px_per_cell)
    for i in range(grid_h):
        row = []
        for j in range(grid_w):
            row.append(Cell())
        grid.append(row)

# Displays cell as a white or black square (based on wether it's alive or not) with a black outline
def display_cell(alive, pos):
    x, y = pos
    color = (255, 255, 255) if alive else (6, 7, 66)
    pygame.draw.rect(screen, color, pygame.Rect(x * px_per_cell + border,
                                                y * px_per_cell + border,
                                                px_per_cell - 2 * border,
                                                px_per_cell - 2 * border))

def main():
    create_grid()
    simulation = False

    # Value to toggle to the alive attributes of cells when clicked
    toggle_to = True

    hold_right = False
    running = True

    while running:
        # Processes events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                    simulation = not simulation

        # Gets input from mouse
        mouse_pos = pygame.mouse.get_pos()
        left_click, right_click = pygame.mouse.get_pressed()[0], pygame.mouse.get_pressed()[2]

        # Converts mouse_pos from pixels to the position of the cell the cursor is hovering on
        grid_mouse_pos = (int(mouse_pos[0] / px_per_cell), int(mouse_pos[1] / px_per_cell))

        screen.fill((0, 0, 0))

        # Changes the toggle_to boolean when the user presses the right mouse button
        if right_click and not hold_right:
            toggle_to = not toggle_to

        # Switches the state of the selected cell if the following cell if the following conditions are true:
        # The mouse cursor is hovering over a cell
        # The left mouse button is clicked
        # The simulation is not running
        if is_in_grid(grid_mouse_pos) and left_click and not simulation:
            grid[grid_mouse_pos[1]][grid_mouse_pos[0]].alive = toggle_to

        # Runs the simulation
        if simulation:
            # Sets the score atribute of each cell equal to the number of neighbours it has
            for i, row in enumerate(grid):
                for j, cell in enumerate(row):
                    if cell.alive:
                        for pos in get_neighbours_pos((j, i)):
                            if is_in_grid(pos):
                                grid[pos[1]][pos[0]].score += 1
            
            # Changes the state of each cell in grid based on the rules of the game
            for row in grid:
                for cell in row:
                    cell.change_state()

        # Displays every cell in grid
        for i, row in enumerate(grid):
            for j, cell in enumerate(row):
                display_cell(cell.alive, (j, i))
                
        # Checks if the user is, or is not holding the right button of the mouse 
        if right_click:
            hold_right = True
        else:
            hold_right = False
        
        pygame.display.update()

        # Sets game frame rate to 30
        clock.tick(30)
    
    pygame.quit()

if __name__ == "__main__":
    main()