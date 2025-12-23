"""Unified audio loading from YouTube URLs or local files."""

import os
import subprocess
from pathlib import Path
from urllib.parse import urlparse

from pytubefix import YouTube


class AudioLoader:
    """Load audio from YouTube URLs or local file paths."""

    def __init__(self, cache_dir: str = "data"):
        """
        Initialize AudioLoader with cache directory.

        Args:
            cache_dir: Directory to cache downloaded/converted audio files
        """
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def load(self, source: str) -> str:
        """
        Load audio from YouTube URL or local file path.

        Args:
            source: YouTube URL (e.g., "https://youtube.com/watch?v=...")
                   OR local file path (e.g., "data/audio.wav", "/path/to/file.flac")

        Returns:
            Path to WAV file (downloaded/converted if needed, or original if already WAV)

        Raises:
            ValueError: If source is invalid or file doesn't exist
        """
        if self._is_youtube_url(source):
            return self._download_from_youtube(source)
        else:
            return self._ensure_wav_format(source)

    def _is_youtube_url(self, source: str) -> bool:
        """
        Check if source is a YouTube URL.

        Args:
            source: String to check

        Returns:
            True if source is a YouTube URL, False otherwise
        """
        try:
            parsed = urlparse(source)
            return parsed.netloc in [
                "www.youtube.com",
                "youtube.com",
                "youtu.be",
                "m.youtube.com",
            ]
        except Exception:
            return False

    def _download_from_youtube(self, url: str) -> str:
        """
        Download audio from YouTube and convert to WAV.

        Args:
            url: YouTube video URL

        Returns:
            Path to converted WAV file

        Raises:
            ValueError: If no audio stream found or conversion fails
        """
        # Initialize YouTube object
        yt = YouTube(url)

        # Generate cache filename based on video ID
        video_id = yt.video_id
        m4a_path = self.cache_dir / f"{video_id}.m4a"
        wav_path = self.cache_dir / f"{video_id}.wav"

        # Check if WAV already exists in cache
        if wav_path.exists():
            print(f"Using cached audio: {wav_path}")
            return str(wav_path)

        # Download if m4a doesn't exist
        if not m4a_path.exists():
            print(f"Downloading audio from YouTube: {yt.title}")
            audio_stream = (
                yt.streams.filter(only_audio=True).filter(file_extension="mp4").first()
            )

            if not audio_stream:
                raise ValueError(f"No audio stream found for URL: {url}")

            # Download as m4a
            audio_stream.download(
                output_path=str(self.cache_dir), filename=m4a_path.name
            )

        # Convert m4a to WAV using ffmpeg
        print(f"Converting to WAV: {wav_path}")
        try:
            subprocess.run(
                [
                    "ffmpeg",
                    "-i",
                    str(m4a_path),
                    "-acodec",
                    "pcm_s16le",  # PCM 16-bit
                    "-ar",
                    "44100",  # Sample rate 44.1kHz
                    "-y",  # Overwrite if exists
                    str(wav_path),
                ],
                check=True,
                capture_output=True,
                text=True,
            )
        except subprocess.CalledProcessError as e:
            print(f"ffmpeg stderr: {e.stderr}")
            print(f"ffmpeg stdout: {e.stdout}")
            raise ValueError(f"Failed to convert audio: {e.stderr}")

        return str(wav_path)

    def _ensure_wav_format(self, file_path: str) -> str:
        """
        Ensure local file is in WAV format (convert if needed).

        Args:
            file_path: Path to local audio file

        Returns:
            Path to WAV file (original or converted)

        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If conversion fails
        """
        file_path = Path(file_path)

        if not file_path.exists():
            raise FileNotFoundError(f"Audio file not found: {file_path}")

        # If already WAV, return as-is
        if file_path.suffix.lower() == ".wav":
            return str(file_path)

        # Convert to WAV
        wav_path = self.cache_dir / f"{file_path.stem}.wav"

        # Check if already converted
        if wav_path.exists():
            print(f"Using cached WAV: {wav_path}")
            return str(wav_path)

        print(f"Converting {file_path.suffix} to WAV: {wav_path}")
        try:
            subprocess.run(
                [
                    "ffmpeg",
                    "-i",
                    str(file_path),
                    "-acodec",
                    "pcm_s16le",
                    "-ar",
                    "44100",
                    "-y",
                    str(wav_path),
                ],
                check=True,
                capture_output=True,
                text=True,
            )
        except subprocess.CalledProcessError as e:
            print(f"ffmpeg stderr: {e.stderr}")
            raise ValueError(f"Failed to convert audio: {e.stderr}")

        return str(wav_path)
