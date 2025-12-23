"""
Spectrogram Generator - Generate audio spectrograms with flexible configuration.

Supports:
- YouTube URLs or local audio files
- Linear and polar projections
- Parameter grids for batch generation
- Preconfigured themes (minimal, scientific, presentation, etc.)
"""

from dataclasses import asdict
from datetime import datetime
from pathlib import Path

from config import minimal
from config.parameters import create_filename
from modules.audio_formatter import AudioPreprocessor
from modules.audio_loader import AudioLoader
from modules.spectrogram_visualizer import SpectrogramConfig, SpectrogramGenerator


def main(
    source: str,
    config: SpectrogramConfig | None = None,
    configs: list[SpectrogramConfig] | None = None,
    trim_start: float = 3.0,
    output_dir: str | None = None,
):
    """
    Generate spectrograms from audio source.

    Args:
        source: YouTube URL or local audio file path
                Examples:
                - "https://www.youtube.com/watch?v=..."
                - "data/audio_test.wav"
                - "/path/to/audio.flac"
        config: Single SpectrogramConfig for single spectrogram mode
                If None, uses minimal() theme as default
        configs: List of SpectrogramConfigs for batch generation mode
                 If provided, generates multiple spectrograms
        trim_start: Seconds to trim from start of audio
        output_dir: Custom output directory (defaults to timestamped folder for batch mode)
    """
    print("=" * 60)
    print("Spectrogram Generator")
    print("=" * 60)

    # 1. Load audio from any source
    print("\n[1/3] Loading audio from source...")
    print(f"      Source: {source}")
    loader = AudioLoader()
    wav_path = loader.load(source)
    print(f"      WAV file: {wav_path}")

    # 2. Preprocess audio
    print("\n[2/3] Preprocessing audio...")
    preprocessor = AudioPreprocessor()
    audio_data, sample_rate = preprocessor.load_audio(wav_path)

    # Trim audio if requested
    if trim_start > 0:
        print(f"      Trimming first {trim_start} seconds...")
        audio_data = preprocessor.trim_audio(
            audio_data, sample_rate, start_seconds=trim_start
        )

    # Print diagnostics
    info = preprocessor.get_audio_info(audio_data, sample_rate)
    print(f"      Sample rate: {info['sample_rate']} Hz")
    print(f"      Duration: {info['duration']:.2f} seconds")
    print(f"      Samples: {info['samples']:,}")
    print(f"      Mean amplitude: {info['mean']:.6f}")
    print(f"      Median amplitude: {info['median']:.6f}")

    # 3. Generate spectrograms
    print("\n[3/3] Generating spectrograms...")

    if configs:
        # Batch mode: generate multiple spectrograms
        print("      Mode: Batch generation")
        total = len(configs)
        print(f"      Total spectrograms: {total}")

        # Create timestamped output directory
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        out_dir = (
            Path(output_dir)
            if output_dir
            else Path("output") / f"spectrograms_{timestamp}"
        )
        out_dir.mkdir(parents=True, exist_ok=True)
        print(f"      Output directory: {out_dir}")

        # Generate all spectrograms
        print("\n      Generating spectrograms:")
        for i, cfg in enumerate(configs, 1):
            generator = SpectrogramGenerator(cfg)
            filename = create_filename(asdict(cfg))

            print(f"      [{i}/{total}] {filename}")
            generator.generate(audio_data, sample_rate, str(out_dir / filename))

        print("\n" + "=" * 60)
        print(f"✓ Completed! {total} spectrograms saved to:")
        print(f"  {out_dir}")
        print("=" * 60)

    else:
        # Single spectrogram mode
        print("      Mode: Single spectrogram")

        cfg = config or minimal()  # Default to minimal theme
        generator = SpectrogramGenerator(cfg)

        # Determine output path
        if output_dir:
            output_path = output_dir
        else:
            output_path = f"spectrogram.{cfg.output_format}"

        print(f"      Output: {output_path}")

        generator.generate(audio_data, sample_rate, output_path)

        print("\n" + "=" * 60)
        print("✓ Completed! Spectrogram saved as:")
        print(f"  {output_path}")
        print("=" * 60)


if __name__ == "__main__":
    # Import theme functions for examples
    from config import minimal, polar_grayscale

    # Example 1: Single spectrogram using default minimal theme
    # main("data/audio_test.wav")

    # Example 2: Single spectrogram with fine-tuned theme
    # main("data/audio_test.wav", config=minimal(dpi=600, cmap="viridis"))

    # Example 3: Single spectrogram with scientific theme
    # main("data/audio_test.wav", config=scientific())

    # Example 4: Batch generation - font comparison
    # main(
    #     source="data/audio_test.wav",
    #     configs=[
    #         minimal(title_font="Helvetica"),
    #         minimal(title_font="Arial"),
    #         minimal(title_font="Courier New"),
    #     ],
    #     trim_start=3.0,
    # )

    # Example 5: Batch generation - colormap comparison
    # main(
    #     source="data/audio_test.wav",
    #     configs=[
    #         minimal(cmap="viridis"),
    #         minimal(cmap="magma"),
    #         minimal(cmap="inferno"),
    #         minimal(cmap="plasma"),
    #     ],
    # )

    # Example 6: Batch generation - theme comparison
    # main(
    #     source="data/audio_test.wav",
    #     configs=[
    #         minimal(),
    #         scientific(),
    #         presentation(),
    #         polar_minimal(),
    #     ],
    # )

    # Example 7: Batch generation from YouTube with fine-tuning
    main(
        source="https://www.youtube.com/watch?v=QwxYiVXYyVs&list=RDQwxYiVXYyVs&start_radio=1&pp=ygUUMjAwMSBhIHNwYWNlIG9keXNzZXmgBwE%3D",
        configs=[
            polar_grayscale(
                title_font="Helvetica",
                title="2001: A Space Odyssey\nSpectrogram",
                title_position="top",
            ),
            polar_grayscale(
                title_font="Arial",
                title="2001: A Space Odyssey\nSpectrogram",
                title_position="bottom",
            ),
            polar_grayscale(
                title_font="Courier New",
                title="2001: A Space Odyssey\nSpectrogram",
                title_position="left",
            ),
        ],
    )

    # Example 8: DPI comparison
    # main(
    #     source="data/audio_test.wav",
    #     configs=[
    #         minimal(dpi=72),
    #         minimal(dpi=150),
    #         minimal(dpi=300),
    #         minimal(dpi=600),
    #     ],
    # )

    # Example 9: Gamma comparison
    # main(
    #     source="data/audio_test.wav",
    #     configs=[
    #         minimal(norm_gamma=gamma)
    #         for gamma in [1, 2, 3, 4, 5, 6, 8, 10]
    #     ],
    # )
