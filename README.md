# PyQrCodeGen

A python script to generate and exports qr codes.

The script can be run with several parameters:

- `-d`, `--data`: the data to encode into the qr code.
- `-e`, `--error-correction`: the level of error correction for the qr code, the values
    can be `L`, `M (the default one)`, `Q`, `H`.
- `-o`, `--output-file`: if this parameter is not given, then the qr code will be displayed into 
    the standard output, else it will be exported in the given file.
- `-l`, `--logo`: an image file to add as logo within the qr code, this option need the `-o` parameter because
    the logo can not be displayed in the standard output.

## Notes

The logo option is still not full working.