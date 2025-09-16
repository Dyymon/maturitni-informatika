
# the most used loop in Python is the for cycle
# this it the most basic for cycle a cycle that will run 10 times
# every time it runs i will get incremented by one untill it reaches 10
# in this case the cycle in each of its cycles prints i as well
for i in range(10):
    print(i)

# now range can be augmented to not only have an end but beginning as well
# now i will start from the number 4 and will go up to 10
for i in range(4, 10):
    print(i)

# additionally we can also specify the step size ie how much i will get incremented
# in this case i goes from 5 to 20 and gets incremented by 3
for i in range(5, 20, 3):
    print(i)

# for cycles can be used in a different way and that is to go through items of a list
# lets have a list arr
arr = ["a", 1, "b", 3, "c", 5, 6, 7, 8, 9]

# we can go through the list by having an i that goes from zero up to the length of arr
for i in range(0, len(arr)):
    print(arr[i])

# or we can go directly through the array, where part is now a specific part of the arr
for part in arr:
    print(part)

# if for any reason we still need the index of the part of the array we can use enumerate
# enumerate gives us both the index numbers of the part and the part as well
for id, part in enumerate(arr):
    print("id: ", id, "part: ", part)

# sometimes we just want a cycle that runs a certain amount of time
# especially in algorithms and we dont care about any indexes
# simpy have
iterations = 100
for _ in range(iterations):
    pass

# now lets look into while loops
# while loops run until a condition is met a condition that is specified in the header
# lets try to recreate a for loop
i = 0 # we need to reinitialize i a process which for loop does for us
while i < 10: # as long as i is less then 10 keep going, this instead of range
    print(i)
    i += 1 # increment i at the end of the loop a process done automatically by for loop

# be weary, if the condition is written incorrectly while loop can run indefinitely!
i = 0
# while i >= 0:
#     print(i)

# sometimes we dont know how long will the loop run but we know when to stop
# its time to introduce while True loop
# True is a bool value, and since its True if it is in header of while it will run indefinitely
# will it?
# here we have a simple mathematical function sin which has been raised by one on the y axis
# now we wonder, when will the value of y get in between 0.3 and -0.3?
# we can use break command to stop the cycle when that will happen
import math # dont worry about this for now

x = 0
while True:
    y = math.sin(x) + 1
    print(y)
    if 0.3 >= y >= -0.3:
        break
    x += 0.1

# knowing break now we can look into the continue command
# lets look back at the for cycle
# we have an list of numbers and we want to see every division 10 / num
# however there might be some zeros and zero in the nums and division with zero is illegal math operation
# lets have a statement than that skips the loop cycle if num == 0

nums = [1,23,5,8,0,2,5]
for id, num in enumerate(nums):
    if num == 0:
        continue

    print("id: ", id, "10 / num: ", 10 / num)

