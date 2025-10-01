# python as any programing language uses libraries, we can import libraries using the import command
# we have python basic libraries and libraries that needs to be installed
# lets try importing one of the basic python libraries math
# this library has various math functions and tools

import math

a = math.sin(1) # calculates sin of given number
print("sin of 1 is: ", a)

print("pi is: ", math.pi) # gives you the number pi

print("inf is: ", math.inf) # makes fictive inf number that behaves like infinite

# this next library is also python standard library with useful time tools

import time

curr_time = time.time() # will give you current time
print("current time: ", curr_time)

time.sleep(1) # will make the program sleep for one second

print("passed time: ", time.time() - curr_time)

# there are many more libraries you can learn more at https://docs.python.org/3/tutorial/stdlib.html

# these libraries might not be sufficient for our needs and sometimes we have to look elsewhere
# our option is to install additional libraries using pip
# on how to install these libraries take a look onto lecture_03/README.md

# numpy is one of the most used libraries in python, it has many numerical and matrix operations
# here we can also see a way how we can additionally shorten the import name by adding as np
import numpy as np

A = np.array([[0,1,2,],[2,5,4],[2,5,4]])
b = np.array([[3,4,5]])
print("A: ")
print(A)
print("b: ")
print(b)
print("A * b: ")
print(A * b)

# there are also libraries used for ploting data such as matplotlib

import matplotlib.pyplot as plt

# Generate x values
x = np.linspace(0, 2 * np.pi, 500)

# Compute y values for sine
y = np.sin(x)

# Plot the sine function
plt.plot(x, y, label="sin(x)")
plt.title("Sine Function")
plt.xlabel("x (radians)")
plt.ylabel("sin(x)")
plt.legend()
plt.grid(True)
plt.show()