"""
Spectrogram Generator - Streamlit Web Interface

A user-friendly web interface for generating beautiful audio spectrograms.
Upload audio files or provide YouTube URLs, select from preset themes,
and customize parameters to create stunning visualizations.
"""

import streamlit as st
from pathlib import Path

# Configure page
st.set_page_config(
    page_title="Spectrogram Generator",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Import components (will create these next)
from streamlit_app.components import audio_input, theme_gallery, theme_selector, results_gallery


def initialize_session_state():
    """Initialize session state variables."""
    if "audio_data" not in st.session_state:
        st.session_state.audio_data = None
    if "sample_rate" not in st.session_state:
        st.session_state.sample_rate = None
    if "audio_source" not in st.session_state:
        st.session_state.audio_source = None
    if "audio_duration" not in st.session_state:
        st.session_state.audio_duration = None
    if "generated_images" not in st.session_state:
        st.session_state.generated_images = []
    if "selected_theme" not in st.session_state:
        st.session_state.selected_theme = "polar_grayscale"
    if "custom_title" not in st.session_state:
        st.session_state.custom_title = "Spectrogram"
    if "title_position" not in st.session_state:
        st.session_state.title_position = "top"


def main():
    """Main Streamlit application."""
    initialize_session_state()

    # Header
    st.title("🎵 Spectrogram Generator")
    st.markdown("Transform audio into beautiful visual spectrograms")

    # Sidebar - Configuration
    with st.sidebar:
        st.header("⚙️ Configuration")

        # Audio Input Section
        st.subheader("1. Audio Input")
        audio_input.render()

        st.divider()

        # Theme Selection Section
        st.subheader("2. Theme & Customization")
        theme_selector.render()

        st.divider()

        # Generation Button
        st.subheader("3. Generate")
        if st.button("🎨 Generate Spectrogram", type="primary", use_container_width=True):
            generate_spectrogram()

    # Main Area - Tabs
    tab1, tab2, tab3 = st.tabs(["🎨 Theme Gallery", "📊 Results", "ℹ️ About"])

    with tab1:
        theme_gallery.render()

    with tab2:
        results_gallery.render()

    with tab3:
        render_about()


def generate_spectrogram():
    """Generate spectrogram based on current settings."""
    from io import BytesIO
    from dataclasses import asdict
    from config import (minimal, scientific, presentation,
                       polar_minimal, polar_scientific, polar_grayscale)
    from modules.spectrogram_visualizer import SpectrogramGenerator
    from config.parameters import create_filename

    # Check if audio is loaded
    if st.session_state.audio_data is None:
        st.error("❌ Please load audio first (upload file, YouTube URL, or use sample)")
        return

    # Get theme function
    theme_map = {
        'minimal': minimal,
        'scientific': scientific,
        'presentation': presentation,
        'polar_minimal': polar_minimal,
        'polar_scientific': polar_scientific,
        'polar_grayscale': polar_grayscale,
    }

    theme_func = theme_map[st.session_state.selected_theme]

    # Create config with overrides
    config = theme_func(
        title=st.session_state.custom_title,
        title_position=st.session_state.title_position,
    )

    # Generate spectrogram
    with st.spinner("Generating spectrogram..."):
        try:
            generator = SpectrogramGenerator(config)

            # Generate to BytesIO
            import tempfile
            with tempfile.NamedTemporaryFile(suffix=f".{config.output_format}", delete=False) as tmp:
                generator.generate(
                    st.session_state.audio_data,
                    st.session_state.sample_rate,
                    tmp.name
                )
                tmp.seek(0)
                image_bytes = Path(tmp.name).read_bytes()

            # Store result
            filename = create_filename(asdict(config))
            st.session_state.generated_images.append({
                'config': config,
                'image': image_bytes,
                'filename': filename,
            })

            st.success(f"✅ Generated spectrogram: {filename}")
            st.info("💡 Switch to the Results tab to view and download your spectrogram")

        except Exception as e:
            st.error(f"❌ Error generating spectrogram: {str(e)}")


def render_about():
    """Render the About tab."""
    st.markdown("""
    ## About Spectrogram Generator

    This tool creates beautiful visual representations of audio frequency content over time.

    ### Features
    - 📁 Upload audio files (WAV, MP3, FLAC, M4A)
    - 🔗 Load from YouTube URLs
    - 🎨 6 preset themes optimized for different use cases
    - ⚙️ Customize title and position
    - 📥 Download high-quality images

    ### Themes

    **Linear Themes:**
    - **Minimal**: Clean, transparent background, subtle axes
    - **Scientific**: White background, full axes, publication-ready
    - **Presentation**: Dark background, vibrant colors, large text

    **Polar Themes:**
    - **Polar Minimal**: Circular visualization, minimal styling
    - **Polar Scientific**: Circular with full axes and labels
    - **Polar Grayscale**: High-contrast black & white circular design

    ### Tips
    - Use the sample audio to test themes before uploading your own files
    - Polar themes work best with longer audio (30+ seconds)
    - Transparent backgrounds are great for overlaying on other graphics
    - Title position can be "top" or "bottom" depending on your layout needs

    ### Technical Details
    - Spectrograms use Short-Time Fourier Transform (STFT)
    - Frequency range: 0 Hz to max_freq (varies by theme)
    - Time resolution: Controlled by window size and overlap parameters
    - Output formats: JPG, PNG (varies by theme)
    """)


if __name__ == "__main__":
    main()
