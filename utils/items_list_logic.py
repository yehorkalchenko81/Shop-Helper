class ItemsList:
    def __init__(self, text: str):
        self.items = [Item(string.strip()) for string in text.split('\n') if string.replace(' ', '').isalnum()]

    def __getitem__(self, key):
        return self.items[key]

    def __iter__(self):
        return iter(self.items)

    def __str__(self):
        return '\n'.join([str(item) for item in self.items])


class Item:
    def __init__(self, text: str):
        self.name = text
        self.is_added = False

    def add(self):
        self.is_added = True

    def remove(self):
        self.is_added = False

    def __str__(self):
        return f'{self.name} ' + ('✅' if self.is_added else '❌')


if __name__ == '__main__':
    items_list = ItemsList('Item1\nItem2\n\nItem3')

    items_list[0].add()
    items_list[1].add()
    items_list[0].remove()

    print(items_list)

    # for i in items_list:
    #     print(i)


