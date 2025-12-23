"""Generate theme preview images for Streamlit app.

Run this script once to generate preview images for all themes.
The previews will be used in the Streamlit theme gallery.

Usage:
    python generate_previews.py
"""

from pathlib import Path
from config import minimal, scientific, presentation, polar_minimal, polar_scientific, polar_grayscale
from modules.audio_formatter import AudioPreprocessor
from modules.spectrogram_visualizer import SpectrogramGenerator


def main():
    """Generate preview images for all themes."""
    # Load sample audio
    sample_audio_path = "streamlit_app/assets/sample_audio.wav"

    if not Path(sample_audio_path).exists():
        print(f"❌ Sample audio not found: {sample_audio_path}")
        print("   Please add a sample audio file first.")
        return

    print("Loading sample audio...")
    preprocessor = AudioPreprocessor()
    audio_data, sample_rate = preprocessor.load_audio(sample_audio_path)

    # Trim to first 30 seconds for previews
    if len(audio_data) / sample_rate > 30:
        audio_data = preprocessor.trim_audio(audio_data, sample_rate, start_seconds=0, end_seconds=30)

    print(f"✓ Loaded {len(audio_data) / sample_rate:.1f}s of audio at {sample_rate}Hz")

    # Define themes
    themes = {
        'minimal': minimal(),
        'scientific': scientific(),
        'presentation': presentation(),
        'polar_minimal': polar_minimal(),
        'polar_scientific': polar_scientific(),
        'polar_grayscale': polar_grayscale(),
    }

    # Create output directory
    output_dir = Path("streamlit_app/assets/theme_previews")
    output_dir.mkdir(parents=True, exist_ok=True)

    # Generate preview for each theme
    print(f"\nGenerating {len(themes)} theme previews...")
    for name, config in themes.items():
        print(f"  [{name}] Generating...")
        generator = SpectrogramGenerator(config)
        output_path = output_dir / f"{name}.{config.output_format}"
        generator.generate(audio_data, sample_rate, str(output_path))
        print(f"  [{name}] ✓ Saved to {output_path}")

    print(f"\n✅ All previews generated successfully!")
    print(f"   Output: {output_dir}")


if __name__ == "__main__":
    main()
