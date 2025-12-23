# Spectrogram Generator - Streamlit Interface

A user-friendly web interface for generating beautiful audio spectrograms.

## Features

- 📁 **Upload Audio Files** - Support for WAV, MP3, FLAC, M4A
- 🔗 **YouTube URLs** - Extract and visualize audio from YouTube videos
- 🎨 **6 Preset Themes** - Choose from carefully designed themes
- ⚙️ **Customization** - Adjust title and position
- 📥 **Easy Download** - Download individual images or all as ZIP

## Quick Start

### 1. Generate Theme Previews (One-time setup)

First, add a sample audio file to `streamlit_app/assets/sample_audio.wav`, then run:

```bash
python generate_previews.py
```

This will create preview images in `streamlit_app/assets/theme_previews/`.

### 2. Run the App

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## Usage

1. **Select a Theme** - Browse the gallery or choose from the dropdown
2. **Load Audio** - Upload a file, paste YouTube URL, or use sample audio
3. **Customize** - Set title and position
4. **Generate** - Click the generate button
5. **Download** - Get your spectrogram as a high-quality image

## Themes

### Linear Themes
- **Minimal** - Clean, transparent background
- **Scientific** - Publication-ready with full axes
- **Presentation** - Dark background for slides

### Polar Themes
- **Polar Minimal** - Circular visualization
- **Polar Scientific** - Technical circular design
- **Polar Grayscale** - High-contrast B&W

## File Structure

```
streamlit_app/
├── components/          # UI components
│   ├── audio_input.py
│   ├── theme_gallery.py
│   ├── theme_selector.py
│   └── results_gallery.py
├── utils/              # Utility functions
├── assets/
│   ├── sample_audio.wav         # Sample audio for testing
│   └── theme_previews/          # Generated preview images
└── README.md
```

## Tips

- Use sample audio to test themes before uploading your own
- Polar themes work best with longer audio (30+ seconds)
- Transparent backgrounds are great for overlays
- You can generate multiple spectrograms in one session

## Development

The app is built using:
- **Streamlit** - Web framework
- **Existing modules** - Reuses main.py logic
- **Session state** - Maintains user data across interactions
