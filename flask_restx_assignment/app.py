name = input("Enter your name: ")

while name == "":
    print("Name cannot be empty. Please enter your name.")
    name = input("Enter your name: ")
print(f"Hello, {name} welcome to the world of science!")

age = int(input("Enter your age: "))

while age < 0 or age > 120:
    print("Age must be between 0 and 120. Please enter a valid age.")
    age = int(input("Enter your age: "))
print(f"Hello, {name}! You are {age} years old. Welcome to the world of science!")
