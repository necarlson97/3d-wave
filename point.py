import pygame as pg
import math


class Point():
    # TODO mass currently unused
    mass = 1

    # How velocity slows over time
    dampening = .99

    # How much sway neighbors have over me
    tension = .01

    # Color of top
    color = (10, 200, 200)
    # Color of floor
    floor_color = (50, 50, 50)
    # TODO ohhh dist_color should interpolate
    # between these

    # Decide wether to render isographic, or flat
    iso = False

    # TODO make these dynamic
    # offsets so 0, 0 can be the middle of the screen
    x_offset = 500
    y_offset = 400

    # Static counter that gets incremented
    # to give each point an id of sorts
    counter = 0

    # For debug purposes
    pg.font.init()
    font = pg.font.SysFont('Arial', 30)

    def __init__(self, pos=None, nei=None):
        # x, y, z positioning
        self.pos = pos if pos else [0, 0, 0]
        # Just for reference when rendering
        self.floor_pos = [0, 0, 0]
        # floor x and z match, but y is lower
        for i in range(3):
            self.floor_pos[i] = self.pos[i]
        self.floor_pos[1] = self.pos[1] + 50

        # Velocity for the 3 coords
        self.dpos = [0, 0, 0]

        # Neighboring points this is connected to
        self.nei = nei if nei else []

        # Get an id from static counter, and inc counter
        self.id = Point.counter
        Point.counter += 1

    def update(self):
        self.propegate()
        for i in range(3):
            self.dpos[i] *= self.dampening
            self.pos[i] += self.dpos[i]

    def propegate(self):
        # Get the average y pos of all my neighbors
        ys = [n.pos[1] for n in self.nei]
        avg_y = sum(ys) / len(ys)
        # Get the distanc between myself and my target
        dist = avg_y - self.pos[1]
        # Alter velocity
        self.dpos[1] += self.tension * dist

    def render(self, s):
        # distance between self and floor
        dist = self.floor_pos[1] - self.pos[1]
        dist = 2 * (100 - dist)
        dist_color = (20, dist % 255, 255)

        # lines to floor
        # self.render_floor_wire(s, dist_color)

        # surface texture
        self.render_side_filled(s, dist_color)

    def post_render(self, s):
        # TODO need to create utility space
        # for things like Game.dev

        # exact circles for floor and surface
        self.render_circles(s)

        self.render_id(s)

    def render_id(self, s):
        ts = self.font.render(f'{self.id}', False, (255, 255, 255))
        s.blit(ts, self.flatten())

    def render_side_filled(self, s, dist_color):
        if len(self.nei) < 2:
            return
        ns = len(self.nei)
        for i in range(ns):
            # Get the next pair of neis (and self) 
            # TODO could pre-calc
            poly_points = [self,
                           self.nei[i],
                           self.nei[(i + 1) % ns]]
            poly_pos = [p.pos for p in poly_points]
            # Create and draw triangle
            fps = [self.flatten(p) for p in poly_pos]
            pg.draw.polygon(s, dist_color, fps)

    def render_floor_filled(self, s, dist_color):
        poly_pos = [self.pos, self.floor_pos,
                    self.nei[0].floor_pos,
                    self.nei[0].pos]
        fps = [self.flatten(p) for p in poly_pos]
        pg.draw.polygon(s, dist_color, fps)

    def render_floor_wire(self, s, dist_color):
        # flattened 2d int representation of
        # self and floor
        flat_p = self.flatten()
        flat_fp = self.flatten(self.floor_pos)

        # draw connecting line
        pg.draw.line(s, dist_color, flat_p, flat_fp, 5)

    def render_circles(self, s):
        flat_p = self.flatten()
        flat_fp = self.flatten(self.floor_pos)

        # draw floor
        pg.draw.circle(s, self.floor_color, flat_fp, 5)
        # draw top
        pg.draw.circle(s, self.color, flat_p, 5)

    def flatten(self, pos=None):
        # default to self.pos for position
        if not pos:
            pos = self.pos
        # render isometric if this is 3d
        if self.iso:
            return self.flatten3d(pos)
        # otherwise return 2d
        return self.flatten2d(pos)

    def flatten2d(self, pos):
        x, y, z = pos
        x = int(x + self.x_offset)
        y = int(y + self.y_offset)
        return [x, y]

    def flatten3d(self, pos, angle=math.radians(-30)):
        # takes a 3d point thruple
        # and turns it into the
        # isometric 2d tuple
        a = angle
        ISO_ANGLE = math.radians(120)

        x, y, z = pos
        draw_x = x * math.cos(a)
        draw_x += y * math.cos(a + ISO_ANGLE)
        draw_x += z * math.cos(a - ISO_ANGLE)

        draw_y = x * math.sin(a)
        draw_y += y * math.sin(a + ISO_ANGLE)
        draw_y += z * math.sin(a - ISO_ANGLE)

        # We are drawing with 0, 0, 0 being the center of the viewport
        # TODO make this based on viewport, not hardcoded
        draw_x += 500
        draw_y += 400

        return (int(draw_x), int(draw_y))

    def __str__(self):
        # TODO better
        return f'{self.id}'

    def __repr__(self):
        # TODO not repr
        return self.__str__()


def generate_point_line(width, seperation=50):
    # Generate a line of points
    # just tuples of x, y
    # the y is kept constant
    # we want the center to be at 0, 0, 0

    s = seperation
    w = width

    points = []
    for i in range(w):
        x = (i - w / 2) * s
        y = 0

        # x, y, z position
        pos = [x, y, 0]

        p = Point(pos)
        points.append(p)

    # assign neighbors
    for i in range(w):
        p = points[i]
        nei_idxs = [n for n in [i - 1, i + 1]
                    if n >= 0 and n < width]
        p.nei = [points[i] for i in nei_idxs]

    return points


def generate_point_plane(width, seperation=15):
    # Generate a flat field of points
    # just a thruple of x, y, z
    # the y is kept constant
    # we want the center to be at 0, 0, 0

    # TODO CLASS UP POINTS

    s = seperation
    w = width

    point_matrix = {}
    for r in range(w):
        point_matrix[r] = {}
        for c in range(w):
            x = (r - w / 2) * s
            y = 0
            z = (c - w / 2) * s
            # x, y, z position
            pos = [x, y, z]

            p = Point(pos)
            point_matrix[r][c] = p

    # assign neighbors
    points = []
    for r in range(w):
        for c in range(w):
            p = point_matrix[r][c]
            # all possible neighbors
            # NOTE: order does matter, as they
            # are rendered 'clockwise'
            nei_idxs = [(r-1, c), (r, c+1),
                        (r+1, c), (r, c-1)]
            # filter out non-existing ones
            nei_idxs = [(r, c) for r, c in nei_idxs
                        if r >= 0 and r < width
                        and c >= 0 and c < width]
            p.nei = [point_matrix[r][c] for r, c in nei_idxs]
            points.append(p)

    points.reverse()
    return points
