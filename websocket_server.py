import asyncio
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from rtlsdr import RtlSdr
import threading

# --- SDR Setup ---
sdr = RtlSdr()
sdr.sample_rate = 2.4e6   # Hz
sdr.center_freq = 95e6    # Hz
sdr.gain = 10             # dB

latest_samples = np.zeros(1024, dtype=np.complex64)
lock = threading.Lock()

def read_sdr():
    global latest_samples
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    async def sdr_loop():
        while True:
            samples = await sdr.read_samples(2048)
            with lock:
                latest_samples = samples
            await asyncio.sleep(0.01)

    loop.run_until_complete(sdr_loop())

# --- Plot Setup ---
fig, axs = plt.subplots(3, 1, figsize=(10, 8))

line_time, = axs[0].plot([], [], lw=1)
axs[0].set_title("Time Domain (Real)")
axs[0].set_xlim(0, 1024)
axs[0].set_ylim(-100, 100)

line_psd, = axs[1].plot([], [], lw=1)
axs[1].set_title("Power Spectrum")
axs[1].set_xlim(0, sdr.sample_rate/1e6)
axs[1].set_ylim(-100, 0)

line_hist, = axs[2].plot([], [], lw=1)
axs[2].set_title("Histogram of Real Component")
axs[2].set_xlim(-150, 150)
axs[2].set_ylim(0, 300)

def update(frame):
    with lock:
        samples = latest_samples.copy()
    
    if len(samples) == 0:
        return

    # Time Domain
    line_time.set_data(np.arange(len(samples)), samples.real)

    # PSD
    freqs, psd = plt.psd(samples, NFFT=1024, Fs=sdr.sample_rate/1e6, Fc=sdr.center_freq/1e6, visible=False)
    line_psd.set_data(freqs, 10 * np.log10(psd))

    # Histogram
    hist, bins = np.histogram(samples.real, bins=100, range=(-150, 150))
    line_hist.set_data(bins[:-1], hist)

    return line_time, line_psd, line_hist

# Start background SDR thread
threading.Thread(target=read_sdr, daemon=True).start()

ani = FuncAnimation(fig, update, interval=200)
plt.tight_layout()
plt.show()
