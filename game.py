import pygame as pg
from net import Net
from strand import Strand
from point import Point


class Game():

    bg = (0, 0, 0)
    dev = False

    def __init__(self, display):
        self.display = display

        self.input_objects = []
        # self.update_objects = [Strand()]
        self.update_objects = [Net()]
        self.render_objects = self.update_objects

    def inputs(self, events):
        for e in [e for e in events if e.type == pg.KEYDOWN]:
            k = e.key
            print('Key pressed:', k)

            # one = dev mode
            if k == 49:
                Game.dev = not Game.dev

            # space = reset
            if k == 32:
                self.update_objects = [Net()]
                self.render_objects = self.update_objects

            # two = isometric vs flat
            if k == 50:
                Point.iso = not Point.iso

            # right = inc mode, left = dec mode
            if k == 275:
                self.update_objects[0].switch_mode(1)
            if k == 276:
                self.update_objects[0].switch_mode(-1)

        for io in self.input_objects:
            io.inputs(events)

    def update(self):
        for o in self.update_objects:
            o.update()

    def render(self, s):
        s.fill(self.bg)

        for o in self.render_objects:
            o.render(s)
        if Game.dev:
            for o in self.render_objects:
                if not hasattr(o, 'post_render'):
                    continue
                o.post_render(s)
