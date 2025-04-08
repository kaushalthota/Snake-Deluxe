import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 600, 400
CELL_SIZE = 20
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🍒 Snake Deluxe")

# Themes
THEMES = {
    "Classic": {
        "bg": (48, 158, 66),
        "border": (169, 169, 169),
        "snake_head": (0, 100, 0),
        "snake_body": (34, 139, 34),
        "food": (220, 20, 60),
        "text": (255, 255, 255),
        "mouth": (255, 255, 0),
    },
    "Night": {
        "bg": (30, 30, 30),
        "border": (70, 70, 70),
        "snake_head": (0, 255, 255),
        "snake_body": (0, 128, 255),
        "food": (255, 105, 180),
        "text": (255, 255, 255),
        "mouth": (255, 255, 0),
    },
    "Desert": {
        "bg": (237, 201, 175),
        "border": (205, 133, 63),
        "snake_head": (139, 69, 19),
        "snake_body": (160, 82, 45),
        "food": (255, 69, 0),
        "text": (0, 0, 0),
        "mouth": (255, 255, 0),
    },
}

selected_theme = THEMES["Classic"]

# Fonts
FONT = pygame.font.SysFont('Arial', 24)
SMALL_FONT = pygame.font.SysFont('Arial', 18)

# Clock
CLOCK = pygame.time.Clock()
SPEED = 10

# Snake settings
snake = [(100, 100), (80, 100), (60, 100)]
snake_dir = (CELL_SIZE, 0)

# Food settings
food = (random.randrange(1, WIDTH // CELL_SIZE - 1) * CELL_SIZE,
        random.randrange(1, HEIGHT // CELL_SIZE - 1) * CELL_SIZE)

# Score
score = 0


def draw_background():
    for x in range(0, WIDTH, CELL_SIZE):
        for y in range(0, HEIGHT, CELL_SIZE):
            pygame.draw.rect(SCREEN, selected_theme["bg"], (x, y, CELL_SIZE, CELL_SIZE))


def draw_border():
    border = selected_theme["border"]
    pygame.draw.rect(SCREEN, border, (0, 0, WIDTH, CELL_SIZE))
    pygame.draw.rect(SCREEN, border, (0, 0, CELL_SIZE, HEIGHT))
    pygame.draw.rect(SCREEN, border, (0, HEIGHT - CELL_SIZE, WIDTH, CELL_SIZE))
    pygame.draw.rect(SCREEN, border, (WIDTH - CELL_SIZE, 0, CELL_SIZE, HEIGHT))


def draw_snake():
    for i, segment in enumerate(snake):
        if i == 0:
            pygame.draw.ellipse(SCREEN, selected_theme["snake_head"], (*segment, CELL_SIZE, CELL_SIZE))
            eye_radius = 2
            offset = 5
            pygame.draw.circle(SCREEN, (255, 255, 255), (segment[0]+offset, segment[1]+offset), eye_radius)
            pygame.draw.circle(SCREEN, (255, 255, 255), (segment[0]+CELL_SIZE-offset, segment[1]+offset), eye_radius)
            pygame.draw.arc(SCREEN, selected_theme["mouth"], (segment[0]+5, segment[1]+10, 10, 5), 3.14, 0, 2)
        else:
            pygame.draw.ellipse(SCREEN, selected_theme["snake_body"], (*segment, CELL_SIZE, CELL_SIZE))


def draw_food():
    pygame.draw.circle(SCREEN, selected_theme["food"], (food[0] + CELL_SIZE // 2, food[1] + CELL_SIZE // 2), CELL_SIZE // 2)


def move_snake():
    global food, score
    head = snake[0]
    new_head = (head[0] + snake_dir[0], head[1] + snake_dir[1])

    if (new_head in snake or
        new_head[0] < CELL_SIZE or new_head[0] >= WIDTH - CELL_SIZE or
        new_head[1] < CELL_SIZE or new_head[1] >= HEIGHT - CELL_SIZE):
        game_over()

    snake.insert(0, new_head)
    if new_head == food:
        score += 1
        food = (random.randrange(1, WIDTH // CELL_SIZE - 1) * CELL_SIZE,
                random.randrange(1, HEIGHT // CELL_SIZE - 1) * CELL_SIZE)
    else:
        snake.pop()


def game_over():
    msg = FONT.render("Game Over! Press any key to exit...", True, selected_theme["food"])
    SCREEN.blit(msg, (WIDTH // 2 - msg.get_width() // 2, HEIGHT // 2))
    pygame.display.flip()
    pygame.time.wait(2000)
    pygame.event.clear()
    while True:
        event = pygame.event.wait()
        if event.type == pygame.KEYDOWN or event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()


def draw_score():
    score_text = FONT.render(f"Score: {score}", True, selected_theme["text"])
    SCREEN.blit(score_text, (10, 5))


def theme_selector_gui():
    SCREEN.fill((0, 0, 0))
    title = FONT.render("Select a Theme", True, (255, 255, 255))
    SCREEN.blit(title, (WIDTH // 2 - title.get_width() // 2, 50))

    buttons = []
    for i, (theme_name, _) in enumerate(THEMES.items()):
        text = SMALL_FONT.render(f"{theme_name}", True, (0, 0, 0))
        btn_rect = pygame.Rect(WIDTH // 2 - 100, 120 + i * 60, 200, 40)
        pygame.draw.rect(SCREEN, (200, 200, 200), btn_rect)
        SCREEN.blit(text, (btn_rect.x + btn_rect.width // 2 - text.get_width() // 2,
                           btn_rect.y + btn_rect.height // 2 - text.get_height() // 2))
        buttons.append((btn_rect, theme_name))

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                for rect, theme in buttons:
                    if rect.collidepoint(mouse_pos):
                        return THEMES[theme]


# Select theme via GUI before game starts
selected_theme = theme_selector_gui()

# Game loop
while True:
    draw_background()
    draw_border()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake_dir != (0, CELL_SIZE):
                snake_dir = (0, -CELL_SIZE)
            elif event.key == pygame.K_DOWN and snake_dir != (0, -CELL_SIZE):
                snake_dir = (0, CELL_SIZE)
            elif event.key == pygame.K_LEFT and snake_dir != (CELL_SIZE, 0):
                snake_dir = (-CELL_SIZE, 0)
            elif event.key == pygame.K_RIGHT and snake_dir != (-CELL_SIZE, 0):
                snake_dir = (CELL_SIZE, 0)

    move_snake()
    draw_snake()
    draw_food()
    draw_score()

    pygame.display.update()
    CLOCK.tick(SPEED)
