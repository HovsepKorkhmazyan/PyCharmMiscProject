# 1
def parse_contact(contact):
    parts = contact.split(", ")
    return {
        "name": parts[0],
        "surname": parts[1],
        "email": parts[2],
        "phone": parts[3]
    }


def get_by_name(contacts, name):
    name = name.lower()
    return [parse_contact(c) for c in contacts if parse_contact(c)["name"].lower() == name]


def get_by_email(contacts, email):
    email = email.lower()
    return [parse_contact(c) for c in contacts if parse_contact(c)["email"].lower() == email]


def get_by_phone(contacts, phone):
    return [parse_contact(c) for c in contacts if parse_contact(c)["phone"] == phone]


def get_domain(email):
    return email.split("@")[1].split["."][0]

email = "james@gmail.com"
domain = get_domain(email)
print(domain)
mail = "gmail"
if mail == get_domain(email):
    print("The email is from the specified domain.")
else:
    print("The email is not from the specified domain.")

contacts = ["James, Scott, james@gmail.com, 09410101"]
result = get_by_name(contacts, "James")
if result:
    print("Get by name:", result)
else:
    print("User  does not exist")
result = get_by_email(contacts, "james@gmail.com")
if result:
    print("Get by email:", result)
else:
    print("User  does not exist")
result = get_by_phone(contacts, "09410101")
if result:
    print("Get by phone:", result)
else:
    print("User  does not exist")

# 2
user1_attempts = 5
user2_attempts = 5
user1_score = 0
user2_score = 0

while user1_attempts > 0 and user2_attempts > 0:
    user_input1 = input("User  1, enter a 3-digit number: ")
    user_input2 = input("User  2, enter a 3-digit number: ")

    if len(user_input1) != 3 or len(user_input2) != 3:
        print("Invalid input - numbers must be exactly 3 digits")
        continue

    if user_input2[-1] == user_input1[-1]:
        print("User  2 guessed correctly!")
        user2_score += 1
    else:
        user2_attempts -= 1
        print(f"User  2's guess is wrong! Attempts remaining: {user2_attempts}")

    if user_input1[-1] == user_input2[-1]:
        print("User  1 guessed correctly!")
        user1_score += 1
    else:
        user1_attempts -= 1
        print(f"User  1's guess is wrong! Attempts remaining: {user1_attempts}")

if user1_attempts == 0:
    print(f"User  1 Game Over! Final score: {user1_score}")
if user2_attempts == 0:
    print(f"User  2 Game Over! Final score: {user2_score}")
