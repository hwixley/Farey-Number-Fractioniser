# Fraction-Rationaliser
Turning rational numbers into rational fractional forms using concepts from the Farey algorithm.Turning rational numbers into rational fractional forms using concepts from the Farey algorithm.

![pi-updated-output](https://github.com/hwixley/Fraction-Rationaliser/assets/57837950/a80f2a3f-c3a0-47fa-984d-39959987b05a)

<hr>

# Install

1. Clone the repository
```
git clone git@github.com:hwixley/Fraction-Rationaliser.git
```
2. Install the requirements
```
pip3 install -r requirements.txt
```
3. Run the script
```
python3 farey.py <precision> <rational-number>
```

<hr>

# Inputs
The script currently has a strict order of non-optional inputs:
```
python3 farey.py <precision> <rational-number>
```

__*This will be updated in future to use dynamic input flags (ie. `-p <precision>`)__

- `<precision>` - an integer value, this denotes the precision of the fraction to the specified number of decimal places
- `<rational-number>` - a rational number in the form of a floating point or string special value, this denotes the number you are generating a fraction for
  - __Special Values:__ `pi`, `e`, `phi`
  - __Special Funcs:__ `sqrt[<num>]`, `log[<num>]`, `log2[<num>]`, `ln[<num>]`, `sin[<num>]`, `cos[<num>]`, `tan[<num>]`
