db = {}

user_input = input("Do you want to Register or Log in?")
while True:
    username = input("Username: ")
    while username in db:
        username = input("Username: ")
    if user_input == "stop":
        break
    elif username in db:
        print("Username already exists")
    else:
        password = input("Password: ")
        db[username] = password
        print("Registered successfully")

    if user_input == "Log in":
        username = input("Username: ")
        password = input("Password: ")

        if username in db:
            if db[username] == password:
                print("Logged in successfully.")
            else:
                print("Login failed: Incorrect password.")
        else:
            print("Login failed: Username does not exist.")
    else:
        print("Invalid input. Please type 'Log in' to log in or 'exit' to quit.")

for i in range(5):
    name = input(f'Enter the name of student {i + 1}: ')
    age = int(input(f'Enter the age of student {i + 1}: '))
    marks = int(input(f'Enter the marks of student {i + 1}: '))

