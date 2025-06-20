import pygame
pygame.init()

# Base width and height
BASE_WIDTH = 800
WIDTH, HEIGHT = 800, 600

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (100, 100, 100)

# Fonts
title_font = pygame.font.Font(None, 74)
menu_font = pygame.font.Font(None, 50)
score_font = pygame.font.Font(None, 74)

# Clock setup
clock = pygame.time.Clock()
FPS = 60

# Resolutions
RESOLUTIONS = [(800, 600), (1280, 720), (1920, 1080), (0, 0)]

# Get screen info for fullscreen
screen_info = pygame.display.Info()
FULL_W = screen_info.current_w
FULL_H = screen_info.current_h

# Setup display
screen = pygame.display.set_mode((WIDTH, HEIGHT))