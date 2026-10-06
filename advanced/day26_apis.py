import requests; print(requests.get("https://api.github.com/users/torvalds",timeout=10).json()["name"])
