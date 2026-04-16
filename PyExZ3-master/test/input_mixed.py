name = input("Enter your name: ")
age = int(input("Enter your age: "))
height = float(input("Enter your height: "))

print(f"Hello, {name}!")
print(f"You are {age} years old and {height} meters tall.")

if age >= 18:
    print("You are an adult.")
else:
    print("You are a minor.")
