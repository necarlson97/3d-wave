from point import Point, generate_point_plane
from graph import Graph


class Net(Graph):

    def __init__(self, width=30):
        super().__init__(width)
        # Points are 3d, so we want to draw
        # isometrically

        Point.tension = .025

        # Can change damening / tension here too

        Point.iso = True
        self.points = generate_point_plane(width)
