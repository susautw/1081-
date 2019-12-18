import math
from dataclasses import dataclass

from .shape import Shape


@dataclass
class Triangle(Shape):
    a: float
    b: float
    c: float

    def render(self) -> None:
        print(f'There is a triangle with edges({self.a}, {self.b}, {self.c})')

    def area(self) -> float:
        s = self.a + self.b + self.c / 2
        return math.sqrt(s * (s - self.a) * (s - self.b) * (s - self.c))

    def perimeter(self) -> float:
        return self.a + self.b + self.c
