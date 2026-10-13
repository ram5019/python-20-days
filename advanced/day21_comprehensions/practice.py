"""Day 21 — Comprehensions."""

def main():
    words = ["hi", "python", "cloud", "aws", "azure"]
    print([w for w in words if len(w) > 4])
    print({x: x * x for x in range(6)})

if __name__ == "__main__":
    main()