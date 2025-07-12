print(">>> Simple WebSocket server with sample data loaded")

import asyncio
import json
import numpy as np
import websockets
import time
import math

# Configuration
SAMPLE_RATE = 2.4e6
CENTER_FREQ = 95e6
NUM_SAMPLES = 2048

# Sample data generator class
class SampleDataGenerator:
    def __init__(self, sample_rate=2.4e6, center_freq=95e6):
        self.sample_rate = sample_rate
        self.center_freq = center_freq
        self.time_step = 0
        self.frame_count = 0
        
    def generate_samples(self, num_samples=2048):
        """Generate realistic sample radio frequency data"""
        # Time array
        t = np.arange(num_samples) / self.sample_rate + self.time_step
        
        # Generate multiple frequency components to simulate real RF signals
        # 1. Main carrier signal (simulating FM radio)
        carrier_freq = 100e3  # 100 kHz offset from center
        carrier_signal = 0.8 * np.exp(1j * 2 * np.pi * carrier_freq * t)
        
        # 2. Add some noise
        noise = 0.1 * (np.random.randn(num_samples) + 1j * np.random.randn(num_samples))
        
        # 3. Add some interference signals (simulating other stations)
        interference1 = 0.3 * np.exp(1j * 2 * np.pi * 200e3 * t + 0.5 * np.sin(2 * np.pi * 1e3 * t))
        interference2 = 0.2 * np.exp(1j * 2 * np.pi * -150e3 * t + 0.3 * np.sin(2 * np.pi * 500 * t))
        
        # 4. Add amplitude modulation to simulate varying signal strength
        am_envelope = 1 + 0.2 * np.sin(2 * np.pi * 10 * t)  # 10 Hz AM
        
        # 5. Add frequency hopping effect (simulating changing channels)
        hop_freq = 50e3 * np.sin(2 * np.pi * 0.1 * t)
        hop_signal = 0.1 * np.exp(1j * 2 * np.pi * hop_freq * t)
        
        # Combine all signals
        combined_signal = am_envelope * (carrier_signal + interference1 + interference2 + hop_signal) + noise
        
        # Add some realistic fading effects
        fading = 0.9 + 0.1 * np.sin(2 * np.pi * 0.05 * t + self.frame_count * 0.1)
        final_signal = combined_signal * fading
        
        # Update time step for next frame
        self.time_step += num_samples / self.sample_rate
        self.frame_count += 1
        
        return final_signal

# Initialize sample generator
sample_generator = SampleDataGenerator(SAMPLE_RATE, CENTER_FREQ)

# WebSocket Handler - Fixed for newer websockets library
async def send_samples(websocket):
    print("Client connected")
    try:
        while True:
            # Generate sample data
            samples = sample_generator.generate_samples(NUM_SAMPLES)
            
            # Downsample for sending
            downsampled = samples[:256]
            interleaved = np.empty(downsampled.size * 2, dtype=np.float32)
            interleaved[0::2] = downsampled.real
            interleaved[1::2] = downsampled.imag
            message = {"samples": interleaved.tolist()}
            await websocket.send(json.dumps(message))
            
            # Simulate real-time sampling rate
            await asyncio.sleep(0.1)  # 100ms delay for smooth visualization
            
    except websockets.exceptions.ConnectionClosed:
        print("Client disconnected")

# Main entry
async def main():
    async with websockets.serve(send_samples, "localhost", 8765):
        print("Sample Data WebSocket server running at ws://localhost:8765")
        print("Generating realistic RF sample data...")
        print("Open Index.html in your browser to see the visualization")
        await asyncio.Future()  # Run forever

if __name__ == "__main__":
    asyncio.run(main())