from typing import Any
from heuristics.HeuristicsDefinitions import HeuristicsStrategy


class Heuristic:

    def __init__(self, data: dict, start: str, goal: str, h: str) -> None:
        self.heuristics = HeuristicsStrategy()
        self.dictionary = data
        self.start = start
        self.goal = goal
        self.h_choice = h

    def process(self, data, n, b) -> Any:
        return self.heuristics.definitions[self.h_choice](data, n, b)
