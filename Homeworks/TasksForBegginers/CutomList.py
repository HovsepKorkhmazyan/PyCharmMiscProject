class CustomList:
    def __init__(self):
        self.items = []

    def append(self, item):
        self.items += [item]

    def remove(self, item):
        if item in self.items:
            self.items.remove(item)
        else:
            raise ValueError(f"{item} not found in list")

    def get(self, index):
        if index < 0 or index >= len(self.items):
            raise IndexError("Index out of range")
        return self.items[index]

    def set(self, index, value):
        if index < 0 or index >= len(self.items):
            raise IndexError("Index out of range")
        self.items[index] = value

    def size(self):
        return len(self.items)

    def clear(self):
        self.items = []

    def __str__(self):
        return str(self.items)

    def __getitem__(self, index):
        return self.get(index)

    def __setitem__(self, index, value):
        self.set(index, value)

    def __len__(self):
        return self.size()

    def __iter__(self):
        return iter(self.items)


if __name__ == "__main__":
    custom_list = CustomList()

    custom_list.append(1)
    custom_list.append(2)
    custom_list.append(3)

    print("Custom List:", custom_list)

    print("Element at index 1:", custom_list.get(1))

    custom_list.set(1, 5)
    print("After setting index 1 to 5:", custom_list)

    custom_list.remove(3)
    print("After removing 3:", custom_list)

    print("Size of the list:", custom_list.size())

    custom_list.clear()
    print("After clearing the list:", custom_list)
