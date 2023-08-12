import sys
import os

from src import Instance
from src import Solution
from src import Validator

class Main:
    def __init__(self, instace, solution):
        self.instance = Instance(instace)
        self.solution = Solution(solution)
    
    def validate(self):
        validator = Validator(self.instance, self.solution)

        vertical_cost = validator.compute_vertical_cost()

        horizontal_cost = validator.compute_horizontal_cost()

        print("###### RESULT #####")
        print("Vertical Cost", vertical_cost)
        print("Horizontal Cost", horizontal_cost)
        print("Total Cost", vertical_cost + horizontal_cost)

        validator.validate()

_, _instance, _solution = sys.argv

main = Main(_instance, _solution)

main.validate()