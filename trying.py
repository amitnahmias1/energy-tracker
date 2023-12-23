import pygame
import sys
import math

# Initialize Pygame
pygame.init()

# Set up display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Circle Collision")

# Set up colors
white = (255, 255, 255)
black = (0, 0, 0)

# Circle properties
circle_radius = 50
circle_pos = (width // 2, height // 2)

# Rectangle properties
rect_width = 50
rect_height = 30
rect_color = (255, 0, 0)

# Create a collision mask surface
circle_mask_surface = pygame.Surface((width, height), pygame.SRCALPHA)
pygame.draw.circle(circle_mask_surface, white, circle_pos, circle_radius)

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Clear the screen
    screen.fill(white)

    # Draw the circle
    pygame.draw.circle(screen, black, circle_pos, circle_radius)

    # Draw the rectangle on colliding pixels

    for x in range(width):
        for y in range(height):
            if circle_mask_surface.get_at((x, y))[3] != 0:  # Check alpha value
                pygame.draw.rect(screen, rect_color, (x, y, rect_width, rect_height))

    # Update the display
    pygame.display.flip()
