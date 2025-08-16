import pygame
import random
import time

# Инициализация Pygame
pygame.init()

# Настройки окна
WIDTH = 1000
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Змейка")

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Настройки змейки

SNAKE_SIZE = 20
SPEED = 20

# Настройки часов
clock = pygame.time.Clock()

# Шрифт для счета
font = pygame.font.SysFont(None, 35)

def show_score(score):
    text = font.render("Счет: " + str(score), True, WHITE)
    screen.blit(text, [10, 10])

def draw_snake(snake_list):
    for x in snake_list:
        pygame.draw.rect(screen, GREEN, [x[0], x[1], SNAKE_SIZE, SNAKE_SIZE])

def game_loop():
    game_over = False
    game_close = False

    x1 = WIDTH / 2
    y1 = HEIGHT / 2
    dx = 0
    dy = 0

    snake_list = []
    snake_length = 1

    food_x = round(random.randrange(0, WIDTH - SNAKE_SIZE) / SNAKE_SIZE) * SNAKE_SIZE
    food_y = round(random.randrange(0, HEIGHT - SNAKE_SIZE) / SNAKE_SIZE) * SNAKE_SIZE

    while not game_over:
        while game_close:
            screen.fill(BLACK)
            text = font.render("Игра окончена! Нажмите Q-выход или C-играть снова", True, WHITE)
            screen.blit(text, [WIDTH/2 - 250, HEIGHT/2 - 20])
            show_score(snake_length - 1)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        game_loop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and dx == 0:
                    dx = -SNAKE_SIZE
                    dy = 0
                elif event.key == pygame.K_RIGHT and dx == 0:
                    dx = SNAKE_SIZE
                    dy = 0
                elif event.key == pygame.K_UP and dy == 0:
                    dx = 0
                    dy = -SNAKE_SIZE
                elif event.key == pygame.K_DOWN and dy == 0:
                    dx = 0
                    dy = SNAKE_SIZE

        # Проверка границ
        if x1 >= WIDTH or x1 < 0 or y1 >= HEIGHT or y1 < 0:
            game_close = True

        x1 += dx
        y1 += dy
        screen.fill(BLACK)
        pygame.draw.rect(screen, RED, [food_x, food_y, SNAKE_SIZE, SNAKE_SIZE])
        
        snake_head = []
        snake_head.append(x1)
        snake_head.append(y1)
        snake_list.append(snake_head)
        
        if len(snake_list) > snake_length:
            del snake_list[0]

        # Проверка столкновения с собой
        for x in snake_list[:-1]:
            if x == snake_head:
                game_close = True

        draw_snake(snake_list)
        show_score(snake_length - 1)

        pygame.display.update()

        # Съела еду
        if x1 == food_x and y1 == food_y:
            food_x = round(random.randrange(0, WIDTH - SNAKE_SIZE) / SNAKE_SIZE) * SNAKE_SIZE
            food_y = round(random.randrange(0, HEIGHT - SNAKE_SIZE) / SNAKE_SIZE) * SNAKE_SIZE
            snake_length += 1

        clock.tick(SPEED)

    pygame.quit()
    quit()

print(type(SPEED))

game_loop()