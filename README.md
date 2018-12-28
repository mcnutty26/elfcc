# elfcc - the elfcode compiler

## Usage

```./elfcode -i <infile> -o <outfile> [opts]```

Where opts is one or more of:
* ```-O0 | -O1 | -O2 | -O3``` the level of compiler optimisation to use
* ```-p``` embed profiling code into the program, which prints out how often each line was executed upon termination
* ```-v | -V``` prints elfcc version information
* ```-h``` prints usage information

## Benefits
_Much_ faster than running elfcode in a virtual machine!

