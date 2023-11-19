import sys
from yaspin import yaspin
import numpy as np
from termcolor import colored

args = sys.argv[1:]

# Parse arguments
if len(args) != 2:
    print(colored("Invalid number of arguments", "red"))
    sys.exit(1)

elif not args[0].isdigit():
    print(colored(f"Invalid precision '{args[0]}'", "red"))
    sys.exit(1)

# if not args[1].replace(".", "", 1).isdigit() and not args[1] in ["pi", "e", "phi"]:

precision = int(args[0])
input_num = args[1]

# Check if input number is a special number or a number with a special operation
special_vals = ["pi", "e", "euler_gamma", "nan", "inf", "NINF", "PINF"]
special_ops = ["sqrt", "log", "log2", "ln", "sin", "cos", "tan"]
if args[1] in special_vals:
    input_num = str(eval(f"np.{args[1]}"))
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
num = float(num_str[0])
decimal = 0
if len(num_str) > 1:
    decimal = float(num_str[1])

seps = "-"*30
print("\n" + seps)
print(colored("INPUTS", "light_grey"))
print(seps)
print(colored("Precision: ", "light_grey") + colored(f"{precision}", "blue"))
print(colored("Number: ", "light_grey") + colored(f"{input_num}", "blue"))
print(seps + "\n")

# Farey sequence
def mediant(a, b):
    return (a[0] + b[0], a[1] + b[1])

def get_precision():
    return 1/(10**(precision))

# Setup left and right, and found vars for Farey sequence
left = (0, 1)
right = (1, 1)
fside = (0, 0)

# Iterate through Farey sequence until the error is smaller than the precision, ie. error < 1/(10**precision)
with yaspin(text="Calculating", color="yellow") as spinner:
    while True and precision >= 0 and decimal >= 0:

        # Calculate mediant
        med = mediant(left, right)
    
        # update left and right
        if med[0] / med[1] < float(f"0.{int(decimal)}"):
            left = med
        else:
            right = med

        # Check if mediant is close enough to the decimal
        errors = []
        for side in [left, right]:
            error = np.abs((side[0] / side[1]) - float(f"0.{int(decimal)}"))
            if error < get_precision():
                errors.append(error)
            else:
                errors.append(np.inf)
        
        # If the error is smaller than the precision check if the closest side is valid, if so break
        if np.min(errors) < get_precision():
            fside = [left, right][np.argmin(errors)]
            
            a = str(fside[0]/fside[1]).split(".")[1][:precision]
            b = str(int(decimal))[:precision]
            if a == b or (len(b) < len(a) and a.startswith(b)):
                spinner.ok("✅ ")
                print("\n" + seps)
                print(colored("FINAL FAREY SEQUENCE", "light_grey"))
                print(seps)
                print(colored("Left: ", "light_grey") + colored(f"{left}", "blue"))
                print(colored("Right: ", "light_grey") + colored(f"{right}", "blue"))
                print(seps)
                print(colored("Final side: ", "light_grey") + colored(f"{fside}", "red"))
                print(colored("Error: ", "light_grey") + colored(f"{np.min(errors)}", "yellow"))
                print(seps)
                break

print(colored("\nApproximately: ", "light_grey") +  colored(f"{int(fside[0] + num * fside[1])}/{int(fside[1])} ≈ {(fside[0] + num * fside[1])/fside[1]}\n", "green"))