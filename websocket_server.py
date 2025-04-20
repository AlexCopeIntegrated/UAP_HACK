print(">>> websocket_server_with_triple_plot.py loaded")

import asyncio
import json
import numpy as np
import websockets
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from rtlsdr import RtlSdr
from output_writer import OutputWriter  # Make sure this file is in same folder

# --- Setup SDR ---
sdr = RtlSdr()
sdr.sample_rate = 2.4e6  # Hz
sdr.center_freq = 100e6  # FM radio
sdr.gain = 10

# --- Setup Output Writer ---
writer = OutputWriter("sdr_output.npy", format_type="numpy")

# --- WebSocket Handler ---
latest_samples = np.zeros(1024, dtype=np.complex64)

async def send_samples(websocket, path=None):
    print("Client connected")
    global latest_samples

    try:
        while True:
            samples = await asyncio.to_thread(sdr.read_samples, 1024)
            latest_samples = samples
            writer.write(samples)  # Write to disk!

            flattened = np.empty(samples.size * 2, dtype=np.float32)
            flattened[0::2] = samples.real
            flattened[1::2] = samples.imag

            message = {"samples": flattened[:100].tolist()}
            await websocket.send(json.dumps(message))
            await asyncio.sleep(0.05)
    except websockets.exceptions.ConnectionClosed:
        print("Client disconnected")

# --- Plotting ---
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 8))

line1, = ax1.plot([], [], lw=1)
ax1.set_title("Time Domain (Real Part)")
ax1.set_ylim(-2, 2)

line2, = ax2.plot([], [], lw=1)
ax2.set_title("Power Spectrum")
ax2.set_ylim(-80, 10)

line3, = ax3.plot([], [], lw=1)
ax3.set_title("Histogram")
ax3.set_xlim(0, 2)

def update_plot(_):
    real_part = latest_samples.real
    fft_data = 20 * np.log10(np.abs(np.fft.fftshift(np.fft.fft(latest_samples))))
    freqs = np.fft.fftshift(np.fft.fftfreq(len(latest_samples), d=1/sdr.sample_rate))

    line1.set_data(np.arange(len(real_part)), real_part)
    ax1.set_xlim(0, len(real_part))

    line2.set_data(freqs / 1e6, fft_data)
    ax2.set_xlim(freqs.min() / 1e6, freqs.max() / 1e6)

    hist_vals, bins = np.histogram(np.abs(latest_samples), bins=50, range=(0, 2))
    line3.set_data(bins[:-1], hist_vals)
    ax3.set_ylim(0, hist_vals.max() + 10)

    return line1, line2, line3

ani = FuncAnimation(fig, update_plot, interval=200)

# --- WebSocket Server ---
async def main():
    async with websockets.serve(send_samples, "0.0.0.0", 8765):
        print("Mock WebSocket server running at ws://localhost:8765")
        plt.tight_layout()
        plt.show()  # Live plot window
        await asyncio.Future()  # Keep server alive

if __name__ == "__main__":
    asyncio.run(main())
