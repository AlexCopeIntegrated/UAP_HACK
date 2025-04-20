print(">>> websocket_server_with_triple_plot.py loaded")

import asyncio
import json
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import websockets

# Global buffer for latest samples
latest_samples = np.zeros(1024, dtype=np.complex64)

# --- WebSocket Handler ---
async def send_samples(websocket, path=None):
    global latest_samples
    print("Client connected")

    try:
        while True:
            # Generate mock complex I/Q samples
            samples = (np.random.randn(1024) + 1j * np.random.randn(1024)).astype(np.complex64)
            latest_samples = samples  # Update global buffer

            # Send first 100 samples to client
            flattened = np.empty(samples.size * 2, dtype=np.float32)
            flattened[0::2] = samples.real
            flattened[1::2] = samples.imag
            message = {
                "samples": flattened[:100].tolist()
            }
            await websocket.send(json.dumps(message))
            await asyncio.sleep(0.1)
    except websockets.exceptions.ConnectionClosed:
        print("Client disconnected")

# --- Matplotlib Plot Setup ---
fig, axes = plt.subplots(3, 1, figsize=(10, 8), tight_layout=True)

# Power Spectrum
ps_line, = axes[0].plot([], [], lw=1.5)
axes[0].set_title("Power Spectrum")
axes[0].set_xlabel("Frequency Bin")
axes[0].set_ylabel("Power (dB)")
axes[0].set_ylim(-50, 10)
axes[0].set_xlim(0, 1024)

# Time Domain Signal (Real Part)
time_line, = axes[1].plot([], [], lw=1.5)
axes[1].set_title("Time-Domain Signal (Real)")
axes[1].set_xlabel("Sample Index")
axes[1].set_ylabel("Amplitude")
axes[1].set_ylim(-5, 5)
axes[1].set_xlim(0, 1024)

# Constellation Diagram (I vs Q)
constellation = axes[2].scatter([], [], s=10)
axes[2].set_title("Constellation Diagram")
axes[2].set_xlabel("In-Phase (I)")
axes[2].set_ylabel("Quadrature (Q)")
axes[2].set_xlim(-5, 5)
axes[2].set_ylim(-5, 5)

# --- Animation Function ---
def update_plot(frame):
    global latest_samples
    if latest_samples.size == 0:
        return ps_line, time_line, constellation

    # Power spectrum
    psd = 10 * np.log10(np.abs(np.fft.fftshift(np.fft.fft(latest_samples)))**2 + 1e-12)
    ps_line.set_ydata(psd)
    ps_line.set_xdata(np.arange(len(psd)))

    # Time-domain (real)
    time_line.set_ydata(latest_samples.real)
    time_line.set_xdata(np.arange(len(latest_samples)))

    # Constellation
    constellation.set_offsets(np.column_stack((latest_samples.real, latest_samples.imag)))

    return ps_line, time_line, constellation

# --- Start Plot Animation ---
def start_plot():
    ani = FuncAnimation(fig, update_plot, interval=200)
    plt.show()

# --- Async Main ---
async def main():
    server = websockets.serve(send_samples, "localhost", 8765)
    print("Mock WebSocket server running at ws://localhost:8765")

    await asyncio.gather(server, loop.run_in_executor(None, start_plot))

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
