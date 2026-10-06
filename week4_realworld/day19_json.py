"""Day 19 — JSON.
Task: Dict <-> JSON round trip.
"""

import json

def main():
    data = {"name": "Ravi", "skills": ["Python", "SQL"]}
    text = json.dumps(data, indent=2)
    print(text)

    parsed = json.loads(text)
    print("Skills:", parsed["skills"])

if __name__ == "__main__":
    main()