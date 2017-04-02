""" main program """

# import internal modules
from wheel import Wheel

# import stdlib
import random
import colorsys
from winsound import Beep
import collections
import argparse
import time
import sys

# import non-standard libraries
import pygame
pygame.init()


# initialize colors
def init_colors(ncolors):
    """
    Generate colors across the spectrum and return a list of RGB tuples

    Step 1: Generate `ncolors` colors in HSB-space with coordinates between 0 and 1
    Step 2: Use colorsys.hsv_to_rgb(h, s, v) to convert to RGB-space with coordinates between 0 and 1
    Step 3: Map [0, 1] to [0, 255] by multiplying by 255 (and converting to integers)

    :param ncolors: the number of colors to generate
    :return: a list of tuples (R, G, B); 0 <= R, G, B <= 255
    """

    return list(map(lambda c: (int(255*c[0]), int(255*c[1]), int(255*c[2])),
                    [colorsys.hsv_to_rgb(i/ncolors, 1, 1) for i in range(ncolors)]))


# parse sys.argv
def parse_args():
    parser = argparse.ArgumentParser(prog='wheel_spin.py', description='Create a wheel-spin game.')

    # get ticket values
    parser.add_argument('-tickets', nargs='+', type=int, action='store', default=[1, 2, 3, 4, 5, 6, 7],
                        help='The ticket values for each sector of the wheel.')

    # parse size
    parser.add_argument('--x', action='store', type=int, default=1200, help='size of the window: x')
    parser.add_argument('--y', action='store', type=int, default=900, help='size of the window: y')

    # randomize prizes?
    # NOTE 1: 'store_false' creates the flag with a default of True
    # NOTE 2: confusion may arise here because, although RANDOM is the default behavior, we are
    #         passing in the NO RANDOM flag. As such, we want dest=random to be True when we DON'T
    #         pass in this flag. This is why we default to True (see note 1)
    parser.add_argument('--nr', '--norandom', action='store_false', dest='random',
                        help='flags that prizes should not be in a random order [default behavior: RANDOM]')

    # beep for each ticket won?
    # See notes to `randomize prizes?`
    parser.add_argument('--nb', '--nobeep', action='store_false', dest='beep',
                        help='flags that the program should not beep for every ticket won [default behavior: BEEP]')

    # should the window be fullscreen?
    # see notes to `randomize prizes?`
    parser.add_argument('--nofullscreen', '--nfs', '--windowed', '--w', action='store_false', dest='fullscreen',
                        help='flags that the window should not be in fullscreen [default behavior: FULLSCREEN]')

    return parser.parse_args(sys.argv[1:])


# initialize font
def init_font(window_size, colors):
    font_size = int(0.8 * window_size[1] / len(colors))
    return font_size, pygame.font.Font('palai.ttf', font_size)


# MAIN
def main():
    # ------------------------------
    # ---- INIT
    # ------------------------------
    args = parse_args()

    size = args.x, args.y
    screen = pygame.display.set_mode(size, pygame.FULLSCREEN if args.fullscreen else 0)
    radius = int(0.4 * min(size))

    # colors = init_colors()

    ticket_values = args.tickets
    if args.random:
        random.shuffle(ticket_values)

    colors = init_colors(ncolors=len(ticket_values))

    prizes = collections.OrderedDict(zip(colors, ticket_values))

    font_size, font = init_font(size, prizes.keys())

    res_font_size = size[1] // 10
    res_font = pygame.font.Font('palai.ttf', res_font_size)

    wheel_pos = size[0]//3 - radius, int(size[1]//2 - 1.1 * radius)
    wheel = Wheel(radius=radius, colors=prizes.keys())

    # -------------------------------
    # ---- THE LOOP
    # -------------------------------

    active = False
    while True:
        screen.fill(pygame.Color(0, 0, 0))
        wheel.draw(screen, wheel_pos)

        # draw prizes
        for i, color in enumerate(prizes.keys()):
            prize = prizes[color]
            x = font.render(str(prize), True, color, None)
            screen.blit(x, (int(radius * 2.5), i * font_size))

        pygame.display.flip()  # show()

        start_time = time.clock()
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit(0)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                start_time = time.clock()
                active = True
            elif event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                # spin the wheel
                active = False
                duration = time.clock() - start_time

                min_speed = 0.08
                dur_speed = max(0.5 + random.random(), 1) * max(0.5 + random.random(), 1) * max(duration ** 2, 3) * 0.01
                alpha = -0.0001

                wheel.spin(screen, wheel_pos, min_speed + dur_speed, alpha)

                # handle displaying prizes
                color = tuple(wheel.pointer.get_at((0, 0)))[:-1]  # oolor is RGBA... discard alpha=255
                if args.beep:
                    for _ in range(prizes[color]):
                        Beep(660, 200)

                reward = prizes[color]
                text = 'You win {n} ticket{s}!'.format(n=reward, s='' if reward == 1 else 's')
                x = res_font.render(text, True, color, None)
                screen.blit(x, (size[0]//100, size[1] - res_font_size))

                pygame.display.flip()
                time.sleep(3)

                pygame.event.clear()  # prevent buffering an input

        if active:
            wheel.theta -= 0.01


if __name__ == '__main__':
    main()
