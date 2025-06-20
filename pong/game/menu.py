import pygame
import sys

# Initialize Pygame
pygame.init()

from .game_mechanics import reset_objects
from .conf import WHITE, BLACK, GRAY, WIDTH, HEIGHT, title_font, menu_font, RESOLUTIONS, clock, FPS, screen, FULL_W, FULL_H

# Draw Tools //////////////////////

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

    screen.blit(win_text, center_top(win_text, offset=HEIGHT // 6))
    screen.blit(info_text, center_top(info_text, offset=HEIGHT // 3))

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
    """General menu navigation helper."""

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
    global WIDTH, HEIGHT, FULL_W, FULL_H

    def handle_action(index):

        if index == 0: return 'start'
        elif index == 1: settings_menu()
        elif index == 2: pygame.quit(); sys.exit()

    while True:
        result = navigate_menu(["Start Game", "Settings", "Quit"], draw_menu, lambda i: handle_action(i))

        if result == 'start': return WIDTH, HEIGHT


def mode_selection():
    def handle_action(index):

        score_limit = [5, 10, 20][index]
        return score_limit
    
    result = navigate_menu(["First to 5 Points", "First to 10 Points", "First to 20 Points"], draw_mode_select, handle_action)
    return result


def settings_menu():
    def handle_action(index):

        if index == 0: resolution_selection()
        return index == 1
    
    navigate_menu(["Change Resolution", "Back"], draw_settings_menu, handle_action)


def resolution_selection():
    def handle_action(index):

        global WIDTH, HEIGHT, FULL_W, FULL_H, screen
        res = RESOLUTIONS[index]

        if res == (0, 0):

            screen = pygame.display.set_mode((FULL_W, FULL_H), pygame.FULLSCREEN)
            WIDTH, HEIGHT = FULL_W, FULL_H

        else:

            WIDTH, HEIGHT = res
            screen = pygame.display.set_mode(res)

        reset_objects(WIDTH, HEIGHT)
        return True
    
    navigate_menu(RESOLUTIONS, draw_resolution_menu, handle_action)

def pause_game():
    def handle_action(index): return 'main_menu' if index == 1 else 'resume'
    
    return navigate_menu(["Resume", "Main Menu"], draw_pause_menu, handle_action)