import pygame
import random
import time

# Инициализация Pygame
pygame.init()

# Константы
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
COLORS = [
    (0, 255, 255),   # Cyan (I)
    (255, 165, 0),   # Orange (L)
    (0, 0, 255),     # Blue (J)
    (255, 255, 0),   # Yellow (O)
    (0, 255, 0),     # Green (S)
    (255, 0, 0),     # Red (Z)
    (128, 0, 128)    # Purple (T)
]

# Настройки игры
WIDTH = 10
HEIGHT = 20
BLOCK_SIZE = 30
GAME_WIDTH = WIDTH * BLOCK_SIZE
GAME_HEIGHT = HEIGHT * BLOCK_SIZE
PANEL_WIDTH = 200
SCREEN_WIDTH = GAME_WIDTH + PANEL_WIDTH
SCREEN_HEIGHT = GAME_HEIGHT

# Фигуры Тетриса
SHAPES = [
    [[1, 1, 1, 1]],               # I
    [[1, 0, 0], [1, 1, 1]],        # L
    [[0, 0, 1], [1, 1, 1]],        # J
    [[1, 1], [1, 1]],              # O
    [[0, 1, 1], [1, 1, 0]],        # S
    [[1, 1, 0], [0, 1, 1]],        # Z
    [[0, 1, 0], [1, 1, 1]]         # T
]

class Tetris:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Tetris")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('Arial', 24)
        
        self.grid = [[0] * WIDTH for _ in range(HEIGHT)]
        self.score = 0
        self.level = 1
        self.fall_speed = 1000
        self.last_fall = pygame.time.get_ticks()
        self.current_piece = self.new_piece()
        self.next_piece = self.new_piece()
        self.game_over = False

    def new_piece(self):
        shape = random.choice(SHAPES)
        color = random.choice(COLORS)
        return {
            'shape': shape,
            'color': color,
            'x': WIDTH // 2 - len(shape[0]) // 2,
            'y': 0
        }

    def check_collision(self, piece, dx=0, dy=0):
        for y, row in enumerate(piece['shape']):
            for x, cell in enumerate(row):
                if cell:
                    new_x = piece['x'] + x + dx
                    new_y = piece['y'] + y + dy
                    if new_x < 0 or new_x >= WIDTH or new_y >= HEIGHT:
                        return True
                    if new_y >= 0 and self.grid[new_y][new_x]:
                        return True
        return False

    def rotate_piece(self):
        rotated = list(zip(*reversed(self.current_piece['shape'])))
        if not self.check_collision({'shape': rotated, 
                                   'x': self.current_piece['x'],
                                   'y': self.current_piece['y']}):
            self.current_piece['shape'] = rotated

    def clear_lines(self):
        lines_cleared = 0
        new_grid = []
        for row in self.grid:
            if 0 not in row:
                lines_cleared += 1
            else:
                new_grid.append(row)
        self.grid = [[0]*WIDTH for _ in range(lines_cleared)] + new_grid
        return lines_cleared

    def lock_piece(self):
        for y, row in enumerate(self.current_piece['shape']):
            for x, cell in enumerate(row):
                if cell:
                    self.grid[self.current_piece['y'] + y][self.current_piece['x'] + x] = self.current_piece['color']
        lines = self.clear_lines()
        if lines > 0:
            self.score += [40, 100, 300, 1200][lines-1] * self.level
            self.level = 1 + self.score // 1000
            self.fall_speed = max(50, 1000 - (self.level-1)*100)
        self.current_piece = self.next_piece
        self.next_piece = self.new_piece()
        if self.check_collision(self.current_piece):
            self.game_over = True

    def draw_grid(self):
        for y in range(HEIGHT):
            for x in range(WIDTH):
                if self.grid[y][x]:
                    pygame.draw.rect(self.screen, self.grid[y][x],
                                   (x*BLOCK_SIZE, y*BLOCK_SIZE,
                                    BLOCK_SIZE-1, BLOCK_SIZE-1))

    def draw_piece(self, piece, offset_x=0, offset_y=0):
        for y, row in enumerate(piece['shape']):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(self.screen, piece['color'],
                                   ((piece['x'] + x)*BLOCK_SIZE + offset_x,
                                    (piece['y'] + y)*BLOCK_SIZE + offset_y,
                                    BLOCK_SIZE-1, BLOCK_SIZE-1))

    def draw_panel(self):
        x = GAME_WIDTH + 20
        self.screen.blit(self.font.render(f'Score: {self.score}', True, WHITE), (x, 50))
        self.screen.blit(self.font.render(f'Level: {self.level}', True, WHITE), (x, 100))
        self.screen.blit(self.font.render('Next:', True, WHITE), (x, 200))
        self.draw_piece(self.next_piece, x, 250)

    def run(self):
        while not self.game_over:
            self.screen.fill(BLACK)
            dt = pygame.time.get_ticks() - self.last_fall
            
            # Обработка ввода
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_over = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        if not self.check_collision(self.current_piece, dx=-1):
                            self.current_piece['x'] -= 1
                    if event.key == pygame.K_RIGHT:
                        if not self.check_collision(self.current_piece, dx=1):
                            self.current_piece['x'] += 1
                    if event.key == pygame.K_DOWN:
                        if not self.check_collision(self.current_piece, dy=1):
                            self.current_piece['y'] += 1
                    if event.key == pygame.K_UP:
                        self.rotate_piece()
                    if event.key == pygame.K_SPACE:
                        while not self.check_collision(self.current_piece, dy=1):
                            self.current_piece['y'] += 1
                        self.lock_piece()
            
            # Автоматическое падение
            if dt > self.fall_speed:
                if not self.check_collision(self.current_piece, dy=1):
                    self.current_piece['y'] += 1
                    self.last_fall = pygame.time.get_ticks()
                else:
                    self.lock_piece()

            # Отрисовка
            self.draw_grid()
            self.draw_piece(self.current_piece)
            self.draw_panel()
            pygame.draw.rect(self.screen, GRAY, (0, 0, GAME_WIDTH, GAME_HEIGHT), 1)
            
            pygame.display.flip()
            self.clock.tick(60)
        
        # Экран завершения игры
        self.screen.fill(BLACK)
        text = self.font.render(f'Game Over! Score: {self.score}', True, WHITE)
        self.screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2,
                              SCREEN_HEIGHT//2 - text.get_height()//2))
        pygame.display.flip()
        time.sleep(3)
        pygame.quit()

if __name__ == '__main__':
    game = Tetris()
    game.run()