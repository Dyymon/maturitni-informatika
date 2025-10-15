def add_matrix(A: list[list[float]], B: list[list[float]]) -> list[list[float]]:
    """
    Takes two matrices and adds them together as such A + B. More on matrix addition on https://en.wikipedia.org/wiki/Matrix_addition
    :param A: list of lists of floats representing a matrix, sublist represents a row
    :param B: list of lists of floats representing a matrix, sublist represents a row
    :return: the result of addition of two matrices, list of lists of floats representing a matrix, sublist represents a row
    """
    C = [[]]

    return C


def multiply_matrix(A: list[list[float]], B: list[list[float]]) -> list[list[float]]:
    """
    takes two matrices and multiplies them together as such A @ B. More on matrix multiplication https://en.wikipedia.org/wiki/Matrix_multiplication
    :param A: list of lists of floats representing a matrix, sublist represents a row
    :param B: list of lists of floats representing a matrix, sublist represents a row
    :return: the result of multiplication of two matrices, list of lists of floats representing a matrix, sublist represents a row
    """
    C = [[]]

    return C


def solve(equation: list[str | list[list[float]]]) -> list[list[float]]:
    """
    takes an argument list of either matrices or strings ie [A, "+", B "@", C, ... "-", Z]
    where A, B, ..., Z are matrices represented as list of lists of floats.
    This function will than calculate the given input ie. A + B @ C ... - Z and will return the result
    :param equation: list of either strings representing a mathematical operation, or list of list of floats representing a matrix.
    :return: the result of solving the input equation, list of lists of floats representing a matrix, sublist represents a row
    """
    solution = [[]]

    return solution


if __name__ == "__main__":
    A = [[1, 2, 3], [4, 5, 6]]
    B = [[7, 8, 9], [10, 11, 12]]

    C = add_matrix(A, B)
    print(C)

    A = [[1, 2, 3], [4, 5, 6]]
    B = [[7], [8], [9]]
    C = multiply_matrix(A, B)
    print(C)

    A = [[1, 2, 3], [4, 5, 6]]
    B = [[7, 8, 9], [10, 11, 12]]
    C = [[1, 2, 3], [4, 5, 6]]
    solution = solve([A, "+", B, "@", C])
    print(solution)
