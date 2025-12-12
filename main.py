import matplotlib.pyplot as plt
import numpy as np
import soundfile as sf

file = "22_minutes.flac"


def main():
    # Read FLAC file into numpy array (normalized float32 values)
    data, sample_rate = sf.read(file)  # Defaults to float32, normalized to [-1.0, 1.0]

    # Convert stereo to mono if needed
    if len(data.shape) > 1:
        data = np.mean(data, axis=1)

    # If you want the scipy.io.wavfile order (sample_rate, data):
    sample_rate = int(sample_rate)

    # Now 'data' is a numpy array, just like scipy.io.wavfile.read() returns
    print(f"Sample rate: {sample_rate} Hz")
    print(f"Data shape: {data.shape}")
    print(f"Data dtype: {data.dtype}")
    print(f"Duration: {len(data) / sample_rate:.2f} seconds")

    # Access the numpy array
    print(f"\nFirst 10 samples: {data[:10]}")
    print(f"Last 10 samples: {data[-10:]}")

    fig, ax = plt.subplots(figsize=(24, 18), dpi=300)

    plt.specgram(data, Fs=sample_rate, cmap="viridis")
    # plt.title("Spectrogram of 22_minutes.flac")
    plt.axis("off")
    plt.tight_layout(pad=0)
    plt.show()
    plt.savefig("spectrogram_flac.svg", transparent=True, format="svg")


if __name__ == "__main__":
    main()
