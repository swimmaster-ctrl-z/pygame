import pygame
from random import randrange as rnd

WIDTH, HEIGHT = 1200, 800
FPS = 60

#платформа
paddle_width = 270
paddle_height = 18
paddle_speed = 15
paddle = pygame.Rect(WIDTH // 2 - paddle_width // 2, HEIGHT - paddle_height - 10, paddle_width, paddle_height)

#шарик
ball_radius = 20
ball_speed = 6
ball_rect = int(ball_radius * 2 ** 0.5)
ball = pygame.Rect(rnd(ball_rect, WIDTH - ball_rect), HEIGHT // 2, ball_rect, ball_rect)
dx, dy = 1, -1

#кирпичики
#level1
block_list_level_1 = [pygame.Rect(10 + 120 * i, 10 + 70 * j, 100, 50) for i in range(10) for j in range(3)]
color_list_level_1 = [(rnd(0, 256), rnd(0, 256), rnd(0, 256)) for i in range(10) for j in range(3)]
#level2
block_list_level_2 = [pygame.Rect(10 + 120 * i, 10 + 70 * j, 100, 50) for i in range(10) for j in range(5)]
color_list_level_2 = [(rnd(0, 256), rnd(0, 256), rnd(0, 256)) for i in range(10) for j in range(5)]
#level3
block_list_level_3 = [pygame.Rect(10 + 120 * i, 10 + 70 * j, 100, 50) for i in range(10) for j in range(7)]
color_list_level_3 = [(rnd(0, 256), rnd(0, 256), rnd(0, 256)) for i in range(10) for j in range(7)]

pygame.init()
sc = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
img = pygame.image.load("spasez.jpg").convert()


def detect_collusion(dx, dy, ball, rect):
    if dx > 0:
        delta_x = ball.right - rect.left
    else:
        delta_x = rect.right - ball.left
    if dy> 0:
        delta_y = ball.bottom - rect.top
    else:
        delta_y = rect.bottom - ball.top
    if abs(delta_x - delta_y) < 10:
        dx, dy = -dx, -dy
    elif delta_x > delta_y:
        dy = - dy
    elif delta_y > delta_x:
        dx = -dx
    return dx, dy


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
    #шаблон
    sc.blit(img, (0, 0))
    if block_list_level_1:
        [pygame.draw.rect(sc, color_list_level_1[color], block) for color, block in enumerate(block_list_level_1)]
        hit_index = ball.collidelist(block_list_level_1)
        if hit_index != -1:
            hit_rect = block_list_level_1.pop(hit_index)
            hit_color = color_list_level_1.pop(hit_index)
            dx, dy = detect_collusion(dx, dy, ball, hit_rect)
    if not block_list_level_1:
        paddle_width = 235
        [pygame.draw.rect(sc, color_list_level_2[color], block) for color, block in enumerate(block_list_level_2)]
        hit_index = ball.collidelist(block_list_level_2)
        if hit_index != -1:
            hit_rect = block_list_level_2.pop(hit_index)
            hit_color = color_list_level_2.pop(hit_index)
            dx, dy = detect_collusion(dx, dy, ball, hit_rect)
        FPS = 80
    if not block_list_level_2:
        paddle_width = 200
        [pygame.draw.rect(sc, color_list_level_3[color], block) for color, block in enumerate(block_list_level_3)]
        hit_index = ball.collidelist(block_list_level_3)
        if hit_index != -1:
            hit_rect = block_list_level_3.pop(hit_index)
            hit_color = color_list_level_3.pop(hit_index)
            dx, dy = detect_collusion(dx, dy, ball, hit_rect)
        FPS = 100
    pygame.draw.rect(sc, (255, 0, 255), paddle)
    pygame.draw.circle(sc, (255, 255, 255), ball.center, ball_radius)
        #движение шарика
    ball.x += ball_speed * dx
    ball.y += ball_speed * dy
        #левый и правый край
    if ball.centerx < ball_radius or ball.centerx > WIDTH - ball_radius:
        dx = -dx
        #верхний край
    if ball.centery < ball_radius:
        dy = -dy
        #столкновение с платформой
    if ball.colliderect(paddle) and dy > 0:
        dx, dy = detect_collusion(dx, dy, ball, paddle)
        #столкновение с блоком
    hit_index = ball.collidelist(block_list_level_1)
    if hit_index != -1:
        hit_rect = block_list_level_1.pop(hit_index)
        hit_color = color_list_level_1.pop(hit_index)
        dx, dy = detect_collusion(dx, dy, ball, hit_rect)
    #победа/проигрыш
    if ball.bottom > HEIGHT:
        exit()


    #управление
    key = pygame.key.get_pressed()
    if key[pygame.K_LEFT] and paddle.left > 0:
        paddle.left -= paddle_speed
    if key[pygame.K_RIGHT] and paddle.right < WIDTH:
        paddle.right += paddle_speed

    pygame.display.flip()
    clock.tick(FPS)
