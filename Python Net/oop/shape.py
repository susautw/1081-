from abc import ABC, abstractmethod


class Shape(ABC):

    @abstractmethod
    def render(self) -> None:
        pass

    @abstractmethod
    def area(self) -> float:
        pass

    @abstractmethod
    def perimeter(self) -> float:
        pass
