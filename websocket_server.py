print(">>> websocket_server_with_triple_plot.py loaded")

import asyncio
import json
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from rtlsdr import RtlSdr
import websockets
from output_writer import OutputWriter

# SDR Setup
sdr = RtlSdr()
sdr.sample_rate = 2.4e6
sdr.center_freq = 95e6
sdr.gain = 10

# Output writer (writes to file)
writer = OutputWriter("samples.npy", format_type="numpy")

# Async Queue for sample sharing between plot and websocket
sample_queue = asyncio.Queue()

# WebSocket Handler
async def send_samples(websocket, path):
    print("Client connected")
    try:
        while True:
            samples = await sample_queue.get()
            # Downsample for sending
            downsampled = samples[:256]
            interleaved = np.empty(downsampled.size * 2, dtype=np.float32)
            interleaved[0::2] = downsampled.real
            interleaved[1::2] = downsampled.imag
            message = {"samples": interleaved.tolist()}
            await websocket.send(json.dumps(message))
    except websockets.exceptions.ConnectionClosed:
        print("Client disconnected")

# Plotting
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 8))
line1, = ax1.plot([], [], lw=1)
line2, = ax2.plot([], [], lw=1)
img = ax3.imshow(np.zeros((100, 512)), aspect='auto', cmap='plasma', extent=[0, 1, 0, 1])
waterfall_data = []

def init_plot():
    ax1.set_title("Time Domain")
    ax2.set_title("Power Spectrum")
    ax3.set_title("Waterfall")
    return line1, line2, img

def update_plot(frame):
    if not hasattr(update_plot, "samples"):
        return line1, line2, img
    samples = update_plot.samples
    if samples is None:
        return line1, line2, img

    # Time domain
    line1.set_data(np.arange(len(samples)), samples.real)
    ax1.set_xlim(0, len(samples))
    ax1.set_ylim(-1, 1)

    # Frequency domain
    fft_vals = np.fft.fftshift(np.fft.fft(samples, 1024))
    psd_vals = 20 * np.log10(np.abs(fft_vals) + 1e-6)
    freqs = np.fft.fftshift(np.fft.fftfreq(1024, d=1/sdr.sample_rate))
    line2.set_data(freqs / 1e6, psd_vals)
    ax2.set_xlim(freqs[0] / 1e6, freqs[-1] / 1e6)
    ax2.set_ylim(psd_vals.min(), psd_vals.max())

    # Waterfall
    new_row = psd_vals[np.newaxis, :]
    waterfall_data.append(new_row)
    if len(waterfall_data) > 100:
        waterfall_data.pop(0)
    img.set_data(np.vstack(waterfall_data))
    img.set_extent([freqs[0]/1e6, freqs[-1]/1e6, 0, len(waterfall_data)])
    return line1, line2, img

ani = FuncAnimation(fig, update_plot, init_func=init_plot, interval=200, blit=False, cache_frame_data=False)

# Sample Reader Task
async def sample_reader():
    while True:
        samples = sdr.read_samples(2048)
        writer.write(samples)
        await sample_queue.put(samples)
        update_plot.samples = samples

# Main entry
async def main():
    async with websockets.serve(send_samples, "localhost", 8765):
        print("Mock WebSocket server running at ws://localhost:8765")
        await asyncio.gather(
            sample_reader(),
        )

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(main())
    plt.show()

