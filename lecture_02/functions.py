
# we are already using functions for example print() is a function that will print its input
# or len() which will return a number, specifically length of a given array
# lets make our first function then
# lets make a function that will simply print "hello world"

def hello_world(): # every function has a header
    print("hello world") # and its code inside

hello_world()

# this is a no input and no output function, its only function is to print into terminal
# functions as we know from the print() function can have inputs, lets make one
# lets make a function that greets someone depending on their name

pepa = "Pepa"

def greeting(name): # in the header we add the input variable, that we use in function
    print(f"Hello {name}") # f"{x}" is another way how to add variable into a text

greeting(pepa)

# we can ofcourse have multiple number of inputs

david = "david"
def greetings(name_1, name_2):
    print(f"Hello {name_1} and {name_2}")

greetings(david, pepa)

# functions can also have an output, lets make a simple mathematical function y = x**2

def function(x):
    y = x**2
    return y

solution = function(5)
print(solution)

# even multiple inputs

def function_3d_polynomial(x, y):
    z = x**2 + y + 1
    return z

# and of course, multiple inputs and outputs
def quadratic_and_partial_derivates(x, y):
    z = x**2 + y**2
    d_x = 2*x
    d_y = 2*y

    return z, d_x, d_y

solution = quadratic_and_partial_derivates(2, 3)
print(solution)

# the output type of a function with multiple outputs is a tuple a type of an array
# tuple behaves similarly to a string as it allows us to ask for a specific index
print(solution[0])

# but it won't allow us to rewrite its parts
# solution[0] = 15

# you can also divide the outputs in the following way to have separate outputs not in tuple
# you can additionally ignore and output with _

z, dx, _ = quadratic_and_partial_derivates(4, 10)
print(f"z = {z}\n" #\n will give us new line in the terminal
      f"dx = {dx}\n")

# of course functions can be as complicated as you want

def my_function(plot_range, step=0.1): # specifying value in a header means that if you don't give it any it will use this one
    plots = [] # we create an empty list
    for i in range(-plot_range, plot_range + 1):
        x = i * step
        y = x**2
        plots.append(y) # you can add into an empty list values this way

    return plots

print(my_function(10))








