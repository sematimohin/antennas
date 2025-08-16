import pygame
import sys

# Инициализация Pygame
pygame.init()

# Константы
TILE_SIZE = 64
WIDTH = 8
HEIGHT = 8
SCREEN_WIDTH = TILE_SIZE * WIDTH
SCREEN_HEIGHT = TILE_SIZE * HEIGHT

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)

# Настройки окна
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Sokoban")

# Загрузка изображений
player_img = pygame.Surface((TILE_SIZE-10, TILE_SIZE-10))
player_img.fill(BLUE)
wall_img = pygame.Surface((TILE_SIZE, TILE_SIZE))
wall_img.fill(BLACK)
box_img = pygame.Surface((TILE_SIZE-10, TILE_SIZE-10))
box_img.fill(RED)
target_img = pygame.Surface((TILE_SIZE-20, TILE_SIZE-20))
target_img.fill(YELLOW)

# Уровни
levels = [
    # Уровень 1
    [
        "########",
        "# ..   #",
        "# $$   #",
        "#  $  @#",
        "#   $$ #",
        "#   .. #",
        "#      #",
        "########"
    ],
    # Уровень 2
    [
        "########",
        "#@  #  #",
        "# $.#  #",
        "#  # $$#",
        "# $  . #",
        "#  ##  #",
        "# .  $ #",
        "########"
    ],
    # Уровень 3
    [
        "########",
        "#@#. # #",
        "# $ #  #",
        "# $ $ .#",
        "## ## ##",
        "# .  $ #",
        "#   #  #",
        "########"
    ]
]

class GameObject:
    def __init__(self, x, y, is_wall=False, is_box=False, is_target=False):
        self.x = x
        self.y = y
        self.is_wall = is_wall
        self.is_box = is_box
        self.is_target = is_target

    def draw(self):
        if self.is_wall:
            screen.blit(wall_img, (self.x*TILE_SIZE, self.y*TILE_SIZE))
        elif self.is_box:
            screen.blit(box_img, (self.x*TILE_SIZE+5, self.y*TILE_SIZE+5))
        elif self.is_target:
            screen.blit(target_img, (self.x*TILE_SIZE+10, self.y*TILE_SIZE+10))

def parse_level(level):
    objects = []
    player_pos = (0, 0)
    for y, row in enumerate(level):
        for x, char in enumerate(row):
            if char == "#":
                objects.append(GameObject(x, y, is_wall=True))
            elif char == "$":
                objects.append(GameObject(x, y, is_box=True))
            elif char == ".":
                objects.append(GameObject(x, y, is_target=True))
            elif char == "@":
                player_pos = (x, y)
    return objects, player_pos

def move_is_valid(new_x, new_y, dx, dy, objects):
    for obj in objects:
        if obj.is_wall and obj.x == new_x and obj.y == new_y:
            return False
    
    for obj in objects:
        if obj.is_box:
            if obj.x == new_x and obj.y == new_y:
                next_x = new_x + dx
                next_y = new_y + dy
                if any(o.is_wall or o.is_box for o in objects if o.x == next_x and o.y == next_y):
                    return False
                obj.x += dx
                obj.y += dy
    return True

def check_win(objects):
    boxes = [obj for obj in objects if obj.is_box]
    targets = [obj for obj in objects if obj.is_target]
    
    for target in targets:
        if not any(box.x == target.x and box.y == target.y for box in boxes):
            return False
    return True

def show_message(text, color):
    font = pygame.font.Font(None, 74)
    text = font.render(text, True, color)
    text_rect = text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
    screen.blit(text, text_rect)
    pygame.display.flip()
    pygame.time.wait(2000)

def main():
    current_level = 0
    max_level = len(levels) - 1
    clock = pygame.time.Clock()  # Инициализация часов
    
    while current_level <= max_level:
        objects, (player_x, player_y) = parse_level(levels[current_level])
        running = True
        win = False
        
        while running:
            screen.fill(WHITE)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.KEYDOWN:
                    dx, dy = 0, 0
                    if event.key == pygame.K_LEFT:
                        dx = -1
                    elif event.key == pygame.K_RIGHT:
                        dx = 1
                    elif event.key == pygame.K_UP:
                        dy = -1
                    elif event.key == pygame.K_DOWN:
                        dy = 1
                    
                    if dx != 0 or dy != 0:
                        new_x = player_x + dx
                        new_y = player_y + dy
                        
                        if move_is_valid(new_x, new_y, dx, dy, objects):
                            player_x = new_x
                            player_y = new_y
            
            # Отрисовка объектов
            for obj in objects:
                obj.draw()
            
            # Отрисовка игрока
            screen.blit(player_img, (player_x*TILE_SIZE+5, player_y*TILE_SIZE+5))
            
            # Проверка победы
            if check_win(objects):
                win = True
                running = False
            
            pygame.display.flip()
            clock.tick(30)
        
        if win:
            current_level += 1
            if current_level > max_level:
                show_message("ALL LEVELS COMPLETED!", GREEN)
                pygame.quit()
                sys.exit()
            else:
                show_message(f"LEVEL {current_level}!", GREEN)
    
    pygame.quit()

if __name__ == "__main__":
    main()