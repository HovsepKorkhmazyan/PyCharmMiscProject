# 1 List Comprehension
print(','.join([el for el in input().split() if len(el) > 3]))

# 2
user_input = input().split()
temp = []
for el in user_input:
    if el.isalpha():
        temp.append(el[::-1])
print(temp)

# ver 2 of 2
print(' '.join([el[::-1] for el in input().split()]))

# 3
while True:
    user_input = input().split()
    if user_input == ['stop']:
        break
    emails = {
    "mail.ru": [],
    "gmail.com": [],
    "outlook.com": []
}
    domain = input().split("@")[1]
    if domain in emails:
        emails[domain].append(user_input)
    else:
        emails[domain] = user_input

    for el in user_input:
        if el in "mail.ru":
            emails["mail.ru"].append(el)
        if el in "gmail.com":
            emails["gmail.com"].append(el)
        if el in "outlook.com":
            emails["outlook.com"].append(el)
    for domain, emails in emails.items():
        print(domain)
        for email in emails:
            print(email)

