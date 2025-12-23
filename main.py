"""
Spectrogram Generator - Generate audio spectrograms with flexible configuration.

Supports:
- YouTube URLs or local audio files
- Linear and polar projections
- Parameter grids for batch generation
- Preconfigured themes (minimal, scientific, presentation, etc.)
"""

from datetime import datetime
from pathlib import Path

from config.parameters import ParameterGrid, create_filename
from config.themes import get_theme
from modules.audio_formatter import AudioPreprocessor
from modules.audio_loader import AudioLoader
from modules.spectrogram_visualizer import SpectrogramConfig, SpectrogramGenerator


def main(
    source: str,
    parameter_grid: dict | None = None,
    theme: str | None = "minimal",
    trim_start: float = 3.0,
    output_dir: str | None = None,
):
    """
    Generate spectrograms from audio source with parameter grid support.

    Args:
        source: YouTube URL or local audio file path
                Examples:
                - "https://www.youtube.com/watch?v=..."
                - "data/audio_test.wav"
                - "/path/to/audio.flac"
        parameter_grid: Dict of parameter variations for batch generation
                       Example: {'cmap': ['viridis', 'magma'], 'dpi': [150, 300]}
                       If None, generates single spectrogram using theme
        theme: Base theme name (from config/themes.py)
               Options: 'minimal', 'scientific', 'presentation',
                       'polar_minimal', 'polar_scientific'
        trim_start: Seconds to trim from start of audio
        output_dir: Custom output directory (defaults to timestamped folder)
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

    if parameter_grid:
        # Multi-spectrogram mode: parameter grid
        print("      Mode: Parameter grid")
        print(f"      Base theme: {theme}")

        # Get base configuration from theme
        base_config = get_theme(theme) if theme else SpectrogramConfig()

        # Create parameter grid
        grid = ParameterGrid(parameter_grid, base_config=base_config)
        total = grid.count()
        print(f"      Total combinations: {total}")

        # Create timestamped output directory
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        out_dir = (
            Path(output_dir)
            if output_dir
            else Path("output") / f"spectrograms_{timestamp}"
        )
        out_dir.mkdir(parents=True, exist_ok=True)
        print(f"      Output directory: {out_dir}")

        # Generate all combinations
        print("\n      Generating spectrograms:")
        for i, params in enumerate(grid.generate_combinations(), 1):
            config = SpectrogramConfig(**params)
            generator = SpectrogramGenerator(config)
            filename = create_filename(params)

            print(f"      [{i}/{total}] {filename}")
            generator.generate(audio_data, sample_rate, str(out_dir / filename))

        print("\n" + "=" * 60)
        print(f"✓ Completed! {total} spectrograms saved to:")
        print(f"  {out_dir}")
        print("=" * 60)

    else:
        # Single spectrogram mode: use theme directly
        print("      Mode: Single spectrogram")
        print(f"      Theme: {theme if theme else 'default'}")

        config = get_theme(theme) if theme else SpectrogramConfig()
        generator = SpectrogramGenerator(config)

        # Determine output path
        if output_dir:
            output_path = output_dir
        else:
            theme_name = theme if theme else "default"
            output_path = f"spectrogram_{theme_name}.{config.output_format}"

        print(f"      Output: {output_path}")

        generator.generate(audio_data, sample_rate, output_path)

        print("\n" + "=" * 60)
        print("✓ Completed! Spectrogram saved as:")
        print(f"  {output_path}")
        print("=" * 60)


if __name__ == "__main__":
    # Example 1: Single spectrogram from local file using minimal theme
    # main("data/audio_test.wav", theme="minimal")

    # Example 2: Single spectrogram with different theme
    # main("data/audio_test.wav", theme="scientific")

    # Example 3: Parameter grid from local file (colormap comparison)
    # main(
    #     source="data/audio_test.wav",
    #     parameter_grid={
    #         "cmap": ["viridis", "magma", "inferno"],
    #         "projection": ["linear", "polar"],
    #     },
    #     theme="minimal",
    #     trim_start=3.0,
    # )

    # Example 4: Parameter grid from YouTube URL (requires YouTube download)
    main(
        source="https://www.youtube.com/watch?v=QwxYiVXYyVs&list=RDQwxYiVXYyVs&start_radio=1&pp=ygUUMjAwMSBhIHNwYWNlIG9keXNzZXmgBwE%3D",
        parameter_grid={
            "cmap": ["gray_r"],
            "projection": ["polar"],
            "dpi": [300],
            "title_font": ["Helvetica", "Arial", "Courier New"],
            "title": ["Spectrogram", "Audio Visualization", "Frequency Analysis"],
        },
        theme="minimal",
    )

    # Example 5: DPI comparison
    # main(
    #     source="data/audio_test.wav",
    #     parameter_grid={'dpi': [72, 150, 300, 600]},
    #     theme="minimal"
    # )

    # Example 6: Gamma comparison
    # main(
    #     source="data/audio_test.wav",
    #     parameter_grid={'norm_gamma': [1, 2, 3, 4, 5, 6, 8, 10]},
    #     theme="minimal"
    # )
