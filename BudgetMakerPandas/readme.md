# Introduction #
This script is used to sum values in a .csv file.

## How to use ##
To use this script, there must be a filed named raw.csv in the folder. The header in the csv file must contain:
* Beløb
* Emne
* Underemne

The script will sum up all values in 'Beløb' with the same 'Emne'.

## Example ##
The raw.csv file:

```
Bogføringsdato;Beløb;Emne;Underemne
2023-01-10;-100;Hjemmeside;
10/10/2023;-800;Forbrug;Vand
10/10/2023;-700;Forbrug;Varme
10/10/2023;-900;Forbrug;El
10/10/2023;-100;Forbrug;
10/10/2023;6.700,59;Løn;
09-10-2023;-118,95;Vedligehold;Kælder
```

The output will be output.csv:

```
Category;Amount
Forbrug;-2500,0
 - El;-900,0
 - Vand;-800,0
 - Varme;-700,0
Vedligehold;-118,95
 - Kælder;-118,95
Hjemmeside;-100,0
Løn;6700,59
```