# compulsory Homework 1
  - In this homework your task is to complete the functions `add_matrix()` and `multiply_matrix()` in `matrix_operations.py` file
  - As a bonus you can implement `solve()` to further improve your grade
  - To understand matrix multiplication and addition take a look at the following:
    - wiki on matrix addition: https://en.wikipedia.org/wiki/Matrix_addition
    - wiki on matrix multiplication: https://en.wikipedia.org/wiki/Matrix_multiplication
    - check some youtube videos as well: https://www.youtube.com/watch?v=p48uw2vFWQs
  - You can use the `matrix_operations_test.py` to test your result
  - **!!YOU ARE ALLOWED TO USE ONLY PYTHON BASIC LIBRARIES!!**
  - **!!ASSIGNMENTS ARE ACCEPTED ONLY IN PYTHON CODE!!**
  - **DEADLINE: 5.11 16:00**

## example for add_matrix()
```
A = [[1, 2, 3], [4, 5, 6]]
B = [[7, 8, 9], [10, 11, 12]]
C = add_matrix(A, B)
print(C)
>> [[8, 10, 12], [14, 16, 18]]
```

## example for multiply_matrix()
```
A = [[1, 2, 3], [4, 5, 6]]
B = [[7], [8], [9]]
C = multiply_matrix(A, B)
print(C)
>> [[50], [122]]
```

## example for multiply_matrix()
```
A = [[1, 2, 3], [4, 5, 6]]
B = [[7, 8, 9], [10, 11, 12]]
C = [[1, 2, 3], [4, 5, 6]]
solution = solve([A, "+", B, "@", C])
print(solution)
>> [[ 49,  74,  99], [ 70, 104, 138]]
```
