import os
import subprocess

import matplotlib.pyplot as plt
import numpy as np
import soundfile as sf
from matplotlib.colors import PowerNorm
from pytubefix import YouTube


def load_audio_file(youtube_url: str, path: str):
    # Init the video
    yt = YouTube(youtube_url)

    # Extract the first MP4 audio file found
    mp4_stream = yt.streams.filter(only_audio=True).filter(file_extension="mp4").first()

    if mp4_stream:
        # Create directory if it doesn't exist
        output_dir = os.path.dirname(path)
        os.makedirs(output_dir, exist_ok=True)

        # Download as m4a - pytubefix download() takes output_path and filename separately
        base_filename = os.path.basename(path).replace(".mp4", ".m4a")
        mp4_stream.download(output_path=output_dir, filename=base_filename)
        m4a_path = os.path.join(output_dir, base_filename)

        # Convert m4a to wav using ffmpeg
        wav_path = path.replace(".mp4", ".wav")
        try:
            subprocess.run(
                [
                    "ffmpeg",
                    "-i",
                    m4a_path,
                    "-acodec",
                    "pcm_s16le",  # Convert to PCM 16-bit
                    "-ar",
                    "44100",  # Sample rate 44.1kHz
                    "-y",  # Overwrite output file if exists
                    wav_path,
                ],
                check=True,
                capture_output=True,
                text=True,
            )
        except subprocess.CalledProcessError as e:
            print(f"ffmpeg stderr: {e.stderr}")
            print(f"ffmpeg stdout: {e.stdout}")
            raise

        return wav_path
    else:
        raise ValueError(f"No MP4 stream found for URL: {youtube_url}")


def decode_audio(path: str):
    data, sample_rate = sf.read(path)

    # Convert stereo to mono if needed
    if len(data.shape) > 1:
        data = np.mean(data, axis=1)

    # If you want the scipy.io.wavfile order (sample_rate, data):
    sample_rate = int(sample_rate)

    return data, sample_rate


def create_spectrogram(data, sample_rate, **kwargs):
    fig, ax = plt.subplots(figsize=(12, 10), dpi=300)

    plt.specgram(data, Fs=sample_rate, **kwargs)
    # plt.title("Spectrogram of 22_minutes.flac")
    plt.axis("off")
    plt.tight_layout(pad=0)
    plt.savefig("spectrogram_flac.png", transparent=True, format="png")
    plt.show()

    return None


def main(youtube_url: str):
    path = "data/audio_test.mp4"

    wav_path = load_audio_file(youtube_url=youtube_url, path=path)

    data, sample_rate = decode_audio(path=wav_path)

    # Run the spectrogram to get the data
    Pxx, freqs, bins, im = plt.specgram(data, Fs=sample_rate, scale="dB")
    print(
        f"Spectrogram range: {10 * np.log10(Pxx.min())} to {10 * np.log10(Pxx.max())} dB"
    )

    create_spectrogram(
        data=data,
        sample_rate=sample_rate,
        norm=PowerNorm(
            gamma=4,
        ),
        # scale="dB",
    )

    print(f"Mean: {np.mean(data)}")
    print(f"Median: {np.median(data)}")

    # Now 'data' is a numpy array, just like scipy.io.wavfile.read() returns
    print(f"Sample rate: {sample_rate} Hz")
    print(f"Data shape: {data.shape}")
    print(f"Data dtype: {data.dtype}")
    print(f"Duration: {len(data) / sample_rate:.2f} seconds")

    # Access the numpy array
    print(f"\nFirst 10 samples: {data[:10]}")
    print(f"Last 10 samples: {data[-10:]}")


if __name__ == "__main__":
    main("https://www.youtube.com/watch?v=JiPkST80jMU&list=RDJiPkST80jMU")
