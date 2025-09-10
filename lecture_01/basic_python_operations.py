
# assigning values to variables a and b
a = 4
b = 4

# simple Pythagoras equation c = (a^2 + b^2)^(1/2)
# for multiplication use *
# for division use /
# for power use **
# use brackets () similarly to math
c = (a**2 + b**2)**0.5

# we can print the result into the python shell
print("the result of c = (a**2 + b**2)**0.5 is:")
print(c)

# lets reassign value to c
c = 2

# we can add 1 to c simply by
c = c + 1
print("by running c = c + 1 we get:")
print(c)

# or by the reduced version
c += 1
print("by running c += 1 we get:")
print(c)

# we can do that for multiplication as well
c *= 2
print("by running c *= 2 we get:")
print(c)

# even division
c /= 2
print("by running c /= 2 we get:")
print(c)

# in python as in any other programing language we can create an array, collection of several items, in python its called list
arr = [0, 1, 2, 3]
print("printing an array")
print(arr)

# we can access these items in a following way
print("printing list elements")
print(arr[0])
print(arr[1])
print(arr[2])
print(arr[3])

# if can also do it from the opposite direction, calling arr[-1] will give you the last item of the list
print("printing an list elements again backwards")
print(arr[-1])
print(arr[-2])
print(arr[-3])
print(arr[-4])

# if yoy want to know the length of an list simply run the following command
length = len(arr)
print("printing the list length")
print(length)

# we can even reassign values to lists
arr[0] = 100
print("showing reassigned value in list")
print(arr)

# we can store more than just numbers into variables an lists
word = "python"
print("we can store words into variables, here we print a variable called word")
print(word)

# we can store words, or as they are called in the programing lingo, strings into lists as well
arr = ["hello", "world", "!"]
print("printing a list with strings")
print(arr)

# these string can be accessed element wise similarly as a list can be
print("printing a string element wise")
print(word[0])
print(word[1])
print(word[2])

# you can show only portion of a list or a string
print("here you can see an example of printing all elements up to the second index:")
print(arr[:2])
print("here you can see an example of printing all elements from the third index:")
print(word[3:])
print("and of course you can combine these:")
print(word[2:5])

# essentially strings a list behave very similarly
print("printing list and stringth length and reassigning value")
print(len(word))
print(len(arr))
# however string does not support item assignment like a list does!

# finally you can assign to list item an list item
arr1 = [1, 2, 3]
arr2 = [4, 5, 6]
arr[0] = arr1
arr[1] = arr2
print("printing a list with lists")
print(arr)

# to get to their values you have to call
print("printing an elements of list in list")
print(arr[0][0])
print(arr[0][1])
print(arr[0][2])
