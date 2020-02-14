# br187-tool
Tool for calculating the external fire spread of a radiating surface in line with guidance document BR 187

## Usage:
`br187.py`

or for command line usage add the `-c` flag and provide the geometry:

`br187.py -c [--width WIDTH] [--height HEIGHT] [--separation SEPARATION] [--type TYPE] [--title "TITLE"] [--output OUTPUTPATH]`

(Types are: **p**arallel, **c**orner, **o**rthogonal)

### Example:

calculating external fire spread characteristics of a 10m x 3m wall a distance of 4m away from an opposite building:

`br187.py -c --width 10 --height 3 --separation 4 --type p --title "example analysis" --output "my_analysis"`

Output:
```
--------------------------------------------------------------------------------------------------------
BR 187 | External Fire Spread Calculator
A calculator based on the BR 187 standard for calculating external fire spread to neighbouring buildings

Author: Alex Todd
OFR Consultants

Title: example analysis
Type: parallel
Separation: 4.0
View Factor: 0.3074686504477437
Radiator Dimensions
        Width: 10.0
        Height: 3.0
Reduced Fire Load
        Safe Distance: 6.9
        Unprotected Area
                unsprinklered: 48.8
                sprinklered: 97.6
Standard Fire Load
        Safe Distance: 10.5
        Unprotected Area
                unsprinklered: 24.4
                sprinklered: 48.8

```

## Dependencies:
- numpy

## Help:
For help on using this tool I recommend running it with the `--help` option.

For Example: `br187.py --help`

## Contact
Alex Todd

OFR Consultants

alex.todd@ofrconsultants.com
