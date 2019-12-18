from typing import List

from oop.Rectangle import Rectangle
from oop.Triangle import Triangle
from oop.circle import Circle
from oop.shape import Shape


class Main:
    @staticmethod
    def main():
        shapes: List[Shape] = [Circle(12), Rectangle(12, 16), Triangle(12, 16, 55)]

        for shape in shapes:
            shape.render()
            print(f'Area: {shape.area()}')
            print(f'Perimeter: {shape.perimeter()}')
            print()
