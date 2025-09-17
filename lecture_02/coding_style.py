
# it is important to specify the input types of the functions
def fisrt_function(number: int, decimal: float, text: str, array: list):
    print(f"{number} * {decimal} = {number * decimal}")
    print("my text is: ", text)
    print("my array is: ", array)

# not only the input types can be specified but also the output types
def second_function(number: float) -> float:
    return number ** 2

# it is also important to make a propper documentations for all the functions
def third_function(x: float) -> float:
    """
    this function computes mathematical equation y = x**2

    :param x: float to be inputted into the equation
    :return: float result of the equation
    """

    return x ** 2


# this if prevent running your script when the functions are called from a different file
if __name__ == "__main__":
    fisrt_function(15, 0.5, "hello world!", [0,1,2,3])
    print("second function is: ", second_function(2))
