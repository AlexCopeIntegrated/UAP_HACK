import asyncio
import websockets
import numpy as np
from rtlsdr import RtlSdr
import json

class RTLSDRReader:
    def __init__(self, frequency, sample_rate=2.4e6, gain=None, ppm=0):
        self.sdr = RtlSdr()
        self.sdr.sample_rate = sample_rate
        self.sdr.center_freq = frequency
        self.sdr.gain = gain if gain is not None else self.sdr.get_gain()
        self.sdr.freq_correction = ppm

    def read_samples(self, num_samples):
        return self.sdr.read_samples(num_samples)

    def close(self):
        self.sdr.close()

async def send_samples(websocket, path):
    freq = 100e6      # 100 MHz
    sample_rate = 2.4e6
    gain = 20         # in dB
    chunk_size = 16384

    reader = RTLSDRReader(frequency=freq, sample_rate=sample_rate, gain=gain)

    try:
        while True:
            samples = reader.read_samples(chunk_size)
            # Convert complex samples to JSON (or your chosen format)
            # Here, we're sending raw float32 values (real + imag) as a simple example
            data = {
                'samples': samples.astype(np.float32).tolist(),
            }
            await websocket.send(json.dumps(data))  # Send to WebSocket
    except asyncio.CancelledError:
        print("Connection closed.")
    finally:
        reader.close()

start_server = websockets.serve(send_samples, "localhost", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
print("WebSocket server running at ws://localhost:8765")
asyncio.get_event_loop().run_forever()