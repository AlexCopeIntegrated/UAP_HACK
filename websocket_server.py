import asyncio
import json
import numpy as np
from rtlsdr import RtlSdr
import websockets

# --- RTL-SDR Setup ---
sdr = RtlSdr()
sdr.sample_rate = 2.4e6  # Hz
sdr.center_freq = 100e6  # 100 MHz
sdr.gain = 'auto'

# --- WebSocket Handler ---
async def send_samples(websocket, path):
    print("Client connected")

    try:
        while True:
            # Read samples from RTL-SDR
            samples = await sdr.read_samples_async(num_samples=1024, num_callbacks=1)
            samples = samples[0]  # unwrap from callback

            # Convert complex64 to real + imag list
            flattened = np.empty(samples.size * 2, dtype=np.float32)
            flattened[0::2] = samples.real
            flattened[1::2] = samples.imag

            # Send as JSON
            message = {
                "samples": flattened[:100].tolist()  # just a snippet for demo
            }
            await websocket.send(json.dumps(message))

            await asyncio.sleep(0.1)
    except websockets.exceptions.ConnectionClosed:
        print("Client disconnected")

# --- Server Startup ---
async def main():
    async with websockets.serve(send_samples, "localhost", 8765):
        print("WebSocket server running at ws://localhost:8765")
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    try:
        asyncio.run(main())
    finally:
        sdr.close()
