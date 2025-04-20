# RTL-SDR Tool

A command-line utility for capturing and processing RTL-SDR radio data.

## Features

- Read data from RTL-SDR USB devices
- Configure frequency, bandwidth, and gain settings
- Output data to stdout or file
- Choose between standardized binary formats (NumPy .npy or raw I/Q samples)

## Installation

### Prerequisites

- Python 3.6 or higher
- RTL-SDR USB device
- RTL-SDR USB drivers installed

### Installing

```
pip install -r requirements.txt
python setup.py install
```

Or install in development mode:

```
pip install -r requirements.txt
python setup.py develop
```

## Usage

```
rtlsdr-tool -f FREQUENCY [-b BANDWIDTH] [-g GAIN] [-n NUM_SAMPLES] 
           [-o OUTPUT] [-p PPM] [--format {numpy,raw}]
```

### Required Arguments

- `-f, --frequency`: Center frequency in Hz (e.g., 100.1e6 for 100.1 MHz)

### Optional Arguments

- `-b, --bandwidth`: Bandwidth/sample rate in Hz (default: 2.4 MHz)
- `-g, --gain`: Gain in dB (default: automatic)
- `-n, --num-samples`: Number of samples to capture (default: 1048576)
- `-o, --output`: Output file (default: stdout)
- `-p, --ppm`: PPM frequency correction (default: 0)
- `--format`: Output format - numpy (binary .npy) or raw (binary I/Q samples)

## Examples

Listen to an FM radio station at 100.1 MHz and save as a NumPy file:

```
rtlsdr-tool -f 100.1e6 -o fmradio.npy
```

Capture data at 915 MHz with custom gain and output raw samples:

```
rtlsdr-tool -f 915e6 -g 42 -n 2000000 -o samples.raw --format raw
```

Stream samples to another program via pipe:

```
rtlsdr-tool -f 145.5e6 | other-program
```

## Output Formats

### NumPy (.npy)

The default format is NumPy's .npy binary format. This preserves the complex I/Q samples in a format that's easy to load in Python with `numpy.load()`.

### Raw I/Q Samples

The raw format writes the complex I/Q samples as pairs of 32-bit floats (8 bytes per complex sample), with no header or metadata.

## License

This project is licensed under the MIT License.

## Acknowledgements

- [pyrtlsdr](https://github.com/roger-/pyrtlsdr) - Python wrapper for librtlsdr 