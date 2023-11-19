# Fraction-Rationaliser
Turning rational numbers into rational fractional forms using concepts from the Farey algorithm.Turning rational numbers into rational fractional forms using concepts from the Farey algorithm.

![pi-output](https://github.com/hwixley/Fraction-Rationaliser/assets/57837950/4c851fbc-e9c0-4fe8-bb47-08aa11f5fa82)

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

# Inputs
The script currently has a strict order of non-optional inputs:
`python3 farey.py <precision> <rational-number>`

*This will be updated in future to use dynamic input flags (ie. `-p <precision>`)

- `<precision>` - an integer value, this denotes the precision of the fraction to the specified number of decimal places
- `<rational-number>` - a rational number in the form of a floating point or string special value, this denotes the number you are generating a fraction for
  - <b>Special Values:</b> `pi`, `e`, `phi`
  - <b>Special Funcs:</b> `sqrt[<num>]`, `log[<num>]`, `log2[<num>]`, `ln[<num>]`, `sin[<num>]`, `cos[<num>]`, `tan[<num>]`
