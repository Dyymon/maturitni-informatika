
def fisrt_function(number: int, decimal: float, text: str, array: list):
    print(f"{number} * {decimal} = {number * decimal}")
    print("my text is: ", text)
    print("my array is: ", array)

def second_function(number: float) -> float:
    return number ** 2


if __name__ == "__main__":
    fisrt_function(15, 0.5, "hello world!", [0,1,2,3])
    print("second function is: ", second_function(2))
