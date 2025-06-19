import pygame
import sys
import random

# Initialize Pygame
pygame.init()
pygame.mouse.set_visible(False)

# Constants
BASE_WIDTH = 800
WIDTH, HEIGHT = 800, 600
FPS = 60
BALL_SIZE = 20
PADDLE_WIDTH, PADDLE_HEIGHT = 10, 100
BALL_BASE_SPEED_X = 4
BALL_BASE_SPEED_Y = 2

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (100, 100, 100)

# Fonts
title_font = pygame.font.Font(None, 74)
menu_font = pygame.font.Font(None, 50)
score_font = pygame.font.Font(None, 74)

# Get screen info for fullscreen
screen_info = pygame.display.Info()
FULLSCREEN_WIDTH = screen_info.current_w
FULLSCREEN_HEIGHT = screen_info.current_h
RESOLUTIONS = [(800, 600), (1280, 720), (1920, 1080), (0, 0)]

# Setup display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong - Local Multiplayer")
clock = pygame.time.Clock()

# Game objects
left_paddle = right_paddle = ball = None
init_vel = True
ball_speed_multiplier = 1.0
ball_color = list(WHITE)


def reset_objects():
    """Reset paddle and ball positions."""

    global left_paddle, right_paddle, ball

    left_paddle = pygame.Rect(50, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
    right_paddle = pygame.Rect(WIDTH - 60, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
    ball = pygame.Rect(WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2, BALL_SIZE, BALL_SIZE)


def reset_ball():
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

reset_objects()
ball_vel_x, ball_vel_y = reset_ball()



# Draw tools //////////////////////

def draw_menu(selected_index):
    """Draw main menu."""

    screen.fill(BLACK)

    title_text = title_font.render("Pong Game", True, WHITE)
    screen.blit(title_text, center_top(title_text))
    draw_menu_items(["Start Game", "Settings", "Quit"], selected_index)

    pygame.display.flip()


def draw_mode_select(selected_index):
    """Draw score limit selection menu."""

    screen.fill(BLACK)

    title_text = title_font.render("Score Limit", True, WHITE)
    screen.blit(title_text, center_top(title_text))
    draw_menu_items(["First to 5 Points", "First to 10 Points", "First to 20 Points"], selected_index)

    pygame.display.flip()


def draw_settings_menu(selected_index):
    """Draw settings menu."""

    screen.fill(BLACK)

    title_text = title_font.render("Settings", True, WHITE)
    screen.blit(title_text, center_top(title_text))
    draw_menu_items(["Change Resolution", "Back"], selected_index)

    pygame.display.flip()


def draw_resolution_menu(selected_index):
    """Draw resolution selection menu."""

    screen.fill(BLACK)
    title_text = title_font.render("Select Resolution", True, WHITE)
    screen.blit(title_text, center_top(title_text))

    for i, res in enumerate(RESOLUTIONS):

        label = "Fullscreen" if res == (0, 0) else f"{res[0]} x {res[1]}"
        color = WHITE if i == selected_index else GRAY
        text = menu_font.render(label, True, color)
        y_pos = HEIGHT // 2 + i * 60

        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, y_pos))

    pygame.display.flip()


def draw_pause_menu(selected_index):
    """Draw pause menu."""

    screen.fill(BLACK)

    title_text = title_font.render("Game Paused", True, WHITE)
    screen.blit(title_text, center_top(title_text))

    draw_menu_items(["Resume", "Main Menu"], selected_index)

    pygame.display.flip()


def draw_victory_screen(winner):
    """Show victory screen."""

    screen.fill(BLACK)

    win_text = title_font.render(f"Player {winner} Wins!", True, WHITE)
    info_text = menu_font.render("Press ENTER to return to main menu", True, GRAY)

    screen.blit(win_text, center_top(win_text, offset=-HEIGHT // 6))
    screen.blit(info_text, center_top(info_text))

    pygame.display.flip()

    while True:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN: return


def draw_menu_items(items, selected_index):
    """Helper to draw menu items."""

    for i, item in enumerate(items):

        color = WHITE if i == selected_index else GRAY
        text = menu_font.render(item, True, color)
        y_pos = HEIGHT // 2 + i * 60

        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, y_pos))


def center_top(surface, offset=0):
    """Center surface horizontally at top."""

    return WIDTH // 2 - surface.get_width() // 2, HEIGHT // 4 + offset


# Menu //////////////////////

def navigate_menu(options, draw_func, action_func=None):
    """Generic menu navigation helper."""

    selected_index = 0

    while True:

        clock.tick(FPS)
        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_UP:
                    selected_index = max(0, selected_index - 1)

                elif event.key == pygame.K_DOWN:
                    selected_index = min(len(options) - 1, selected_index + 1)

                elif event.key == pygame.K_RETURN:
                    if action_func:

                        result = action_func(selected_index)

                        if result is not None: return result
                        
                    else: return selected_index
                    
        draw_func(selected_index)


def main_menu():
    def handle_action(index):

        if index == 0: return 'start'
        elif index == 1: settings_menu()
        elif index == 2: pygame.quit(); sys.exit()

    while True:
        result = navigate_menu(["Start Game", "Settings", "Quit"], draw_menu, lambda i: handle_action(i))

        if result == 'start': return


def mode_selection():
    def handle_action(index):

        global score_limit
        score_limit = [5, 10, 20][index]
        return True
    
    navigate_menu(["First to 5 Points", "First to 10 Points", "First to 20 Points"], draw_mode_select, handle_action)


def settings_menu():
    def handle_action(index):

        if index == 0: resolution_selection()
        return index == 1
    
    navigate_menu(["Change Resolution", "Back"], draw_settings_menu, handle_action)


def resolution_selection():
    def handle_action(index):

        global WIDTH, HEIGHT, screen
        res = RESOLUTIONS[index]

        if res == (0, 0):

            screen = pygame.display.set_mode((FULLSCREEN_WIDTH, FULLSCREEN_HEIGHT), pygame.FULLSCREEN)
            WIDTH, HEIGHT = FULLSCREEN_WIDTH, FULLSCREEN_HEIGHT
        else:

            WIDTH, HEIGHT = res
            screen = pygame.display.set_mode(res)

        reset_objects()
        return True
    
    navigate_menu(RESOLUTIONS, draw_resolution_menu, handle_action)

def pause_game():
    def handle_action(index): return 'main_menu' if index == 1 else 'resume'
    
    return navigate_menu(["Resume", "Main Menu"], draw_pause_menu, handle_action)


# Game //////////////////////

def move_ball(left_score, right_score):
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
    if resolve_collision(left_paddle) or resolve_collision(right_paddle): pass

    # Scoring
    if ball.left <= 0:

        right_score += 1
        reset_ball_with_pause()

    elif ball.right >= WIDTH:

        left_score += 1
        reset_ball_with_pause()

    return left_score, right_score


def resolve_collision(paddle):

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


def reset_ball_with_pause():

    pygame.time.delay(700)
    global ball_vel_x, ball_vel_y
    ball_vel_x, ball_vel_y = reset_ball()


def move_paddles():

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


def draw_objects(left_score, right_score):

    screen.fill(BLACK)

    pygame.draw.rect(screen, WHITE, left_paddle)
    pygame.draw.rect(screen, WHITE, right_paddle)
    pygame.draw.ellipse(screen, ball_color, ball)
    pygame.draw.aaline(screen, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT))

    screen.blit(score_font.render(str(left_score), True, WHITE), (WIDTH // 2 - 100, 20))
    screen.blit(score_font.render(str(right_score), True, WHITE), (WIDTH // 2 + 60, 20))

    pygame.display.flip()