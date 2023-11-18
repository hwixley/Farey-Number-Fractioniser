import sys
from yaspin import yaspin
import numpy as np

args = sys.argv[1:]

precision = int(args[0])
num_str = args[1].split(".")
num = int(num_str[0])
decimal = int(num_str[1])

left = (0, 1)
right = (1, 1)

def mediant(a, b):
    return (a[0] + b[0], a[1] + b[1])


with yaspin(text="Calculating", color="yellow") as spinner:
    while True:
        med = mediant(left, right)
        if med[0] / med[1] < float(f"0.{decimal}"):
            left = med
        else:
            right = med

        print((med[0] / med[1]) - float(f"0.{decimal}"))
        print(f"Calculating {med[0]}/{med[1]}")

        print("")

        if precision == 0:
            break
        else:
            a = str(med[0] / med[1])[2:2+precision]
            b = str(decimal)[:precision]
            min_len = np.min([len(a), len(b)])
            # print(a, b, min_len)
            if a == b or (len(b) < len(a) and a[:min_len] == b[:min_len]):
                break

        

print(f"{int(num)} + {med[0]}/{med[1]} \t OR \t {med[0] + int(num) * med[1]}/{med[1]}")
