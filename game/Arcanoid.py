import pygame
import random

# Инициализация Pygame
pygame.init()

# Размер экрана
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Арканоид с бонусами")

# Создание объекта clock
clock = pygame.time.Clock()

# Основной цвет
WHITE = (255, 255, 255)

# Дополнительные цвета
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
PURPLE = (128, 0, 128)
PINK = (255, 105, 180)
ORANGE = (255, 165, 0)
BROWN = (139, 69, 19)

# Начальные параметры платформы и мяча
platform = pygame.Rect(350, 550, 100, 20)
platform_color = WHITE  # Начальный цвет платформы белый
platform_speed = 10

ball = pygame.Rect(400, 300, 15, 15)
ball_color = WHITE  # Начальный цвет мяча белый
ball_dx = 4
ball_dy = -4

# Переменные для счета, жизней и уровня
score = 0
lives = 3
level = 1
font = pygame.font.Font(None, 36)

# Цвета кирпичиков на разных уровнях
brick_colors = [PURPLE, PINK, ORANGE, BROWN, PURPLE]

# Список кирпичей
def create_bricks(level):
    bricks = []
    color = brick_colors[(level - 1) % len(brick_colors)]  # Меняем цвет кирпичей с каждым уровнем
    for x in range(50, 750, 100):
        for y in range(50, 200, 40):
            bricks.append({"rect": pygame.Rect(x, y, 80, 30), "color": color})
    return bricks

bricks = create_bricks(level)

# Бонусы
bonuses = []
bonus_timer = 0
active_bonus = None

# Функция рисования всех объектов на экране
def draw_game():
    screen.fill((0, 0, 0))  # Черный фон
    pygame.draw.rect(screen, platform_color, platform)  # Рисуем платформу
    pygame.draw.ellipse(screen, ball_color, ball)  # Рисуем мяч

    # Рисуем кирпичи
    for brick in bricks:
        pygame.draw.rect(screen, brick["color"], brick["rect"])

    # Рисуем бонусы
    for bonus in bonuses:
        pygame.draw.rect(screen, GREEN, bonus)

    # Рисуем текст: счет, жизни, уровень
    score_text = font.render(f"Счёт: {score}", True, WHITE)
    lives_text = font.render(f"Жизни: {lives}", True, WHITE)
    level_text = font.render(f"Уровень: {level}", True, WHITE)
    screen.blit(score_text, (10, 10))
    screen.blit(lives_text, (WIDTH - 150, 10))
    screen.blit(level_text, (WIDTH // 2 - 70, 10))

    # Если жизни закончились, показываем сообщение о конце игры
    if lives <= 0:
        game_over_text = font.render("Игра окончена", True, WHITE)
        screen.blit(game_over_text, (WIDTH // 2 - 100, HEIGHT // 2))

# Функция движения мяча
def move_ball():
    global ball_dx, ball_dy, lives
    ball.x += ball_dx
    ball.y += ball_dy

    # Столкновение с границами экрана
    if ball.left <= 0 or ball.right >= WIDTH:
        ball_dx = -ball_dx
    if ball.top <= 0:
        ball_dy = -ball_dy
    if ball.top > HEIGHT:  # Потеря жизни
        lives -= 1
        reset_ball()

    # Столкновение с платформой
    if ball.colliderect(platform):
        ball_dy = -ball_dy

    # Столкновение с кирпичами
    for brick in bricks[:]:
        if ball.colliderect(brick["rect"]):
            ball_dy = -ball_dy
            bricks.remove(brick)
            global score
            score += 10
            if random.random() < 0.5:  # 50% шанс выпадения бонуса
                bonuses.append(pygame.Rect(brick["rect"].x, brick["rect"].y, 20, 20))
            break

# Функция движения платформы
def move_platform(keys):
    if keys[pygame.K_LEFT] and platform.left > 0:
        platform.x -= platform_speed
    if keys[pygame.K_RIGHT] and platform.right < WIDTH:
        platform.x += platform_speed

# Функция движения бонусов
def move_bonuses():
    for bonus in bonuses[:]:
        bonus.y += 5  # Бонусы падают вниз
        if bonus.colliderect(platform):
            effect = random.choice(["speed_up", "size_up"])
            if effect == "speed_up":
                platform_speed = 15  # Ускорение платформы
            elif effect == "size_up":
                platform.width = 150  # Увеличение платформы
            bonus_timer = pygame.time.get_ticks()
            bonuses.remove(bonus)
        elif bonus.top > HEIGHT:
            bonuses.remove(bonus)

# Функция обновления бонусов (срок действия бонуса)
def update_bonus():
    global platform_speed, platform, active_bonus
    if active_bonus == "speed_up" and pygame.time.get_ticks() - bonus_timer > 10000:  # 10 секунд
        active_bonus = None
        platform_speed = 10
    elif active_bonus == "size_up" and pygame.time.get_ticks() - bonus_timer > 10000:
        active_bonus = None
        platform.width = 100  # Возврат к нормальному размеру

# Функция сброса мяча
def reset_ball():
    ball.x = 400
    ball.y = 300
    global ball_dx, ball_dy
    ball_dx = 4 * random.choice([-1, 1])
    ball_dy = -4

# Функция перехода на следующий уровень
def next_level():
    global level, bricks
    level += 1
    if level > 5:  # Ограничение до 5 уровней
        level = 5
    bricks = create_bricks(level)
    reset_ball()

# Главный игровой цикл
running = True
while running:
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Обработка нажатий клавиш для изменения цветов
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                platform_color = RED
            elif event.key == pygame.K_2:
                platform_color = BLUE
            elif event.key == pygame.K_3:
                platform_color = GREEN
            elif event.key == pygame.K_4:
                ball_color = CYAN
            elif event.key == pygame.K_5:
                ball_color = PURPLE
            elif event.key == pygame.K_6:
                ball_color = YELLOW
            elif event.key == pygame.K_0:  # Сброс всех цветов в белый
                platform_color = WHITE
                ball_color = WHITE

    # Обновление всех движущихся объектов
    move_platform(keys)
    move_ball()
    move_bonuses()
    update_bonus()

    # Переход на следующий уровень, если все кирпичи уничтожены
    if lives > 0 and not bricks:
        next_level()

    # Завершаем игру, если жизни закончились
    if lives <= 0:
        running = False

    # Отображение всех объектов
    draw_game()
    pygame.display.flip()  # Обновление экрана
    clock.tick(60)  # Ограничение до 60 кадров в секунду

pygame.quit()