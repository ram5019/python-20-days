"""Day 22 — Lambda, map, filter."""

def main():
    c = [0, 25, 37, 100]
    print(list(map(lambda x: x * 9 / 5 + 32, c)))
    print(list(filter(lambda x: x % 2 == 0, range(10))))

if __name__ == "__main__":
    main()