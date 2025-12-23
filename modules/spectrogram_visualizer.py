"""Spectrogram visualization with linear and polar projections."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import PowerNorm
from scipy.signal import spectrogram

if TYPE_CHECKING:
    from matplotlib.axes import Axes
    from matplotlib.figure import Figure


@dataclass
class SpectrogramConfig:
    """Configuration for spectrogram visualization."""

    # Core parameters
    projection: str = "linear"  # "linear" or "polar"
    cmap: str = "magma"
    figsize: tuple[float, float] = (11, 5)
    dpi: int = 300

    # Processing parameters
    norm_gamma: float = 4.0
    max_freq: int | None = 18000
    nperseg: int = 256  # STFT window size
    noverlap: int = 128  # STFT overlap
    polar_inner_radius: float = 0.05  # Inner hole radius for polar plots (0.0 - 1.0)
    normalize_db: bool = False  # Normalize dB values to 0-1 range

    # Styling parameters
    background: str = "transparent"  # "transparent", "white", "black", or hex color
    title: str = "Spectrogram"
    title_font: str = "Helvetica"
    title_size: int = 20
    title_color: str = "#000004"
    title_weight: str = "bold"  # "normal", "bold", etc.
    title_position: str = "top"  # "top" or "bottom"

    # Axes parameters
    time_tick_interval: int = 15  # seconds
    show_axes: str = "minimal"  # "minimal", "full", "none"
    axes_color: str = "#CCCCCC"
    tick_color: str = "#CCCCCC"
    tick_size: int = 8

    # Output parameters
    output_format: str = "jpg"  # "jpg", "png", "svg"
    quality: int = 95  # For JPG (1-100)


class SpectrogramGenerator:
    """Generate spectrograms with linear or polar projection."""

    def __init__(self, config: SpectrogramConfig):
        """
        Initialize with configuration.

        Args:
            config: SpectrogramConfig object with all visualization settings
        """
        self.config = config

    def generate(
        self, audio_data: np.ndarray, sample_rate: int, output_path: str
    ) -> None:
        """
        Generate and save spectrogram.

        Args:
            audio_data: Mono audio signal (numpy array)
            sample_rate: Sample rate in Hz
            output_path: Where to save the output image
        """
        # Create spectrogram based on projection type
        if self.config.projection == "linear":
            fig, ax = self._create_linear_spectrogram(audio_data, sample_rate)
        elif self.config.projection == "polar":
            fig, ax = self._create_polar_spectrogram(audio_data, sample_rate)
        else:
            raise ValueError(
                f"Invalid projection: {self.config.projection}. Must be 'linear' or 'polar'."
            )

        # Apply styling
        duration = len(audio_data) / sample_rate
        self._apply_styling(fig, ax, duration)

        # Save figure
        self._save_figure(fig, output_path)

        # Clean up
        plt.close(fig)

    def _create_linear_spectrogram(
        self, audio_data: np.ndarray, sample_rate: int
    ) -> tuple[Figure, Axes]:
        """
        Create traditional linear spectrogram using ax.specgram().

        Args:
            audio_data: Mono audio signal
            sample_rate: Sample rate in Hz

        Returns:
            (fig, ax) tuple
        """
        # Determine background color
        facecolor = (
            "none"
            if self.config.background == "transparent"
            else self.config.background
        )

        # Create figure
        fig = plt.figure(
            figsize=self.config.figsize, dpi=self.config.dpi, facecolor=facecolor
        )

        # Create main axis with top margin for title
        ax = fig.add_axes((0, 0, 1, 0.9))

        # Create spectrogram
        Pxx, freqs, bins, im = ax.specgram(
            audio_data,
            Fs=sample_rate,
            cmap=self.config.cmap,
            norm=PowerNorm(gamma=self.config.norm_gamma),
            NFFT=self.config.nperseg,
            noverlap=self.config.noverlap,
        )

        # Limit frequency range if requested
        if self.config.max_freq is not None:
            ax.set_ylim(0, self.config.max_freq)

        return fig, ax

    def _create_polar_spectrogram(
        self, audio_data: np.ndarray, sample_rate: int
    ) -> tuple[Figure, Axes]:
        """
        Create polar spectrogram using scipy STFT + pcolormesh on polar axes.

        Args:
            audio_data: Mono audio signal
            sample_rate: Sample rate in Hz

        Returns:
            (fig, ax) tuple
        """
        # Compute STFT with configured parameters
        f, t, Sxx = spectrogram(
            audio_data,
            fs=sample_rate,
            nperseg=self.config.nperseg,
            noverlap=self.config.noverlap,
        )

        # Convert to dB scale
        Sxx_db = 10 * np.log10(Sxx + 1e-10)  # Add epsilon to avoid log(0)

        # Normalize dB values to 0-1 range if requested
        if self.config.normalize_db:
            Sxx_norm = (Sxx_db - Sxx_db.min()) / (Sxx_db.max() - Sxx_db.min())
        else:
            Sxx_norm = Sxx_db

        # Limit frequency range if requested
        if self.config.max_freq is not None:
            freq_mask = f <= self.config.max_freq
            f = f[freq_mask]
            Sxx_norm = Sxx_norm[freq_mask, :]

        # Create polar mesh grid
        # theta: time dimension mapped to full circle (0 to 2π)
        # r: frequency dimension mapped to radius with inner hole
        theta = np.linspace(0, 2 * np.pi, Sxx_norm.shape[1] + 1)
        r = np.linspace(
            self.config.polar_inner_radius, 1.0, Sxx_norm.shape[0] + 1
        )  # Inner hole at polar_inner_radius
        Theta, R = np.meshgrid(theta, r)

        # Determine background color
        facecolor = (
            "none"
            if self.config.background == "transparent"
            else self.config.background
        )

        # Create figure with polar projection
        fig = plt.figure(
            figsize=self.config.figsize, dpi=self.config.dpi, facecolor=facecolor
        )
        # Use add_axes for precise positioning (like linear projection)
        # This prevents matplotlib from adding automatic margins that shift the visual center
        ax = fig.add_axes((0.1, 0.1, 0.8, 0.8), projection="polar")

        # Create polar mesh with appropriate normalization
        if self.config.normalize_db:
            # For normalized data, don't use PowerNorm (data already 0-1)
            ax.pcolormesh(
                Theta,
                R,
                Sxx_norm,
                cmap=self.config.cmap,
                shading="flat",
                vmin=0,
                vmax=1,
            )
        else:
            # For non-normalized data, use PowerNorm
            ax.pcolormesh(
                Theta,
                R,
                Sxx_norm,
                cmap=self.config.cmap,
                norm=PowerNorm(gamma=self.config.norm_gamma),
                shading="flat",
            )

        # Set radial limits to show the full range
        ax.set_ylim(0, 1)

        return fig, ax

    def _apply_styling(self, fig: Figure, ax: Axes, duration: float) -> None:
        """
        Apply consistent styling based on configuration.

        Args:
            fig: Matplotlib figure
            ax: Matplotlib axes
            duration: Audio duration in seconds
        """
        if self.config.projection == "linear":
            self._style_linear_axes(ax, duration)
        elif self.config.projection == "polar":
            self._style_polar_axes(ax, duration)

        # Add title (works for both projections) - only if title is not empty
        if self.config.title:
            if self.config.title_position == "top":
                y_pos = 0.98
                va = "top"
            else:  # bottom
                y_pos = 0.02
                va = "bottom"

            # Center horizontally (add_axes positioning ensures proper centering)
            x_pos = 0.5

            fig.text(
                x_pos,
                y_pos,
                self.config.title,
                fontname=self.config.title_font,
                fontweight=self.config.title_weight,
                fontsize=self.config.title_size,
                color=self.config.title_color,
                verticalalignment=va,
                horizontalalignment="center",
            )

    def _style_linear_axes(self, ax: Axes, duration: float) -> None:
        """
        Apply styling for linear spectrogram axes.

        Args:
            ax: Matplotlib axes
            duration: Audio duration in seconds
        """
        if self.config.show_axes == "minimal":
            # Minimal axes: only bottom spine with time labels
            ax.spines["bottom"].set_visible(True)
            ax.spines["bottom"].set_color(self.config.axes_color)
            ax.spines["bottom"].set_linewidth(0.5)
            ax.spines["top"].set_visible(False)
            ax.spines["left"].set_visible(False)
            ax.spines["right"].set_visible(False)

            # Offset the bottom spine
            ax.spines["bottom"].set_position(("outward", 5))

            # Set time ticks
            tick_positions = np.arange(0, duration, self.config.time_tick_interval)
            tick_labels = [f"{int(t // 60)}:{int(t % 60):02d}" for t in tick_positions]

            ax.set_xticks(tick_positions)
            ax.set_xticklabels(tick_labels)
            ax.spines["bottom"].set_bounds(tick_positions[0], tick_positions[-1])

            # Style ticks
            ax.tick_params(
                axis="x",
                colors=self.config.tick_color,
                labelsize=self.config.tick_size,
                length=3,
                width=0.5,
                pad=2,
            )
            ax.tick_params(
                axis="y", which="both", left=False, right=False, labelleft=False
            )

        elif self.config.show_axes == "full":
            # Full axes with all spines and labels
            for spine in ax.spines.values():
                spine.set_visible(True)
                spine.set_color(self.config.axes_color)

            ax.tick_params(
                colors=self.config.tick_color, labelsize=self.config.tick_size
            )

        elif self.config.show_axes == "none":
            # No axes
            for spine in ax.spines.values():
                spine.set_visible(False)
            ax.tick_params(
                axis="both",
                which="both",
                left=False,
                right=False,
                top=False,
                bottom=False,
                labelleft=False,
                labelbottom=False,
            )

    def _style_polar_axes(self, ax: Axes, duration: float) -> None:
        """
        Apply styling for polar spectrogram axes.

        Args:
            ax: Matplotlib polar axes
            duration: Audio duration in seconds
        """
        if self.config.show_axes == "minimal":
            # Minimal polar styling - clean, no grid, no outline
            ax.set_xticklabels([])  # Remove angular labels
            ax.set_yticklabels([])  # Remove radial labels
            ax.grid(False)  # Remove grid lines
            ax.spines["polar"].set_visible(False)  # Remove outline

        elif self.config.show_axes == "full":
            # Full polar styling with time labels
            time_positions = np.arange(0, duration, self.config.time_tick_interval)
            theta_positions = time_positions / duration * 2 * np.pi
            labels = [f"{int(t // 60)}:{int(t % 60):02d}" for t in time_positions]

            ax.set_xticks(theta_positions)
            ax.set_xticklabels(
                labels, color=self.config.tick_color, fontsize=self.config.tick_size
            )
            ax.tick_params(colors=self.config.tick_color)
            ax.grid(color=self.config.axes_color, linewidth=0.5)
            ax.spines["polar"].set_visible(True)  # Keep outline for full mode

        elif self.config.show_axes == "none":
            # No axes
            ax.set_xticklabels([])
            ax.set_yticklabels([])
            ax.grid(False)
            ax.spines["polar"].set_visible(False)  # Remove outline

    def _save_figure(self, fig: Figure, output_path: str) -> None:
        """
        Save figure with proper formatting.

        Args:
            fig: Matplotlib figure
            output_path: Where to save the output image
        """
        # Ensure output directory exists
        output_path_obj = Path(output_path)
        output_path_obj.parent.mkdir(parents=True, exist_ok=True)

        # Determine transparency
        transparent = self.config.background == "transparent"

        # Save based on format
        if self.config.output_format.lower() == "jpg":
            plt.savefig(
                output_path_obj,
                transparent=transparent,
                format="jpg",
                bbox_inches="tight",
                pad_inches=0.5,
                pil_kwargs={"quality": self.config.quality},
            )
        elif self.config.output_format.lower() == "png":
            plt.savefig(
                output_path_obj,
                transparent=transparent,
                format="png",
                bbox_inches="tight",
                pad_inches=0.5,
            )
        elif self.config.output_format.lower() == "svg":
            plt.savefig(
                output_path_obj,
                transparent=transparent,
                format="svg",
                bbox_inches="tight",
                pad_inches=0.5,
            )
        else:
            raise ValueError(
                f"Invalid output format: {self.config.output_format}. Must be 'jpg', 'png', or 'svg'."
            )
