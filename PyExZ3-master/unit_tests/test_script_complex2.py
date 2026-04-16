# Complex test script for script execution mode
# This script mimics the functionality of various test cases

# Test if-elif-else chain (similar to unnecessary_condition3.py)
if x > 0:
    result = 10
elif x == 0:
    result = 20
elif x == -1:
    result = 21
elif x == -2:
    result = 22
elif x == -3:
    result = 23
elif x == -4:
    result = 24
else:
    result = 25

print(f"Result from if-elif-else: {result}")

# Test nested conditions (similar to diamond.py)
if x > 0:
    if y > 0:
        nested_result = "x>0 and y>0"
    else:
        nested_result = "x>0 and y<=0"
else:
    if y > 0:
        nested_result = "x<=0 and y>0"
    else:
        nested_result = "x<=0 and y<=0"

print(f"Result from nested conditions: {nested_result}")
