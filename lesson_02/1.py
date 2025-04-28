data = [1, 2, 3, 4, 4, 5, 2, 1]


class DeduplicationIterator:
    def __init__(self, data: list[int]) -> None:
        breakpoint()  # TODO: remove
        self.data = set(data)

    def __next__(self):
        for i in self.data:
            return i

    def __iter__(self):
        for i in self.data:
            yield i


iterator = DeduplicationIterator(data=data)
print(next(iterator))

# for i in DeduplicationIterator(data=data):
#     print(i)
