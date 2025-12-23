"""Results gallery component - displays generated spectrograms with download options."""

import streamlit as st
from io import BytesIO
import zipfile


def render():
    """Render the results gallery."""
    if not st.session_state.generated_images:
        st.info("💡 No spectrograms generated yet. Configure settings in the sidebar and click Generate!")
        return

    st.markdown("### 📊 Generated Spectrograms")
    st.caption(f"Total: {len(st.session_state.generated_images)} spectrogram(s)")

    # Download all button (if multiple)
    if len(st.session_state.generated_images) > 1:
        zip_bytes = create_zip_file(st.session_state.generated_images)
        st.download_button(
            label="📥 Download All as ZIP",
            data=zip_bytes,
            file_name="spectrograms.zip",
            mime="application/zip",
            use_container_width=True,
        )
        st.divider()

    # Display each generated spectrogram
    for idx, result in enumerate(st.session_state.generated_images):
        render_result_card(idx, result)

    # Clear all button
    if st.button("🗑️ Clear All Results", use_container_width=True):
        st.session_state.generated_images = []
        st.rerun()


def render_result_card(idx: int, result: dict):
    """Render a single result card."""
    st.markdown(f"#### Spectrogram {idx + 1}")

    col1, col2 = st.columns([3, 1])

    with col1:
        # Display image
        st.image(result['image'], use_container_width=True)

    with col2:
        # Filename
        st.caption(f"**{result['filename']}**")

        # Download button
        st.download_button(
            label="📥 Download",
            data=result['image'],
            file_name=result['filename'],
            mime=f"image/{result['config'].output_format}",
            key=f"download_{idx}",
            use_container_width=True,
        )

        # Show config details
        with st.expander("⚙️ Details"):
            st.json({
                'theme': getattr(result['config'], '_theme_name', 'custom'),
                'projection': result['config'].projection,
                'dpi': result['config'].dpi,
                'cmap': result['config'].cmap,
                'title': result['config'].title,
                'title_position': result['config'].title_position,
                'output_format': result['config'].output_format,
            })

    st.divider()


def create_zip_file(results: list) -> bytes:
    """Create a ZIP file containing all generated spectrograms."""
    zip_buffer = BytesIO()

    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for result in results:
            zip_file.writestr(result['filename'], result['image'])

    zip_buffer.seek(0)
    return zip_buffer.getvalue()
