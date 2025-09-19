import pygame
import random

running = True

WIDTH = 700
HEIGHT = 600

left_points = 0
right_points = 0

pygame.init()
my_font = pygame.font.SysFont('comic Sans Ms', 30)

surface = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Tennis for two")

left_padding = right_padding = 10
up_padding = down_padding = 10

BAR_HEIGHT = HEIGHT / 3
BAR_WIDTH = WIDTH / 20

BALL_HEIGHT = WIDTH / 20
BALL_WIDTH = WIDTH / 20

left_bar = pygame.Rect(
    left_padding, 
    up_padding, 
    BAR_WIDTH, 
    BAR_HEIGHT
)

right_bar = pygame.Rect(
    WIDTH - BAR_WIDTH - right_padding,
    up_padding,
    BAR_WIDTH,
    BAR_HEIGHT
)

middle_line = pygame.Rect(
    WIDTH / 2,
    0,
    WIDTH / 90,
    HEIGHT
)

ball = pygame.Rect(
    WIDTH / 2 - BALL_WIDTH / 2,
    HEIGHT / 2 - BALL_HEIGHT / 2,
    BALL_WIDTH,
    BALL_HEIGHT
)

BAR_Y_SPEED = 20
ACCELERATION = 0.05

ball_x_speed = 15 * random.sample([-1, 1], 1)[0]
ball_y_speed = 25 * random.sample([-1, 1], 1)[0]

def ball_collides_with_right_bar(): 
    return ball.left + ball.width >= right_bar.left and right_bar.top < ball.top < right_bar.top + right_bar.height

def ball_collides_with_left_bar():
    return ball.left <= left_bar.left + left_bar.width and left_bar.top < ball.top < left_bar.top + left_bar.height

def game_over() -> bool:
    if ball.left + ball.width >= WIDTH:
        global left_points
        left_points += 1
        return True
    if ball.left < 0:
        global right_points 
        right_points += 1
        return True
    return False  

clock = pygame.time.Clock()

while running:
    
    #clock.tick(5)

    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False

    keys = pygame.key.get_pressed()

    # right bar controls
    if keys[pygame.K_UP]:
        right_bar.move_ip(0, - BAR_Y_SPEED * (right_bar.top > 0 + up_padding))
    if keys[pygame.K_DOWN]:
        right_bar.move_ip(0, BAR_Y_SPEED * ((right_bar.top + right_bar.height) < HEIGHT - down_padding))
    # left bar controls
    if keys[pygame.K_w]:
        left_bar.move_ip(0, - BAR_Y_SPEED * (left_bar.top > 0 + up_padding))
    if keys[pygame.K_s]:
        left_bar.move_ip(0, BAR_Y_SPEED * ((left_bar.top + left_bar.height) < HEIGHT - down_padding))
    # ball movement
    # top and down border collision
    if ball.top <= 0 + up_padding: ball_y_speed *= -(1 + ACCELERATION)
    if ball.top + ball.height >= HEIGHT - down_padding: ball_y_speed *= -(1 + ACCELERATION)
    # bar collision
    if ball_collides_with_right_bar(): ball_x_speed *= -(1 + ACCELERATION)
    if ball_collides_with_left_bar(): ball_x_speed *= -(1 + ACCELERATION)
    if game_over():
        ball_x_speed = 15 * random.sample([-1, 1], 1)[0]
        ball_y_speed = 25 * random.sample([-1, 1], 1)[0]        
        ball = pygame.Rect(
            WIDTH / 2 - BALL_WIDTH / 2,
            HEIGHT / 2 - BALL_HEIGHT / 2,
            BALL_WIDTH,
            BALL_HEIGHT
        )
        
    ball.move_ip(ball_x_speed, ball_y_speed)

    # Score
    left_score = my_font.render(str(left_points), False, (255, 255, 255))
    right_score = my_font.render(str(right_points), False, (255, 255, 255))

    # Reset frame
    surface.fill((0, 0, 0))

    surface.blit(left_score, (WIDTH / 2 - 30, 0))
    surface.blit(right_score, (WIDTH / 2 + 20, 0))
    pygame.draw.rect(surface, (255, 255, 255), left_bar)
    pygame.draw.rect(surface, (255, 255, 255), right_bar)
    pygame.draw.rect(surface, (255, 255, 255), middle_line)
    pygame.draw.rect(surface, (255, 255, 255), ball)
    
    pygame.display.update()

    pygame.time.wait(100)

