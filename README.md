# Fraction-Rationaliser
Turning rational numbers into rational fractional forms using concepts from the Farey algorithm.Turning rational numbers into rational fractional forms using concepts from the Farey algorithm.

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
`python3 farey.py <precision> <rational-number>`

- `<precision>` - an integer value, this denotes the precision of the fraction to the specified number of decimal places
- `<rational-number>` - a rational number in the form of a floating point or string special value, this denotes the number you are generating a fraction for
  - Special Values:
      - `pi`
      - `e`
      - `phi`
      - `sqrt<num>`