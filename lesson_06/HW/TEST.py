import time
import random
import copy


# лічильник операцій
class Pidrahunok:
    def __init__(self):
        self.porivnyannya = 0
        self.prysvoyennya = 0


# бульбашка
def sort_bulbashka(mas, p):
    n = len(mas)
    for i in range(n):
        for j in range(0, n - i - 1):
            p.porivnyannya += 1
            if mas[j] > mas[j + 1]:
                mas[j], mas[j + 1] = mas[j + 1], mas[j]
                p.prysvoyennya += 3


# вибором
def sort_vyborom(mas, p):
    n = len(mas)
    for i in range(n):
        min_i = i
        for j in range(i + 1, n):
            p.porivnyannya += 1
            if mas[j] < mas[min_i]:
                min_i = j
        if min_i != i:
            mas[i], mas[min_i] = mas[min_i], mas[i]
            p.prysvoyennya += 3


# вставками
def sort_vstavkamy(mas, p):
    for i in range(1, len(mas)):
        kluch = mas[i]
        p.prysvoyennya += 1
        j = i - 1
        while j >= 0 and mas[j] > kluch:
            p.porivnyannya += 1
            mas[j + 1] = mas[j]
            p.prysvoyennya += 1
            j -= 1
        p.porivnyannya += 1
        mas[j + 1] = kluch
        p.prysvoyennya += 1


# шелла
def sort_shela(mas, p):
    n = len(mas)
    k = n // 2
    while k > 0:
        for i in range(k, n):
            temp = mas[i]
            p.prysvoyennya += 1
            j = i
            while j >= k and mas[j - k] > temp:
                p.porivnyannya += 1
                mas[j] = mas[j - k]
                p.prysvoyennya += 1
                j -= k
            p.porivnyannya += 1
            mas[j] = temp
            p.prysvoyennya += 1
        k //= 2


# перевірка
def perevirka_sortuvannya(mas):
    algos = [
        ("Бульбашка", sort_bulbashka),
        ("Вибором", sort_vyborom),
        ("Вставками", sort_vstavkamy),
        ("Шелла", sort_shela),
    ]

    for nazva, funktsiya in algos:
        kopiya = copy.deepcopy(mas)
        l = Pidrahunok()
        start = time.perf_counter()
        funktsiya(kopiya, l)
        end = time.perf_counter()
        print(f"{nazva}:\nПорівнянь: {l.porivnyannya}, Присвоєнь: {l.prysvoyennya}, Час: {end - start:.6f} сек\n")

def main():
    # запуск
    baza = [9, 13, -4, -1, -6, 57, 8, 50, 11, 39, 22, 14, 12]
    rand100 = [random.randint(-100, 100) for _ in range(100)]
    rand10000 = [random.randint(-1000, 1000) for _ in range(10000)]

    print("=== БАЗОВИЙ МАСИВ ===\n")
    perevirka_sortuvannya(baza)

    print("\n=== МАСИВ ІЗ 100 ЕЛЕМЕНТІВ ===\n")
    print("Початковий:", rand100)
    perevirka_sortuvannya(rand100)

    print("\n=== МАСИВ ІЗ 10000 ЕЛЕМЕНТІВ ===\n")
    perevirka_sortuvannya(rand10000)

if __name__ == "__main__":
    main()
