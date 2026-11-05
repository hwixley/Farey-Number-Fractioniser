import sys
from fractions import Fraction

import mpmath
from yaspin import yaspin
from termcolor import colored

GUARD_DIGITS = 20  # extra working digits so the requested digits are trustworthy

args = sys.argv[1:]

# Parse arguments
if len(args) != 2:
    print(colored("Invalid number of arguments", "red"))
    sys.exit(1)

elif not args[0].isdigit():
    print(colored(f"Invalid precision '{args[0]}'", "red"))
    sys.exit(1)

precision = int(args[0])
input_arg = args[1]

special_vals = {
    "pi": lambda: mpmath.pi,
    "e": lambda: mpmath.e,
    "phi": lambda: mpmath.phi,
    "euler_gamma": lambda: mpmath.euler,
}
special_ops = {
    "sqrt": mpmath.sqrt,
    "log": mpmath.log10,
    "log2": lambda x: mpmath.log(x, 2),
    "ln": mpmath.ln,
    "sin": mpmath.sin,
    "cos": mpmath.cos,
    "tan": mpmath.tan,
}


def mpf_to_fraction(x):
    """Exact conversion of an mpmath float (mantissa * 2^exp) to a Fraction."""
    if isinstance(x, mpmath.mpc) or not mpmath.isfinite(x):
        raise ValueError("number is not a finite real")
    man, exp = mpmath.mpf(x).man_exp
    return Fraction(man) * (Fraction(2) ** exp)


def parse_number(s):
    """Return the input as an exact Fraction (irrationals are evaluated to `precision` + guard digits)."""
    if s in special_vals:
        return mpf_to_fraction(special_vals[s]())
    for op, fn in special_ops.items():
        if s.startswith(op + "[") and s.endswith("]"):
            return mpf_to_fraction(fn(mpmath.mpf(s[len(op) + 1:-1])))
    # Plain decimal / integer / "a/b" input is converted exactly
    return Fraction(s)


def to_decimal(f, places):
    """Exact decimal string of a Fraction, truncated to `places` decimals."""
    sign = "-" if f < 0 else ""
    digits = str((abs(f.numerator) * 10 ** places) // f.denominator).rjust(places + 1, "0")
    return sign + (digits[:-places] + "." + digits[-places:] if places else digits)


def ceil_div(n, m):
    return -(-n // m)


# Evaluate constants/functions with arbitrary precision (not 64-bit floats)
mpmath.mp.dps = precision + GUARD_DIGITS
try:
    target = parse_number(input_arg)
    # Keep enough significant digits for large integer parts too
    if abs(target) >= 1:
        mpmath.mp.dps = precision + GUARD_DIGITS + len(str(abs(target.numerator) // target.denominator))
        target = parse_number(input_arg)
except (ValueError, ZeroDivisionError, TypeError) as err:
    print(colored(f"Invalid input number '{input_arg}' ({err})", "red"))
    sys.exit(1)

sign = -1 if target < 0 else 1
whole = abs(target.numerator) // target.denominator
x = abs(target) - whole  # fractional part in [0, 1)

seps = "-" * 30
print("\n" + seps)
print(colored("INPUTS", "light_grey"))
print(seps)
print(colored("Precision: ", "light_grey") + colored(f"{precision}", "blue"))
print(colored("Number: ", "light_grey") + colored(to_decimal(target, precision), "blue"))
print(seps + "\n")

# Plain integers from here on: x = X / Y (much faster than Fraction, which runs a gcd on every op)
X, Y = x.numerator, x.denominator

# The answer must match x when truncated to `precision` decimals: T/scale <= p/q < (T+1)/scale
scale = 10 ** precision
T = (X * scale) // Y


def good(p, q):
    return T * q <= p * scale < (T + 1) * q


def smallest_good_k(make, kmax):
    """Binary search the smallest k in [1, kmax] where make(k) is good (monotone within a run)."""
    k_lo, k_hi = 1, kmax
    while k_lo < k_hi:
        mid = (k_lo + k_hi) // 2
        if good(*make(mid)):
            k_hi = mid
        else:
            k_lo = mid + 1
    return k_lo


# Farey / Stern-Brocot walk with exact integers.
# Consecutive mediant steps in the same direction are taken as one batch:
#   left_k = (a + k*c, b + k*d)   or   right_k = (c + k*a, d + k*b)
# which gives exactly the same sequence of mediants, just without looping over each one.
left = (0, 1)
right = (1, 1)
steps = 0

with yaspin(text="Calculating", color="yellow") as spinner:
    if good(*left):
        fside = left
    elif good(*right):
        fside = right
    else:
        while True:
            (a, b), (c, d) = left, right
            med = (a + c, b + d)
            cmp = med[0] * Y - X * med[1]  # sign of (mediant - x)
            if cmp == 0:
                fside = med
                steps += 1
                break
            if cmp < 0:
                # Move left towards x: left_k < x  <=>  k < (x*b - a) / (c - x*d)
                kmax = ceil_div(X * b - a * Y, c * Y - X * d) - 1
                make = lambda k: (a + k * c, b + k * d)
            else:
                # Move right towards x: right_k > x  <=>  k < (c - x*d) / (x*b - a)
                kmax = ceil_div(c * Y - X * d, X * b - a * Y) - 1
                make = lambda k: (c + k * a, d + k * b)
            end = make(kmax)
            if good(*end):
                k = smallest_good_k(make, kmax)
                fside = make(k)
                steps += k
                break
            if cmp < 0:
                left = end
            else:
                right = end
            steps += kmax
    spinner.ok("✅ ")

num = sign * (fside[0] + whole * fside[1])
den = fside[1]
error = abs(Fraction(num, den) - target)

print("\n" + seps)
print(colored("FINAL FAREY SEQUENCE", "light_grey"))
print(seps)
print(colored("Mediant steps: ", "light_grey") + colored(f"{steps}", "blue"))
print(colored("Digits: ", "light_grey") + colored(f"{len(str(abs(num)))}/{len(str(den))}", "cyan"))
print(colored("Error: ", "light_grey") + colored(mpmath.nstr(mpmath.mpf(error.numerator) / error.denominator, 5), "yellow"))
print(seps)

print(colored("\nApproximately: ", "light_grey") + colored(f"{num}/{den} ≈ {to_decimal(Fraction(num, den), precision)}\n", "green"))
