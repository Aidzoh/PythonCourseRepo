import pygame
import random

# Initialize Pygame
pygame.init()

from .conf import WHITE, BLACK, score_font, BASE_WIDTH, screen

# Constants
BALL_SIZE = 20
PADDLE_WIDTH, PADDLE_HEIGHT = 10, 100
BALL_BASE_SPEED_X = 4
BALL_BASE_SPEED_Y = 2

# Game objects
left_paddle = right_paddle = ball = None
init_vel = True
ball_speed_multiplier = 1.0
ball_color = list(WHITE)


def reset_objects(WIDTH, HEIGHT):
    """Reset paddle and ball positions."""

    global left_paddle, right_paddle, ball

    left_paddle = pygame.Rect(50, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
    right_paddle = pygame.Rect(WIDTH - 60, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
    ball = pygame.Rect(WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2, BALL_SIZE, BALL_SIZE)


def reset_ball(WIDTH, HEIGHT):
    """Reset the ball position and return new velocity."""
    global init_vel, ball_speed_multiplier, ball_color

    ball.center = (WIDTH // 2, HEIGHT // 2 + HEIGHT * random.randint(-2, 2) // 8)
    init_vel = True
    ball_speed_multiplier = 1.0
    ball_color = list(WHITE)

    speed_factor = max(0.5, min(1.5, WIDTH / BASE_WIDTH))
    vel_x = random.choice([-BALL_BASE_SPEED_X, BALL_BASE_SPEED_X]) * speed_factor
    vel_y = random.choice([-BALL_BASE_SPEED_Y, BALL_BASE_SPEED_Y]) * speed_factor

    return vel_x, vel_y


# Game //////////////////////

def move_ball(left_score, right_score, WIDTH, HEIGHT):
    """Moves ball and decides if Player scored"""
    global ball_vel_x, ball_vel_y, ball_color

    speed_factor = max(0.6, min(1.4, WIDTH / BASE_WIDTH))

    ball.x += ball_vel_x * ball_speed_multiplier * speed_factor
    ball.y += ball_vel_y * ball_speed_multiplier * speed_factor

    # Wall collisions
    if ball.top <= 0 or ball.bottom >= HEIGHT:

        ball_vel_y *= -1
        ball.top = max(ball.top, 0)
        ball.bottom = min(ball.bottom, HEIGHT)

    # Paddle collisions
    if resolve_collision(left_paddle, WIDTH) or resolve_collision(right_paddle, WIDTH): pass

    # Scoring
    if ball.left <= 0:

        right_score += 1
        reset_ball_with_pause(WIDTH, HEIGHT)

    elif ball.right >= WIDTH:

        left_score += 1
        reset_ball_with_pause(WIDTH, HEIGHT)

    return left_score, right_score


def resolve_collision(paddle, WIDTH):
    """Resolves collisions and prevents wierd colliding behavior"""

    global ball_vel_x, ball_vel_y, init_vel, ball_speed_multiplier, ball_color

    if ball.colliderect(paddle):

        ball_vel_x *= -1

        relative_intersect_y = (paddle.centery - ball.centery)
        normalized = relative_intersect_y / (PADDLE_HEIGHT / 2)
        bounce_angle = normalized * -80
        new_velocity = pygame.math.Vector2(7, 0).rotate(bounce_angle)
        ball_vel_y = int(new_velocity.y * 0.7)

        if init_vel:

            ball_vel_x *= 2
            ball_vel_y *= 2
            init_vel = False

        ball_speed_multiplier = min(ball_speed_multiplier + 0.05 * (WIDTH / BASE_WIDTH), 2)
        ball_color[1] = max(ball_color[1] - 10, 0)
        ball_color[2] = max(ball_color[2] - 15, 0)

        if ball_vel_x > 0:

            ball.left = paddle.right + 1

        else: ball.right = paddle.left - 1

        return True
    
    return False


def reset_ball_with_pause(WIDTH, HEIGHT):
    """Essential for new round start"""

    pygame.time.delay(700)
    global ball_vel_x, ball_vel_y
    ball_vel_x, ball_vel_y = reset_ball(WIDTH, HEIGHT)


def move_paddles(WIDTH, HEIGHT):
    """Ultimate paddles control function"""

    keys = pygame.key.get_pressed()
    move_speed = min(10 * (WIDTH / BASE_WIDTH), 15)

    if keys[pygame.K_w] and left_paddle.top > 0:

        left_paddle.y -= move_speed

    if keys[pygame.K_s] and left_paddle.bottom < HEIGHT:

        left_paddle.y += move_speed

    if keys[pygame.K_UP] and right_paddle.top > 0:

        right_paddle.y -= move_speed

    if keys[pygame.K_DOWN] and right_paddle.bottom < HEIGHT:

        right_paddle.y += move_speed


def draw_objects(left_score, right_score, WIDTH, HEIGHT):
    """Draws objects"""

    screen.fill(BLACK)

    pygame.draw.rect(screen, WHITE, left_paddle)
    pygame.draw.rect(screen, WHITE, right_paddle)
    pygame.draw.ellipse(screen, ball_color, ball)
    pygame.draw.aaline(screen, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT))

    screen.blit(score_font.render(str(left_score), True, WHITE), (WIDTH // 2 - 100, 20))
    screen.blit(score_font.render(str(right_score), True, WHITE), (WIDTH // 2 + 60, 20))

    pygame.display.flip()