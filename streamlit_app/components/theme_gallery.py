"""Theme gallery component - displays preview images of all available themes."""

import streamlit as st
from pathlib import Path


def render():
    """Render the theme gallery with preview images."""
    st.markdown("### 🎨 Theme Gallery")
    st.caption("Preview what each theme looks like - select one in the sidebar to customize")

    # Theme information
    themes = {
        'minimal': {
            'name': 'Minimal',
            'description': 'Clean, transparent background with subtle axes. Perfect for modern designs.',
            'type': 'Linear',
        },
        'scientific': {
            'name': 'Scientific',
            'description': 'White background, full axes, high contrast. Publication-ready.',
            'type': 'Linear',
        },
        'presentation': {
            'name': 'Presentation',
            'description': 'Dark background, vibrant colors, large text. Great for slides.',
            'type': 'Linear',
        },
        'polar_minimal': {
            'name': 'Polar Minimal',
            'description': 'Circular visualization with minimal styling. Eye-catching and unique.',
            'type': 'Polar',
        },
        'polar_scientific': {
            'name': 'Polar Scientific',
            'description': 'Circular with full axes and labels. Technical and precise.',
            'type': 'Polar',
        },
        'polar_grayscale': {
            'name': 'Polar Grayscale',
            'description': 'High-contrast black & white circular design. Timeless and elegant.',
            'type': 'Polar',
        },
    }

    # Create 2x3 grid
    cols = st.columns(3)

    theme_ids = list(themes.keys())
    for idx, theme_id in enumerate(theme_ids):
        theme = themes[theme_id]
        col_idx = idx % 3

        with cols[col_idx]:
            # Try to load preview image
            preview_path = Path(f"streamlit_app/assets/theme_previews/{theme_id}.jpg")
            if not preview_path.exists():
                preview_path = Path(f"streamlit_app/assets/theme_previews/{theme_id}.png")

            if preview_path.exists():
                st.image(str(preview_path), use_container_width=True)
            else:
                # Placeholder if preview doesn't exist
                st.info(f"Preview for {theme['name']} will be generated")

            # Theme name and type badge
            col_name, col_badge = st.columns([2, 1])
            with col_name:
                st.markdown(f"**{theme['name']}**")
            with col_badge:
                badge_color = "🟦" if theme['type'] == 'Linear' else "🟣"
                st.caption(f"{badge_color} {theme['type']}")

            # Description
            st.caption(theme['description'])

            # Select button
            if st.button(f"Select", key=f"select_{theme_id}", use_container_width=True):
                st.session_state.selected_theme = theme_id
                st.success(f"✅ Selected: {theme['name']}")
                st.rerun()
