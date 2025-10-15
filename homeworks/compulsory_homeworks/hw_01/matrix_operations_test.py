import inspect
import unittest
from random import choice
from copy import deepcopy

import numpy as np

from homeworks.compulsory_homeworks.hw_01.matrix_operations import add_matrix, \
    multiply_matrix, solve


class TestMatrixOperations(unittest.TestCase):

    def test_addition(self):
        """
        tests addition of two matrices
        """

        rows = np.random.randint(1, 5)
        cols = np.random.randint(1, 5)

        A = np.random.randint(0, 10, size=(rows, cols))
        B = np.random.randint(0, 10, size=(rows, cols))

        C_np = A + B
        C_my = add_matrix(A.tolist(), B.tolist())
        self.assertTrue(np.array_equal(C_np, np.array(C_my)),
                        f"Matrix addition failed\n correct result: \n {C_np}\n your result: \n{C_my}")

    def test_multiplication(self):
        """
        tests multiplication of two matrices
        """

        m = np.random.randint(1, 10)
        n = np.random.randint(1, 10)
        p = np.random.randint(1, 10)

        A = np.random.randint(0, 10, size=(m, n))
        B = np.random.randint(0, 10, size=(n, p))

        C_np = A @ B
        C_my = multiply_matrix(A.tolist(), B.tolist())
        self.assertTrue(np.array_equal(C_np, np.array(C_my)),
                        f"Matrix multiplication failed\n correct result: \n {C_np}\n your result: \n{C_my}")

    def test_solve(self):
        """
        test solving of a matrix equation with varying inputs
        """

        rows = np.random.randint(1, 5)
        cols = np.random.randint(1, 5)
        A = np.random.randint(0, 100, size=(rows, cols))
        B = np.random.randint(0, 100, size=(rows, cols))
        C = np.random.randint(0, 100, size=(rows, cols))

        solution_np = A + B - C
        solution_my = np.array(solve([A.tolist(), "+", B.tolist(), "-", C.tolist()]))
        self.assertTrue(np.array_equal(solution_np, solution_my), "incorrect solution for A + B - C")

        solution_np = A @ B @ C
        solution_my = np.array(solve([A.tolist(), "@", B.tolist(), "@", C.tolist()]))
        self.assertTrue(np.array_equal(solution_np, solution_my), "incorrect solution for A @ B @ C")

        solution_np = A + B @ C
        solution_my = np.array(solve([A.tolist(), "+", B.tolist(), "@", C.tolist()]))
        self.assertTrue(np.array_equal(solution_np, solution_my), "incorrect solution for A + B @ C")

        solution_np = A @ B - C
        solution_my = np.array(solve([A.tolist(), "@", B.tolist(), "-", C.tolist()]))
        self.assertTrue(np.array_equal(solution_np, solution_my), "incorrect solution for A @ B - C")

        m = np.random.randint(1, 5)
        n = np.random.randint(1, 5)
        p = np.random.randint(1, 5)
        A = np.random.randint(0, 100, size=(m, n))
        B = np.random.randint(0, 100, size=(n, p))
        C = np.random.randint(0, 100, size=(m, p))

        solution_np = A @ B + C
        solution_my = np.array(solve([A.tolist(), "@", B.tolist(), "+", C.tolist()]))
        self.assertTrue(np.array_equal(solution_np, solution_my), "incorrect solution for A @ B + C")

        m = np.random.randint(1, 5)
        n = np.random.randint(1, 5)
        p = np.random.randint(1, 5)
        q = np.random.randint(1, 5)
        A = np.random.randint(0, 100, size=(m, n))
        B = np.random.randint(0, 100, size=(n, p))
        C = np.random.randint(0, 100, size=(p, q))
        D = np.random.randint(0, 100, size=(m, q))

        solution_np = A @ B @ C + D
        solution_my = np.array(solve([A.tolist(), "@", B.tolist(), "@", C.tolist(), "+", D.tolist()]))
        self.assertTrue(np.array_equal(solution_np, solution_my), "incorrect solution for A @ B @ C + D")

        rows = np.random.randint(1, 5)
        cols = np.random.randint(1, 5)
        A = np.random.randint(0, 100, size=(rows, cols))
        solution_np = deepcopy(A)

        equation = [deepcopy(A)]
        matrix_num = np.random.randint(1, 10)
        for _ in range(matrix_num):
            B = np.random.randint(0, 100, size=(rows, cols))
            if choice([True, False]):
                solution_np = solution_np + B
                equation.append("+")
            else:
                solution_np = solution_np - B
                equation.append("-")

            equation.append(deepcopy(B).tolist())

        solution_my = np.array(solve(equation))
        self.assertTrue(np.array_equal(solution_np, solution_my),
                        "incorrect solution for varying matrix equation + and -")

        m = np.random.randint(1, 5)
        n = np.random.randint(1, 5)
        p = np.random.randint(1, 5)
        A = np.random.randint(0, 100, size=(m, n))
        solution_np = deepcopy(A)
        equation = [deepcopy(A)]
        matrix_num = np.random.randint(1, 10)
        for _ in range(matrix_num):
            B = np.random.randint(0, 100, size=(n, p))
            n = p
            p = np.random.randint(1, 5)
            solution_np = solution_np @ B
            equation.append("@")
            equation.append(deepcopy(B).tolist())


        solution_my = np.array(solve(equation))
        self.assertTrue(np.array_equal(solution_np, solution_my),
                        "incorrect solution for varying matrix equation @")

    def test_imported_modules(self):
        """
        Test that you are not using numpy inside your implementation. Passing by
        default.
        """
        with open(inspect.getfile(add_matrix)) as f:
            self.assertTrue("numpy" not in f.read())


if __name__ == "__main__":
    unittest.main()
