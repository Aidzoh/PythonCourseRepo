import pygame
import sys
import game.test as tst

# Initialize Pygame
pygame.init()
pygame.mouse.set_visible(False)

# Main //////////////////////

running = True
while running:

    tst.main_menu()
    tst.mode_selection()
    left_score = right_score = 0
    tst.reset_ball_with_pause()
    game_active = True

    while game_active:

        tst.clock.tick(tst.FPS)
        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_ESCAPE, pygame.K_p):

                    result = tst.pause_game()
                    if result == 'main_menu':

                        game_active = False
                        break

        if not game_active: continue

        tst.move_paddles()
        left_score, right_score = tst.move_ball(left_score, right_score)
        tst.draw_objects(left_score, right_score)

        if left_score >= tst.score_limit:

            tst.draw_victory_screen(1)
            game_active = False

        elif right_score >= tst.score_limit:

            tst.draw_victory_screen(2)
            game_active = False

pygame.quit()
sys.exit()