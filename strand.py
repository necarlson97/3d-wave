from point import generate_point_line
from graph import Graph


class Strand(Graph):

    def __init__(self, width=19):
        super().__init__(width)
        self.points = generate_point_line(width)
