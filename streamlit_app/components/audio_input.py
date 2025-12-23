"""Audio input component - handles file uploads, YouTube URLs, and sample audio."""

import streamlit as st
from pathlib import Path
import tempfile


def render():
    """Render the audio input UI."""
    # Input mode selection
    input_mode = st.radio(
        "Input Method",
        ["📁 Upload File", "🔗 YouTube URL", "🎵 Use Sample"],
        label_visibility="collapsed",
    )

    if input_mode == "📁 Upload File":
        render_file_upload()
    elif input_mode == "🔗 YouTube URL":
        render_youtube_input()
    else:  # Use Sample
        render_sample_audio()

    # Show audio info if loaded
    if st.session_state.audio_data is not None:
        render_audio_info()


def render_file_upload():
    """Render file upload widget."""
    uploaded_file = st.file_uploader(
        "Upload Audio File",
        type=['wav', 'mp3', 'flac', 'm4a'],
        help="Supported formats: WAV, MP3, FLAC, M4A",
    )

    if uploaded_file is not None:
        # Save to temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=Path(uploaded_file.name).suffix) as tmp:
            tmp.write(uploaded_file.getbuffer())
            tmp_path = tmp.name

        # Load audio
        load_audio_from_file(tmp_path, uploaded_file.name)


def render_youtube_input():
    """Render YouTube URL input."""
    url = st.text_input(
        "YouTube URL",
        placeholder="https://www.youtube.com/watch?v=...",
        help="Paste a YouTube video URL to extract and analyze its audio",
    )

    if url and st.button("Load from YouTube"):
        load_audio_from_youtube(url)


def render_sample_audio():
    """Render sample audio button."""
    st.info("💡 Use pre-loaded sample audio to test themes instantly")

    if st.button("Load Sample Audio", use_container_width=True):
        sample_path = "streamlit_app/assets/sample_audio.wav"
        if Path(sample_path).exists():
            load_audio_from_file(sample_path, "sample_audio.wav")
        else:
            st.error("❌ Sample audio file not found. Please add sample_audio.wav to streamlit_app/assets/")


def load_audio_from_file(file_path: str, filename: str):
    """Load audio from a file path."""
    try:
        with st.spinner(f"Loading {filename}..."):
            from modules.audio_formatter import AudioPreprocessor

            preprocessor = AudioPreprocessor()
            audio_data, sample_rate = preprocessor.load_audio(file_path)

            # Store in session state
            st.session_state.audio_data = audio_data
            st.session_state.sample_rate = sample_rate
            st.session_state.audio_source = filename
            st.session_state.audio_duration = len(audio_data) / sample_rate

            st.success(f"✅ Loaded: {filename}")

    except Exception as e:
        st.error(f"❌ Error loading audio: {str(e)}")


def load_audio_from_youtube(url: str):
    """Load audio from YouTube URL."""
    try:
        with st.spinner("Downloading from YouTube..."):
            from modules.audio_loader import AudioLoader
            from modules.audio_formatter import AudioPreprocessor

            # Download
            loader = AudioLoader()
            wav_path = loader.load(url)

            # Load audio data
            preprocessor = AudioPreprocessor()
            audio_data, sample_rate = preprocessor.load_audio(wav_path)

            # Store in session state
            st.session_state.audio_data = audio_data
            st.session_state.sample_rate = sample_rate
            st.session_state.audio_source = url
            st.session_state.audio_duration = len(audio_data) / sample_rate

            st.success(f"✅ Loaded from YouTube")

    except Exception as e:
        st.error(f"❌ Error loading YouTube audio: {str(e)}")


def render_audio_info():
    """Display information about loaded audio."""
    st.divider()
    st.caption("**Audio Information**")

    duration_mins = int(st.session_state.audio_duration // 60)
    duration_secs = int(st.session_state.audio_duration % 60)

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Duration", f"{duration_mins}:{duration_secs:02d}")
    with col2:
        st.metric("Sample Rate", f"{st.session_state.sample_rate} Hz")

    # Show trim slider if audio is longer than 60 seconds
    if st.session_state.audio_duration > 60:
        st.caption("⚠️ Long audio detected")
        trim_start = st.slider(
            "Trim Start (seconds)",
            0.0,
            min(60.0, st.session_state.audio_duration),
            0.0,
            help="Skip the first N seconds for faster processing"
        )

        if trim_start > 0:
            # Apply trim
            from modules.audio_formatter import AudioPreprocessor
            preprocessor = AudioPreprocessor()
            trimmed = preprocessor.trim_audio(
                st.session_state.audio_data,
                st.session_state.sample_rate,
                start_seconds=trim_start
            )
            st.session_state.audio_data = trimmed
            st.info(f"✂️ Trimmed {trim_start}s from start")
