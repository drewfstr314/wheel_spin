from math import cos, sin, pi, degrees
from winsound import Beep
import pygame
import pygame.gfxdraw
pygame.init()


class Wheel:
    def __init__(self, radius, colors):
        self.colors = list(map(lambda c: pygame.Color(c[0], c[1], c[2]), colors))
        self.radius = radius
        self.theta = 0

        self.surface = self.init_surface()
        self.pointer = self.init_pointer()

    def init_surface(self):
        surface = pygame.Surface((2 * self.radius, 2 * self.radius))  # circum-square

        phi = 2 * pi / len(self.colors)  # angle measure of each sector

        # draw the sectors
        for i, color in enumerate(self.colors):
            self.fill_pie(dest=surface, x=self.radius, y=self.radius, r=self.radius,
                          start=i*phi, end=(i+1)*phi, color=color)

        # draw center circle
        pygame.draw.circle(surface, pygame.Color(0, 0, 0), (self.radius, self.radius), self.radius // 5)

        return surface

    def init_pointer(self):
        pointer = pygame.Surface((self.radius//20, self.radius//9))
        pointer.fill((255, 255, 255))
        return pointer

    @staticmethod
    def fill_pie(dest, x, y, r, start, end, color, ndiv=75):
        """
        akin to pygame.gfxdraw.pie(Surface, x, y, r, start, end, color)
        https://www.pygame.org/docs/ref/gfxdraw.html

        but uses radians meausuring counterclockwise from east

        the sector is filled in using pygame.gfxdraw.filled_polygon(), using `ndiv`
        points along the circumference of the circle
        """
        dt = (end - start) / ndiv
        angles = [start + i * dt for i in range(ndiv + 1)]  # using ndiv leaves a gap between adjacent arcs

        points = [(x, y)] + [(x + r * cos(t), y - r * sin(t)) for t in angles]

        pygame.gfxdraw.filled_polygon(dest, points, color)

    def rotate(self, theta):
        """
        rotate the wheel by angle theta (measured in radians)
        positive theta is a counterclockwise rotation

        [adapted from https://www.pygame.org/wiki/RotateCenter]
        """
        orig_rect = self.surface.get_rect()
        rot_image = pygame.transform.rotate(self.surface, degrees(theta))

        rot_rect = orig_rect.copy()
        rot_rect.center = rot_image.get_rect().center
        rot_image = rot_image.subsurface(rot_rect).copy()

        return rot_image

    def update_pointer(self):
        color = self.rotate(self.theta).get_at((self.radius, self.radius // 2))

        if color != self.pointer.get_at((0, 0)):
            Beep(440, 1)
            self.pointer.fill(color)

    def draw(self, screen, wheel_pos):
        pointer_pos = (
            wheel_pos[0] + self.radius - self.pointer.get_bounding_rect().size[0],
            wheel_pos[1] - self.radius // 10
        )

        self.update_pointer()
        screen.blit(self.pointer, pointer_pos)
        screen.blit(self.rotate(self.theta), wheel_pos)

    def spin(self, screen, wheel_pos, omega, alpha):
        """
        spin the wheel
        :param screen: the screen to draw the wheel on
        :param wheel_pos: the location on the screen to draw the wheel
        :param omega: the initial angular velocity
        :param alpha: the (de)-acceleration of the wheel
        """
        while omega > 0:
            omega += alpha
            self.theta = (self.theta + omega) % (2 * pi)

            self.draw(screen, wheel_pos)
            pygame.display.flip()
