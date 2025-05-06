while True:
    string_input = input("Enter a sentence (or type 'stop' to exit): ")

    if string_input.lower() == "stop":
        break

    words = string_input.split()
    md = {}

    for el in words:
        if el.isalpha():
            if el in md:
                md[el] += 1
            else:
                md[el] = 1

    print(md)  # 