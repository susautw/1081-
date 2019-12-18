from dataclasses import dataclass

from .shape import Shape


@dataclass
class Rectangle(Shape):
    width: float
    height: float

    def render(self) -> None:
        print(f'There is a rectangle with width {self.width} and height {self.height}')

    def area(self) -> float:
        return self.width * self.height

    def perimeter(self) -> float:
        return 2 * (self.width + self.height)
