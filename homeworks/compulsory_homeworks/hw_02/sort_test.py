import unittest
import random

from homeworks.compulsory_homeworks.hw_02.sort import find_minimum, find_maximum, sort_numbers


class TestMatrixOperations(unittest.TestCase):

    def test_min(self):
        """
        tests min function
        """
        length = random.randint(1, 100)
        numbers = [random.randint(1, 100) for _ in range(length)]
        python_solution = min(numbers)
        your_solution = find_minimum(numbers)
        self.assertTrue((python_solution == your_solution), f"incorect min implementation")

    def test_max(self):
        """
        tests max function
        """
        length = random.randint(1, 100)
        numbers = [random.randint(1, 100) for _ in range(length)]
        python_solution = max(numbers)
        your_solution = find_maximum(numbers)
        self.assertTrue((python_solution == your_solution),
                        f"incorect max implementation")


    def test_sort(self):
        """
        test solving of a matrix equation with varying inputs
        """
        length = random.randint(1, 100)
        numbers = [random.randint(1, 100) for _ in range(length)]
        python_solution = sorted(numbers)
        your_solution = sort_numbers(numbers)
        self.assertTrue((python_solution == your_solution),
                        f"incorect sort implementation")


if __name__ == "__main__":
    unittest.main()
