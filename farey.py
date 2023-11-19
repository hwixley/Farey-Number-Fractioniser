import sys
from yaspin import yaspin
import numpy as np
from termcolor import colored

args = sys.argv[1:]

# Parse arguments
precision = int(args[0])
input_num = args[1]
if args[1] == "pi":
    input_num = str(np.pi)
elif args[1] == "e":
    input_num = str(np.e)
elif args[1] == "phi":
    input_num = str((1 + np.sqrt(5))/2)
elif args[1].startswith("sqrt") and args[1][4:].isdigit():
    input_num = str(np.sqrt(int(args[1][4:])))


# Parse input number
num_str = input_num.split(".")
num = int(num_str[0])
decimal = int(num_str[1])

# Farey sequence
def mediant(a, b):
    return (a[0] + b[0], a[1] + b[1])

# Setup left and right, and found vars for Farey sequence
left = (0, 1)
right = (1, 1)
fside = (0, 0)

# Iterate through Farey sequence until the error is smaller than the precision, ie. error < 1/(10**precision)
with yaspin(text="Calculating", color="yellow") as spinner:
    while True:
        med = mediant(left, right)
        if med[0] / med[1] < float(f"0.{decimal}"):
            left = med
        else:
            right = med

        if precision == 0 or decimal == 0:
            break
        else:
            # Check if left or right side are close enough to the decimal
            for side in [left, right]:
                error = np.abs((side[0] / side[1]) - float(f"0.{decimal}"))
                if error < 1/(10**precision):
                    fside = side
                    break

            # Break if a side is found
            if fside != (0, 0):
                break

print(colored("\nApproximately: ", "light_grey") +  colored(f"{fside[0] + int(num) * fside[1]}/{fside[1]} ≈ {(fside[0] + int(num) * fside[1])/side[1]}\n", "green"))