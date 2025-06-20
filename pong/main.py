import pygame
import sys

# Initialize Pong
pygame.init()
pygame.mouse.set_visible(False)

import game.game_mechanics as mech
import game.menu as menu

from game.conf import clock, FPS

pygame.display.set_caption("Pong - Local Multiplayer")

# Main //////////////////////

running = True
while running:

    WIDTH, HEIGHT = menu.main_menu()
    score_limit = menu.mode_selection()
    left_score = right_score = 0
    mech.reset_objects(WIDTH, HEIGHT)
    mech.reset_ball(WIDTH, HEIGHT)
    mech.reset_ball_with_pause(WIDTH, HEIGHT)
    game_active = True

    while game_active:

        clock.tick(FPS)
        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_ESCAPE, pygame.K_p):

                    result = menu.pause_game()
                    if result == 'main_menu':

                        game_active = False
                        break

        if not game_active: continue

        mech.move_paddles(WIDTH, HEIGHT)
        left_score, right_score = mech.move_ball(left_score, right_score, WIDTH, HEIGHT)
        mech.draw_objects(left_score, right_score, WIDTH, HEIGHT)

        if left_score >= score_limit:

            menu.draw_victory_screen(1)
            game_active = False

        elif right_score >= score_limit:

            menu.draw_victory_screen(2)
            game_active = False

pygame.quit()
sys.exit()