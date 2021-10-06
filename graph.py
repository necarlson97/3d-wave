import math
import random as rand
from abc import ABC

import noise
import pygame as pg


class Graph(ABC):

    # Just frames since init
    counter = 0

    # Allows user to control wave modes
    mode = 0

    # For debug purposes
    pg.font.init()
    font = pg.font.SysFont('Arial', 30)

    def __init__(self, width=10):
        self.modes = [self.no_wave,
                      self.corner_wave,
                      self.random_jump,
                      self.perlin,
                      self.perlin_sin]
        self.width = width

    def update(self):
        self.counter += 1

        for p in self.points:
            p.update()

        # Perform the wave
        # dependent on the current mode
        self.modes[self.mode]()

    def switch_mode(self, i):
        self.mode = (self.mode + i) % len(self.modes)

    def no_wave(self):
        # do not effect motion
        pass

    def corner_wave(self):
        # Here we oscilate a single point
        # by a sine wave
        p = self.points[0]
        wave = math.sin(self.counter * .1) * 50
        p.pos[1] = wave
        p.dpos[1] = 0

    def perlin(self):
        # Use 2d perlin noise on one edge to create wave
        for i in range(self.width):
            p = self.points[i]
            x, y, z = p.pos
            wx, wy = z * .01, self.counter * .01
            wave = noise.pnoise2(wx, wy) * 70
            p.pos[1] = wave
            p.dpos[1] = 0

    def perlin_sin(self):
        # Use perlin, but oscillate strength with sin
        self.perlin()
        for i in range(self.width):
            p = self.points[i]
            p.pos[1] *= math.sin(self.counter * .1)

    def random_jump(self):
        # Select a random point,
        # and disturbe it randomly
        p = rand.choice(self.points)
        p.dpos[1] = rand.randint(-10, 10)

    def render(self, s):
        for p in self.points:
            p.render(s)
        self.render_mode(s)

    def post_render(self, s):
        for p in self.points:
            p.post_render(s)

    def render_mode(self, s):
        name = self.modes[self.mode].__name__
        ts = self.font.render(f'{name}', False, (255, 255, 255))
        s.blit(ts, (700, 700))
