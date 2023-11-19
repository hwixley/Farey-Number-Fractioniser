import sys
from yaspin import yaspin
import numpy as np
from termcolor import colored

args = sys.argv[1:]

# Parse arguments
precision = int(args[0])
input_num = args[1]

# Check if input number is a special number or a number with a special operation
special_ops = ["sqrt", "log", "log2", "ln", "sin", "cos", "tan"]
if args[1] == "pi":
    input_num = str(np.pi)
elif args[1] == "e":
    input_num = str(np.e)
elif args[1] == "phi":
    input_num = str((1 + np.sqrt(5))/2)
else:
    for op in special_ops:
        if args[1].startswith(op + "[") and args[1].endswith("]"):
            if args[1][len(op)+1:-1].isdigit() or (args[1][len(op)+1] == "-" and args[1][len(op) + 2:-1].isdigit()):
                input_num = str(eval(f"np.{op}({args[1][len(op)+1:-1]})"))
                break
            else:
                print(colored(f"Invalid input number '{args[1]}'", "red"))
                sys.exit(1)

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
    while True and precision >= 0 and decimal >= 0:

        # Calculate mediant
        med = mediant(left, right)

        # Check if mediant is close enough to the decimal
        error = np.abs((med[0] / med[1]) - float(f"0.{decimal}"))
        if error < 1/(10**precision):
            fside = med
            break

        # Else update left and right
        if med[0] / med[1] < float(f"0.{decimal}"):
            left = med
        else:
            right = med


print(colored("\nApproximately: ", "light_grey") +  colored(f"{fside[0] + int(num) * fside[1]}/{fside[1]} ≈ {(fside[0] + int(num) * fside[1])/fside[1]}\n", "green"))