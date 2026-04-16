# Complex test script for script execution mode

# Test if-elif-else chain
if x > 10:
    print("x is greater than 10")
elif x > 0:
    print("x is between 1 and 10")
else:
    print("x is less than or equal to 0")

# Test nested if statements
if y > 0:
    if y % 2 == 0:
        print("y is positive and even")
    else:
        print("y is positive and odd")
else:
    print("y is non-positive")

# Test while loop (with limited iterations)
i = 0
while i < 3 and x > 0:
    print(f"Loop iteration: {i}")
    i += 1
