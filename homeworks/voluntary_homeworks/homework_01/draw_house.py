
def draw_house(width: int, height: int) -> None:
    """
    This function draws a house out of a simple ASCII characters

    :param width: width of the house, maximum 20, min 2, must be odd
    :param height: height of the base of the house, max 20, min 2
    """
    # asserts for the input
    assert width % 2 == 0, "size x must be odd"
    assert width <= 20 and height <= 20, "maximal size is 20!"
    assert width >= 2 and height >= 2, "minimal size is 2!"

    space = " "
    house_floor = "_"
    house_wall = "|"
    roof_left = "/"
    roof_right = "̈́\\" # this will give you a singular \ as \ is reserved as an escape char


if __name__ == "__main__":
    draw_house(20, 20)