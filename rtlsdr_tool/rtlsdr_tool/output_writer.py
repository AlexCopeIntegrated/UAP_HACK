"""
Output writer module for RTL-SDR data.
"""

import sys
import numpy as np


class OutputWriter:
    """Writer for RTL-SDR data in different formats."""

    def __init__(self, output_path="-", format_type="numpy"):
        """
        Initialize the output writer.

        Args:
            output_path (str): Output path ("-" for stdout)
            format_type (str): Output format ("numpy" or "raw")
        """
        self.format_type = format_type
        self.output_path = output_path

        if output_path == "-":
            # Write to stdout in binary mode
            self.file = sys.stdout.buffer
            self.should_close = False
        else:
            # Write to file
            self.file = open(output_path, "wb")
            self.should_close = True

    def write(self, samples):
        """
        Write samples to the output.

        Args:
            samples (numpy.ndarray): Complex I/Q samples
        """
        if self.format_type == "numpy":
            # Write as .npy format (includes metadata)
            if self.output_path == "-":
                # For stdout, we need to manually create the .npy format
                # This is equivalent to np.save but writes to an already open file
                np.lib.format.write_array(self.file, np.asarray(samples))
            else:
                # For files, we can use np.save directly
                np.save(self.output_path, samples)
                # Close and reopen to prevent duplicate writes if write() is called again
                if self.should_close:
                    self.file.close()
                    self.file = open(self.output_path, "ab")
        else:  # "raw"
            # Write raw complex values as 8-byte pairs (real, imag)
            # Each complex sample is a pair of 32-bit floats
            samples.astype(np.complex64).tofile(self.file)
            self.file.flush()

    def close(self):
        """Close the output file if needed."""
        if self.should_close:
            self.file.close()
