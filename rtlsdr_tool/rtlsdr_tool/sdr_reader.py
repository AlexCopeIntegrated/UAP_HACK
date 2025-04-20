"""
RTL-SDR reader module that interfaces with the RTL-SDR device.
"""

import numpy as np
from rtlsdr import RtlSdr


class RTLSDRReader:
    """Interface for the RTL-SDR device."""

    def __init__(self, frequency, sample_rate=2.4e6, gain=None, ppm=0):
        """
        Initialize the RTL-SDR device.

        Args:
            frequency (float): Center frequency in Hz
            sample_rate (float): Sample rate in Hz (default: 2.4 MHz)
            gain (float or None): Gain in dB (None for auto)
            ppm (int): Frequency correction in ppm
        """
        self.sdr = RtlSdr()

        # Configure device
        self.sdr.sample_rate = sample_rate
        self.sdr.center_freq = frequency

        if gain is not None:
            self.sdr.gain = gain
        else:
            # Use automatic gain
            self.sdr.gain = "auto"

        if ppm != 0:
            self.sdr.freq_correction = ppm

        self.device_info = {
            "center_freq": self.sdr.center_freq,
            "sample_rate": self.sdr.sample_rate,
            "gain": self.sdr.gain,
            "freq_correction": self.sdr.freq_correction,
        }

    def read_samples(self, num_samples):
        """
        Read samples from the RTL-SDR device.

        Args:
            num_samples (int): Number of samples to read

        Returns:
            numpy.ndarray: Complex I/Q samples
        """
        return self.sdr.read_samples(num_samples)

    def get_device_info(self):
        """
        Get device information.

        Returns:
            dict: Device information
        """
        return self.device_info

    def close(self):
        """Close the RTL-SDR device."""
        self.sdr.close()
