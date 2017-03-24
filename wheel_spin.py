from window import Window

import random
from math import pi

import time
import sys
import pygame
pygame.init()

# initialize window
window = Window(1200, 800, Window.COLORS['BLACK'], 'Lincoln Palooza Wheel Spin')

# colors of the wheel
color_keys = ['RED', 'ORANGE', 'YELLOW', 'GREEN', 'CYAN', 'BLUE', 'PINK']
prizes = [5, 3, 4, 1, 0, 10, 2]
colors = list(map(lambda c: Window.COLORS[c], color_keys))

# status: we don't want to start spinning if we're already spinning
spinning = False

# we're going to have the wheel spin faster/longer if the space bar was held down longer
start_time = time.clock()
duration = time.clock() - start_time

# run loop
while True:
    window.refresh()
    window.draw_wheel(colors, 0)
    window.draw_prizes(colors, prizes)
    window.show()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif not spinning and event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            # SPACE bar was pressed
            start_time = time.clock()
        elif not spinning and event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
            # SPACE bar was released
            # let's spin the wheel now
            duration = time.clock() - start_time

            min_rotation = 4 * pi
            dur_rotation = 3 * max(0.75, random.random()) * min(duration, 3) * pi

            theta = min_rotation + dur_rotation
            rotation = 0

            while rotation < theta:

                window.draw_wheel(colors=colors, rotation=rotation)
                window.draw_prizes(colors, prizes)
                window.show()
                window.refresh()
                rotation += max(0.03, 0.40 * (1 - rotation/theta))

            spinning = False
            time.sleep(5)
        else:
            # ignore all other events
            pass
    window.show()
