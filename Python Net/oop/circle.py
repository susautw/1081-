import math
from dataclasses import dataclass

from .shape import Shape


@dataclass
class Circle(Shape):
    radius: float

    def render(self) -> None:
        print(f'There is a circle with radius {self.radius}')

    def area(self) -> float:
        return self.radius ** 2 * math.pi

    def perimeter(self) -> float:
        return self.radius * 2 * math.pi
