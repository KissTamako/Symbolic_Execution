#!/usr/bin/env python3
"""
Simple student script for testing script mode.
Typical student assignment: check if input number is positive.
"""

import sys

def main():
    # Read input from command line arguments or input()
    if len(sys.argv) > 1:
        try:
            x = int(sys.argv[1])
        except ValueError:
            print("Error: Argument must be an integer")
            return
    else:
        try:
            x = int(input("Enter a number: "))
        except ValueError:
            print("Error: Input must be an integer")
            return
    
    # Check if number is positive
    if x > 0:
        print(f"{x} is positive")
        result = "positive"
    elif x < 0:
        print(f"{x} is negative")
        result = "negative"
    else:
        print(f"{x} is zero")
        result = "zero"
    
    # Return result (for testing)
    return result

if __name__ == "__main__":
    main()