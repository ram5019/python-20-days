try: print(10/int(input("N: ")))
except ValueError: print("Not a number")
except ZeroDivisionError: print("Zero not allowed")
