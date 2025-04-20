#!/usr/bin/env python3
"""
Command-line interface for the RTL-SDR tool.
"""
import argparse
import sys
import numpy as np
from .sdr_reader import RTLSDRReader
from .output_writer import OutputWriter


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Capture and process RTL-SDR radio data."
    )

    parser.add_argument(
        "-f",
        "--frequency",
        type=float,
        required=True,
        help="Center frequency in Hz (e.g., 100.1e6 for 100.1 MHz)",
    )

    parser.add_argument(
        "-b",
        "--bandwidth",
        type=float,
        default=2.4e6,
        help="Bandwidth/sample rate in Hz (default: 2.4 MHz)",
    )

    parser.add_argument(
        "-g", "--gain", type=float, default=None, help="Gain in dB (default: automatic)"
    )

    parser.add_argument(
        "-n",
        "--num-samples",
        type=int,
        default=1024 * 1024,
        help="Number of samples to capture (default: 1048576)",
    )

    parser.add_argument(
        "-o", "--output", type=str, default="-", help="Output file (default: stdout)"
    )

    parser.add_argument(
        "-p", "--ppm", type=int, default=0, help="PPM frequency correction (default: 0)"
    )

    parser.add_argument(
        "--format",
        type=str,
        choices=["numpy", "raw"],
        default="numpy",
        help="Output format: numpy (binary .npy) or raw (binary I/Q samples)",
    )

    return parser.parse_args()


def main():
    """Main entry point for the RTL-SDR tool."""
    args = parse_args()

    try:
        # Initialize SDR reader
        sdr = RTLSDRReader(
            frequency=args.frequency,
            sample_rate=args.bandwidth,
            gain=args.gain,
            ppm=args.ppm,
        )

        # Capture samples
        print(
            f"Capturing {args.num_samples} samples at {args.frequency/1e6:.2f} MHz...",
            file=sys.stderr,
        )
        samples = sdr.read_samples(args.num_samples)
        print(f"Captured {len(samples)} samples", file=sys.stderr)

        # Clean up SDR device
        sdr.close()

        # Write output
        writer = OutputWriter(args.output, args.format)
        writer.write(samples)
        writer.close()

    except KeyboardInterrupt:
        print("\nCapture interrupted by user.", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
