# waveform
Waveform Generator for AM, FM and PM

Possible input formats are:
* Bare binary
* ASCII characters, will be converted to 7-bit ASCII
* Numbers, will be converted to 4-bit BCD

This solves exercise 2.3 of the tasks given in Rechnernetze @ TU Dresden.

## Dependencies
* Necessary:
** Python 3
** Matplotlib

* Optional:
** tkinter (for GUI; otherwise a CLI or command line options can be used)
** NumPy (for fast calculations)

## HowTo
Simply execute main.py on your command line.

Possible arguments:  
```
$> ./main.py --help
usage: main.py [-h] [--nogui] [--steps STEPS] [--store-plot INPUT]
               [--store-wave INPUT]

Modulate Waveforms

optional arguments:
  -h, --help          show this help message and exit
  --nogui             Use CLI by preference
  --steps STEPS       Steps to use for plotting per interval
  --store-plot INPUT  Create the waveform chart for the given formatted input.
                      The input is interpreted as Binary.
                      To trigger interpretation as 7-bit ASCII, prefix the input with a_.
                      To trigger interpretation as 4-bit BCD, prefix the input with d_.
                      The file will be saved as wave_INPUT.png to the current directory.
  --store-wave INPUT  Create the waveform data for the given formatted input.
                      The input is interpreted as Binary.
                      To trigger interpretation as 7-bit ASCII, prefix the input with a_.
                      To trigger interpretation as 4-bit BCD, prefix the input with d_.
                      The file will be saved as wave_INPUT.txt to the current directory.
```

