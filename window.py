from math import sin, cos, pi
import random
import time
import winsound
import pygame
import pygame.gfxdraw
pygame.init()


class Window:
    COLORS = {
        'BLACK': pygame.Color(0, 0, 0),
        'WHITE': pygame.Color(255, 255, 255),
        'RED': pygame.Color(255, 0, 0),
        'GREEN': pygame.Color(0, 255, 0),
        'BLUE': pygame.Color(0, 0, 255),
        'YELLOW': pygame.Color(255, 255, 0),
        'PINK': pygame.Color(255, 0, 255),
        'CYAN': pygame.Color(0, 255, 255),
        'ORANGE': pygame.Color(255, 128, 0)
    }

    def __init__(self, width, height, bg_color, caption):
        # initialize window
        self.size = (width, height)
        self.screen = pygame.display.set_mode(self.size)

        # set window title
        pygame.display.set_caption(caption)
        pygame.display.set_icon(pygame.image.load('LAB_Logo_icon.png'))

        # background
        self.background = pygame.Surface(self.size)
        self.background.fill(bg_color)
        self.refresh()

        # circle radii
        self.oradius = int(0.85 * min(self.size)//2)
        self.iradius = int(0.2 * self.oradius)

        # rectangle bounding the outer circle
        self.orect = pygame.Rect(self.translate(-self.oradius, -self.oradius),
                                 (2*self.oradius, 2*self.oradius))

        # font
        self.font = pygame.font.Font('palai.ttf', self.size[1] // 10)

        # pointer color (used for sfx)
        self.pointer_color = None

    @staticmethod
    def show():
        pygame.display.flip()

    def refresh(self):
        """ refresh the screen by redrawing the background """
        self.render(self.background, (0, 0))

    def render(self, obj, loc):
        """ render object <obj> at location <loc = x, y>"""
        self.screen.blit(obj, loc)

    def translate(self, x, y):
        """ give the absolute coordinates of a point measured from the center """
        return int(self.size[0]/2 + x), int(self.size[1]/2 + y)

    def fill_arc(self, center, radius, theta0, theta1, color):
        ndiv = 5000
        d_theta = (theta1 - theta0) / ndiv

        cx, cy = center

        for i in range(ndiv):
            x = cx + radius * cos(theta0 + i*d_theta)
            y = cy + radius * sin(theta0 + i*d_theta)

            pygame.draw.line(self.screen,
                             color,
                             self.translate(*center),
                             self.translate(x, y),
                             3)

    def draw_pointer(self):
        p1 = self.translate(-0.1 * self.oradius, -1.1 * self.oradius)
        p2 = self.translate(0.1 * self.oradius, -1.1 * self.oradius)
        p3 = self.translate(0, -0.8 * self.oradius)

        color = self.screen.get_at(self.translate(0, -0.8 * self.oradius))

        if self.pointer_color is not None and self.pointer_color != color:
            winsound.Beep(440, 100)

        pygame.gfxdraw.filled_trigon(
            self.screen,
            *p1, *p2, *p3,
            self.screen.get_at(self.translate(0, -0.8 * self.oradius))
        )

        self.pointer_color = self.screen.get_at(self.translate(0, -0.8 * self.oradius))

        pygame.gfxdraw.trigon(
            self.screen,
            *p1, *p2, *p3,
            Window.COLORS['BLACK']
        )

    def draw_wheel(self, colors, rotation=0):
        phi = 2*pi / len(colors)  # angle width of each sector

        # draw arcs
        for i, color in enumerate(colors):
            self.fill_arc(center=(0, 0),
                          radius=self.oradius,
                          theta0=i*phi+rotation,
                          theta1=(i+1)*phi+rotation,
                          color=color)

        # draw center circle
        pygame.draw.circle(self.screen,
                           Window.COLORS['BLACK'],
                           self.translate(0, 0),
                           self.iradius)

        self.draw_pointer()

    def draw_prizes(self, colors, prizes):
        for i, (color, prize) in enumerate(zip(colors, prizes)):
            text = self.font.render(str(prize), True, color, None)
            self.render(text, self.translate(-1.5*self.oradius, -self.oradius + i*self.size[1] // 10))
