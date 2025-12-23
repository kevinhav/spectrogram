"""Theme selector component - allows users to select and customize themes."""

import streamlit as st


def render():
    """Render the theme selection and customization UI."""
    # Theme selection
    selected = st.selectbox(
        "Theme",
        options=['minimal', 'scientific', 'presentation',
                'polar_minimal', 'polar_scientific', 'polar_grayscale'],
        index=['minimal', 'scientific', 'presentation',
               'polar_minimal', 'polar_scientific', 'polar_grayscale'].index(st.session_state.selected_theme),
        format_func=lambda x: x.replace('_', ' ').title(),
        help="Choose a preset theme - preview in the Theme Gallery tab",
    )

    # Update session state
    if selected != st.session_state.selected_theme:
        st.session_state.selected_theme = selected

    # Show selected theme info
    st.caption(f"✓ Selected: **{selected.replace('_', ' ').title()}**")

    st.divider()

    # Customization section
    st.caption("**Customization**")

    # Title input
    title = st.text_input(
        "Title",
        value=st.session_state.custom_title,
        help="Text to display on the spectrogram",
    )
    if title != st.session_state.custom_title:
        st.session_state.custom_title = title

    # Title position
    title_pos = st.selectbox(
        "Title Position",
        options=["top", "bottom"],
        index=0 if st.session_state.title_position == "top" else 1,
        help="Where to place the title on the spectrogram",
    )
    if title_pos != st.session_state.title_position:
        st.session_state.title_position = title_pos

    # Show theme-specific tips
    render_theme_tips(selected)


def render_theme_tips(theme: str):
    """Show helpful tips for the selected theme."""
    st.divider()

    tips = {
        'minimal': "💡 Transparent background - great for overlays and modern designs",
        'scientific': "💡 High DPI (600) - perfect for papers and publications",
        'presentation': "💡 Dark background with vibrant colors - ideal for slides",
        'polar_minimal': "💡 Circular visualization - best with 30+ seconds of audio",
        'polar_scientific': "💡 Polar with full axes - technical and precise",
        'polar_grayscale': "💡 High contrast B&W - timeless and elegant design",
    }

    if theme in tips:
        st.caption(tips[theme])
