import pygame
import random

# Constants
SCREEN_WIDTH = 300
SCREEN_HEIGHT = 600
BLOCK_SIZE = 30
GRID_WIDTH = SCREEN_WIDTH // BLOCK_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // BLOCK_SIZE

# Shapes and their colors
SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1], [1, 1]],  # O
    [[1, 1, 0], [0, 1, 1]],  # Z
    [[0, 1, 1], [1, 1, 0]],  # S
    [[1, 1, 1], [0, 1, 0]],  # T
    [[1, 1, 1], [1, 0, 0]],  # L
    [[1, 1, 1], [0, 0, 1]]   # J
]

COLORS = [
    (0, 255, 255),
    (255, 255, 0),
    (255, 0, 0),
    (0, 255, 0),
    (128, 0, 128),
    (255, 165, 0),
    (0, 0, 255)
]

class Tetris:
    def __init__(self):
        self.grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.current_piece = self.get_new_piece()
        self.next_piece = self.get_new_piece()
        self.game_over = False
        self.score = 0

    def get_new_piece(self):
        shape = random.choice(SHAPES)
        color = COLORS[SHAPES.index(shape)]
        return {'shape': shape, 'color': color, 'x': GRID_WIDTH // 2, 'y': 0}

    def rotate_piece(self):
        self.current_piece['shape'] = [list(row) for row in zip(*self.current_piece['shape'][::-1])]

    def move_piece(self, dx, dy):
        self.current_piece['x'] += dx
        self.current_piece['y'] += dy

    def valid_move(self, dx, dy, shape=None):
        if shape is None:
            shape = self.current_piece['shape']
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell:
                    new_x = self.current_piece['x'] + x + dx
                    new_y = self.current_piece['y'] + y + dy
                    if new_x < 0 or new_x >= GRID_WIDTH or new_y < 0 or new_y >= GRID_HEIGHT:
                        return False
                    if self.grid[new_y][new_x]:
                        return False
        return True

    def lock_piece(self):
        for y, row in enumerate(self.current_piece['shape']):
            for x, cell in enumerate(row):
                if cell:
                    self.grid[self.current_piece['y'] + y][self.current_piece['x'] + x] = self.current_piece['color']
        self.clear_lines()
        self.current_piece = self.next_piece
        self.next_piece = self.get_new_piece()
        if not self.valid_move(0, 0):
            self.game_over = True

    def clear_lines(self):
        new_grid = [row for row in self.grid if any(cell == 0 for cell in row)]
        lines_cleared = GRID_HEIGHT - len(new_grid)
        self.score += lines_cleared ** 2
        new_grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(lines_cleared)] + new_grid
        self.grid = new_grid

    def drop_piece(self):
        if self.valid_move(0, 1):
            self.move_piece(0, 1)
        else:
            self.lock_piece()

    def draw_grid(self, screen):
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                color = self.grid[y][x]
                if color:
                    pygame.draw.rect(screen, color, pygame.Rect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
                pygame.draw.rect(screen, (128, 128, 128), pygame.Rect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)

    def draw_piece(self, screen):
        for y, row in enumerate(self.current_piece['shape']):
            for x, cell in enumerate(row):
                if cell:
                    color = self.current_piece['color']
                    pygame.draw.rect(screen, color, pygame.Rect((self.current_piece['x'] + x) * BLOCK_SIZE, (self.current_piece['y'] + y) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    game = Tetris()

    while not game.game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and game.valid_move(-1, 0):
                    game.move_piece(-1, 0)
                elif event.key == pygame.K_RIGHT and game.valid_move(1, 0):
                    game.move_piece(1, 0)
                elif event.key == pygame.K_DOWN:
                    game.drop_piece()
                elif event.key == pygame.K_UP:
                    rotated = [list(row) for row in zip(*game.current_piece['shape'][::-1])]
                    if game.valid_move(0, 0, rotated):
                        game.rotate_piece()

        game.drop_piece()

        screen.fill((0, 0, 0))
        game.draw_grid(screen)
        game.draw_piece(screen)
        pygame.display.flip()
        clock.tick(10)

    pygame.quit()

if __name__ == "__main__":
    main()
