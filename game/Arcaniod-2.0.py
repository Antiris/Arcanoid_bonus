import pygame
import random

# Инициализация Pygame
pygame.init()

# Настройки экрана
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Арканоид")

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
GREEN = (0, 255, 0)

# Параметры платформы, мяча и кирпичей
platform = pygame.Rect(WIDTH // 2 - 60, HEIGHT - 30, 120, 15)
platform_speed = 10
platform_color = WHITE

ball = pygame.Rect(WIDTH // 2 - 10, HEIGHT // 2, 15, 15)
ball_dx, ball_dy = 4, -4
ball_color = WHITE

brick_width, brick_height = 80, 30
bricks = [pygame.Rect(x, y, brick_width, brick_height)
          for y in range(50, 200, 40) for x in range(50, WIDTH - 50, 90)]

# Переменные игры
lives = 3
score = 0
level = 1
max_level = 4
font = pygame.font.Font(None, 36)

# Бонусы
bonuses = []
bonus_effects = {"platform_speed": 0, "ball_speed": 1, "platform_size": 0, "double_points": False, "slow_ball": False, "slow_platform": False}
bonus_timers = {}

# Функция сброса мяча и платформы
def reset_ball_and_platform():
    global ball_dx, ball_dy
    ball.x, ball.y = WIDTH // 2, HEIGHT // 2
    ball_dx = random.choice([-4, 4])
    ball_dy = -4
    platform.x = WIDTH // 2 - platform.width // 2

# Функция отрисовки объектов
def draw_game():
    screen.fill(BLACK)
    pygame.draw.rect(screen, platform_color, platform)
    pygame.draw.ellipse(screen, ball_color, ball)
    for brick in bricks:
        pygame.draw.rect(screen, WHITE, brick)
    for bonus in bonuses:
        pygame.draw.rect(screen, YELLOW, bonus)

    score_text = font.render(f"Счёт: {score}", True, WHITE)
    lives_text = font.render(f"Жизни: {lives}", True, WHITE)
    pause_text = font.render(f"Нажмите P для паузы", True, WHITE)
    screen.blit(score_text, (10, 10))
    screen.blit(lives_text, (WIDTH - 150, 10))
    screen.blit(pause_text, (WIDTH // 2 - 100, 10))

    # Отображение значка паузы
    if paused:
        # Два прямоугольника для паузы
        pygame.draw.rect(screen, WHITE, pygame.Rect(WIDTH // 2 - 50, HEIGHT // 2 - 20, 15, 40))
        pygame.draw.rect(screen, WHITE, pygame.Rect(WIDTH // 2 + 35, HEIGHT // 2 - 20, 15, 40))

# Функция движения мяча
def move_ball():
    global ball_dx, ball_dy, lives, score, bricks, bonuses
    ball.x += ball_dx
    ball.y += ball_dy

    if ball.left <= 0 or ball.right >= WIDTH:
        ball_dx = -ball_dx
    if ball.top <= 0:
        ball_dy = -ball_dy
    if ball.top >= HEIGHT:
        lives -= 1
        reset_ball_and_platform()

    if ball.colliderect(platform):
        ball_dy = -ball_dy

    for brick in bricks[:]:
        if ball.colliderect(brick):
            bricks.remove(brick)
            ball_dy = -ball_dy
            score += 20 if bonus_effects["double_points"] else 10
            if random.random() < 0.3:  # Шанс на бонус
                bonus = pygame.Rect(brick.x, brick.y, 20, 20)
                bonuses.append(bonus)
            break

# Функция движения платформы
def move_platform(keys):
    global platform_speed
    if keys[pygame.K_LEFT] and platform.left > 0:
        platform.x -= platform_speed
    if keys[pygame.K_RIGHT] and platform.right < WIDTH:
        platform.x += platform_speed

# Функция обработки бонусов
def handle_bonuses():
    global platform_speed, ball_dx, ball_dy, platform, ball, bonus_effects, bonuses, bonus_timers

    for bonus in bonuses[:]:
        bonus.y += 5
        if bonus.colliderect(platform):
            effect = random.choice(["platform_speed", "ball_speed", "platform_size", "double_points", "slow_ball", "slow_platform"])
            if effect == "platform_speed":
                platform_speed += 3
            elif effect == "ball_speed":
                ball_dx *= 1.2
                ball_dy *= 1.2
            elif effect == "platform_size":
                platform.width += 20
            elif effect == "double_points":
                bonus_effects["double_points"] = True
            elif effect == "slow_ball":
                bonus_effects["slow_ball"] = True
                ball_dx *= 0.6
                ball_dy *= 0.6
            elif effect == "slow_platform":
                bonus_effects["slow_platform"] = True
                platform_speed *= 0.6

            bonus_timers[effect] = pygame.time.get_ticks()
            bonuses.remove(bonus)
        elif bonus.top > HEIGHT:
            bonuses.remove(bonus)

    # Обновление бонусов
    current_time = pygame.time.get_ticks()
    for effect, timer in list(bonus_timers.items()):
        if current_time - timer > 10000:  # 10 секунд
            if effect == "platform_speed":
                platform_speed = 10
            elif effect == "ball_speed":
                ball_dx /= 1.2
                ball_dy /= 1.2
            elif effect == "platform_size":
                platform.width = 120
            elif effect == "double_points":
                bonus_effects["double_points"] = False
            elif effect == "slow_ball":
                bonus_effects["slow_ball"] = False
                ball_dx /= 0.6
                ball_dy /= 0.6
            elif effect == "slow_platform":
                bonus_effects["slow_platform"] = False
                platform_speed /= 0.6
            del bonus_timers[effect]

# Главный цикл игры
running = True
paused = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                paused = not paused
            if event.key == pygame.K_1:
                platform_color = YELLOW
            if event.key == pygame.K_2:
                platform_color = ORANGE
            if event.key == pygame.K_3:
                platform_color = GREEN
            if event.key == pygame.K_4:
                ball_color = YELLOW
            if event.key == pygame.K_5:
                ball_color = ORANGE
            if event.key == pygame.K_6:
                ball_color = GREEN
            if event.key == pygame.K_0:
                platform_color = WHITE
                ball_color = WHITE

    keys = pygame.key.get_pressed()
    if not paused:
        move_platform(keys)
        move_ball()
        handle_bonuses()

    if not bricks:
        level += 1
        if level > max_level:
            running = False
        else:
            bricks = [pygame.Rect(x, y, brick_width, brick_height) for y in range(50, 200, 40)
                      for x in range(50, WIDTH - 50, 90)]
            reset_ball_and_platform()

    if lives <= 0:
        running = False

    draw_game()
    pygame.display.flip()
    pygame.time.Clock().tick(60)

# Конец игры
screen.fill(BLACK)
game_over_text = font.render("Игра окончена", True, WHITE)
score_text = font.render(f"Ваш итоговый счёт: {score}", True, WHITE)
screen.blit(game_over_text, (WIDTH // 2 - 100, HEIGHT // 2 - 50))
screen.blit(score_text, (WIDTH // 2 - 100, HEIGHT // 2))
pygame.display.flip()
pygame.time.wait(5000)
pygame.quit()
