"""Audio preprocessing and formatting for spectrogram generation."""

import numpy as np
import soundfile as sf


class AudioPreprocessor:
    """Handle audio loading and preprocessing for spectrogram generation."""

    def load_audio(self, file_path: str) -> tuple[np.ndarray, int]:
        """
        Load audio file and return normalized mono data.

        Args:
            file_path: Path to audio file (WAV, FLAC, etc.)

        Returns:
            (audio_data, sample_rate) tuple
            - audio_data: Mono float32 numpy array
            - sample_rate: Integer sample rate in Hz
        """
        data, sample_rate = sf.read(file_path)

        # Convert stereo/multi-channel to mono
        data = self._convert_to_mono(data)

        return data, int(sample_rate)

    def _convert_to_mono(self, data: np.ndarray) -> np.ndarray:
        """
        Convert stereo/multi-channel audio to mono.

        Args:
            data: Audio data array

        Returns:
            Mono audio array (averaged across channels if multi-channel)
        """
        if len(data.shape) > 1:
            # Average across channels
            data = np.mean(data, axis=1)
        return data

    def trim_audio(
        self,
        data: np.ndarray,
        sample_rate: int,
        start_seconds: float = 0.0,
        end_seconds: float | None = None,
    ) -> np.ndarray:
        """
        Trim audio to specified time range.

        Args:
            data: Audio data array
            sample_rate: Sample rate in Hz
            start_seconds: Start time in seconds (default: 0.0)
            end_seconds: End time in seconds (default: None = end of audio)

        Returns:
            Trimmed audio data
        """
        start_sample = int(start_seconds * sample_rate)
        end_sample = int(end_seconds * sample_rate) if end_seconds else len(data)

        # Ensure valid range
        start_sample = max(0, start_sample)
        end_sample = min(len(data), end_sample)

        return data[start_sample:end_sample]

    def get_audio_info(self, data: np.ndarray, sample_rate: int) -> dict:
        """
        Get diagnostic information about audio data.

        Args:
            data: Audio data array
            sample_rate: Sample rate in Hz

        Returns:
            Dictionary with audio information:
            - mean: Mean amplitude
            - median: Median amplitude
            - duration: Duration in seconds
            - samples: Number of samples
            - min: Minimum amplitude
            - max: Maximum amplitude
        """
        duration = len(data) / sample_rate

        return {
            "mean": float(np.mean(data)),
            "median": float(np.median(data)),
            "duration": duration,
            "samples": len(data),
            "min": float(np.min(data)),
            "max": float(np.max(data)),
            "sample_rate": sample_rate,
        }
