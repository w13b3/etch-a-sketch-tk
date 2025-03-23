from typing import List, Tuple, SupportsFloat
import math


class Circle:
    def __init__(self, polygon: List[Tuple[SupportsFloat, SupportsFloat]]):
        x_coords, y_coords = zip(*polygon)
        self.x = sum(x_coords) / len(polygon)
        self.y = sum(y_coords) / len(polygon)
        self.radius = max(math.dist((self.x, self.y), point) for point in polygon)

    @property
    def center(self) -> Tuple[float, float]:
        return self.x, self.y

    def contains(self, point: Tuple[SupportsFloat, SupportsFloat]) -> bool:
        return math.dist(point, self.center) <= self.radius


def circle_polygon(radius: int | float = 30, num_points: int = 36) -> List[Tuple[int | float, int | float]]:
    polygon = []

    for i in range(num_points):
        angle = 2 * math.pi * i / num_points
        center_x = (math.cos(angle) * radius) + radius  # offset the middle of the circle amount of the radius
        center_y = (math.sin(angle) * radius) + radius
        polygon.append((round(center_x, 2), round(center_y, 2)))

    return polygon


def circle_saw_polygon(
    outer_radius: int | float = 30, inner_radius: int | float = 25, num_teeth: int = 50
) -> List[Tuple[int | float, int | float]]:
    polygon = []
    angle_step = (2 * math.pi) / (num_teeth * 2)

    for i in range(num_teeth * 2):
        angle = i * angle_step
        if i % 2 == 0:
            # Tooth tip
            x = (outer_radius * math.cos(angle)) + outer_radius
            y = (outer_radius * math.sin(angle)) + outer_radius
        else:
            # Tooth valley
            x = (inner_radius * math.cos(angle)) + outer_radius
            y = (inner_radius * math.sin(angle)) + outer_radius
        polygon.append((round(x, 2), round(y, 2)))

    return polygon

if __name__ == '__main__':
    circle_saw_polygon(3, 2, num_teeth=5)