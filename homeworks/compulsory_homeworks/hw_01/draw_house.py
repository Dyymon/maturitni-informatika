
height = int(input())
width = int(input())

assert width % 2 == 0, "size x must be odd"
assert width <= 20 and height <= 20, "maximal size is 20!"
assert width >= 2 and height >= 2, "minimal size is 2!"

house_floor = "_"
house_wall = "|"
roof_left = "/"
roof_right = "̈́\\"  # this will give you a singular \ as \ is reserved as an escape char