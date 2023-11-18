import sys

args = sys.argv[1:]

precision = int(args[0])
num = float(args[1])
decimal = num - int(num)

left = (0, 1)
right = (1, 1)

def mediant(a, b):
    return (a[0] + b[0], a[1] + b[1])

for _ in range(precision):
    med = mediant(left, right)
    if med[0] / med[1] < decimal:
        left = med
    else:
        right = med

print(f"{left[0]}/{left[1]}")
