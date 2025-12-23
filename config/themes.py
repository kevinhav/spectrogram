"""Preconfigured themes for spectrogram visualization."""

from dataclasses import replace

from modules.spectrogram_visualizer import SpectrogramConfig


def minimal(**overrides) -> SpectrogramConfig:
    """Minimal theme with optional parameter overrides.

    Small font title below, transparent background, minimal axes.
    Works well for both linear and polar projections.

    Args:
        **overrides: Any SpectrogramConfig parameter to override

    Returns:
        SpectrogramConfig with minimal theme settings
    """
    base = SpectrogramConfig(
        projection="linear",
        cmap="magma",
        figsize=(11, 5),
        dpi=300,
        background="transparent",
        title="Spectrogram",
        title_font="Helvetica",
        title_weight="normal",
        title_size=10,
        title_color="#000004",
        title_position="bottom",
        show_axes="minimal",
        nperseg=2048,  # Higher resolution STFT
        noverlap=1900,  # High overlap for smoothness
        norm_gamma=4.0,
        max_freq=8000,  # 8kHz for better detail (especially for polar)
        polar_inner_radius=0.05,  # Small inner hole for polar
        normalize_db=True,  # Normalize for consistent appearance
        time_tick_interval=15,
        axes_color="#CCCCCC",
        tick_color="#CCCCCC",
        tick_size=8,
        output_format="jpg",
        quality=95,
    )
    return replace(base, **overrides)


def scientific(**overrides) -> SpectrogramConfig:
    """Scientific theme with optional parameter overrides.

    Full axes, white background, high contrast for publications.

    Args:
        **overrides: Any SpectrogramConfig parameter to override

    Returns:
        SpectrogramConfig with scientific theme settings
    """
    base = SpectrogramConfig(
        projection="linear",
        cmap="viridis",
        figsize=(12, 6),
        dpi=600,
        background="white",
        title="Spectrogram",
        title_font="DejaVu Sans",
        title_weight="bold",
        title_size=18,
        title_color="#000000",
        show_axes="full",
        norm_gamma=3.0,
        max_freq=20000,
        time_tick_interval=10,
        axes_color="#333333",
        tick_color="#333333",
        tick_size=10,
        output_format="png",
        quality=95,
    )
    return replace(base, **overrides)


def presentation(**overrides) -> SpectrogramConfig:
    """Presentation theme with optional parameter overrides.

    Dark background, vibrant colors, large text for slides.

    Args:
        **overrides: Any SpectrogramConfig parameter to override

    Returns:
        SpectrogramConfig with presentation theme settings
    """
    base = SpectrogramConfig(
        projection="linear",
        cmap="plasma",
        figsize=(14, 7),
        dpi=150,
        background="black",
        title="Audio Spectrogram",
        title_font="Helvetica",
        title_weight="bold",
        title_size=28,
        title_color="#FFFFFF",
        show_axes="minimal",
        norm_gamma=5.0,
        max_freq=18000,
        time_tick_interval=20,
        axes_color="#FFFFFF",
        tick_color="#FFFFFF",
        tick_size=14,
        output_format="png",
        quality=90,
    )
    return replace(base, **overrides)


def polar_minimal(**overrides) -> SpectrogramConfig:
    """Polar minimal theme with optional parameter overrides.

    Polar version of minimal theme with improved settings.

    Args:
        **overrides: Any SpectrogramConfig parameter to override

    Returns:
        SpectrogramConfig with polar minimal theme settings
    """
    base = SpectrogramConfig(
        projection="polar",
        cmap="magma",
        figsize=(10, 10),  # Square for polar
        dpi=300,
        background="transparent",
        title="Spectrogram (Polar)",
        title_font="Helvetica",
        title_weight="bold",
        title_size=20,
        title_color="#000004",
        show_axes="minimal",
        nperseg=2048,  # Higher resolution
        noverlap=1900,  # High overlap for smoothness
        norm_gamma=4.0,
        max_freq=8000,  # 8kHz for better detail
        polar_inner_radius=0.05,  # Small inner hole
        normalize_db=True,  # Normalize for consistent appearance
        time_tick_interval=15,
        axes_color="#CCCCCC",
        tick_color="#CCCCCC",
        tick_size=8,
        output_format="jpg",
        quality=95,
    )
    return replace(base, **overrides)


def polar_scientific(**overrides) -> SpectrogramConfig:
    """Polar scientific theme with optional parameter overrides.

    Polar version of scientific theme.

    Args:
        **overrides: Any SpectrogramConfig parameter to override

    Returns:
        SpectrogramConfig with polar scientific theme settings
    """
    base = SpectrogramConfig(
        projection="polar",
        cmap="viridis",
        figsize=(10, 10),
        dpi=600,
        background="white",
        title="Frequency-Time Analysis (Polar)",
        title_font="DejaVu Sans",
        title_weight="bold",
        title_size=18,
        title_color="#000000",
        show_axes="full",
        norm_gamma=3.0,
        max_freq=20000,
        time_tick_interval=10,
        axes_color="#333333",
        tick_color="#333333",
        tick_size=10,
        output_format="png",
        quality=95,
    )
    return replace(base, **overrides)


def polar_grayscale(**overrides) -> SpectrogramConfig:
    """Polar grayscale theme with optional parameter overrides.

    High-resolution grayscale polar spectrogram (reference implementation).

    Args:
        **overrides: Any SpectrogramConfig parameter to override

    Returns:
        SpectrogramConfig with polar grayscale theme settings
    """
    base = SpectrogramConfig(
        projection="polar",
        cmap="gray_r",  # Reversed grayscale (black = low, white = high)
        figsize=(12, 12),  # Square for polar
        dpi=300,
        background="white",
        title="",  # No title for clean look
        title_font="Helvetica",
        title_weight="normal",
        title_size=16,
        title_color="#000000",
        show_axes="none",  # Clean, no axes
        nperseg=2048,  # High resolution STFT
        noverlap=1900,  # Very high overlap for smooth result
        max_freq=10000,  # Limit to 10kHz for detail
        polar_inner_radius=0.3,  # Inner hole at 30% radius
        normalize_db=True,  # Normalize dB to 0-1 range
        norm_gamma=1.0,  # No power normalization (already normalized)
        output_format="png",
        quality=95,
    )
    return replace(base, **overrides)
