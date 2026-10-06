"""Day 28 — Weather CLI.
Usage: python3 day28_weather_cli.py Pune
"""

import argparse
import requests

def main():
    p = argparse.ArgumentParser()
    p.add_argument("city")
    args = p.parse_args()
    print(requests.get(f"https://wttr.in/{args.city}?format=3", timeout=10).text)

if __name__ == "__main__":
    main()