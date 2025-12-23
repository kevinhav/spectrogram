"""Parameter grid system for batch spectrogram generation."""

from dataclasses import asdict
from itertools import product
from typing import Any

from modules.spectrogram_visualizer import SpectrogramConfig


class ParameterGrid:
    """Manages parameter grid generation for batch processing."""

    def __init__(
        self,
        parameter_dict: dict[str, list[Any]],
        base_config: SpectrogramConfig | None = None,
    ):
        """
        Initialize with parameter variations.

        Args:
            parameter_dict: Dictionary of parameters to vary.
                           Example: {'cmap': ['viridis', 'magma'], 'dpi': [150, 300]}
            base_config: Base SpectrogramConfig to start from (optional).
                        Parameters in parameter_dict will override base values.
        """
        self.parameter_dict = parameter_dict
        self.base_config = base_config

    def generate_combinations(self) -> list[dict[str, Any]]:
        """
        Generate all parameter combinations using itertools.product.

        Returns:
            List of parameter dictionaries, one per combination
        """
        # Start with base config if provided
        if self.base_config:
            base_params = asdict(self.base_config)
        else:
            base_params = {}

        # Get keys and values for grid parameters
        keys = list(self.parameter_dict.keys())
        values = list(self.parameter_dict.values())

        # Generate all combinations
        combinations = []
        for combo in product(*values):
            # Start with base parameters
            params = base_params.copy()

            # Override with current combination
            for key, value in zip(keys, combo):
                params[key] = value

            combinations.append(params)

        return combinations

    def count(self) -> int:
        """
        Return total number of combinations.

        Returns:
            Total number of parameter combinations
        """
        count = 1
        for values in self.parameter_dict.values():
            count *= len(values)
        return count


def create_filename(params: dict[str, Any]) -> str:
    """
    Generate descriptive filename from parameters.

    Args:
        params: Parameter dictionary

    Returns:
        Descriptive filename encoding key parameters

    Example:
        >>> params = {'cmap': 'magma', 'projection': 'polar', 'figsize': (11, 5), 'norm_gamma': 4, 'dpi': 300}
        >>> create_filename(params)
        'spectrogram_magma_polar_11x5_gamma4_dpi300.jpg'
    """
    # Extract key parameters for filename
    cmap = params.get("cmap", "default")
    projection = params.get("projection", "linear")
    figsize = params.get("figsize", (11, 5))
    gamma = params.get("norm_gamma", 4)
    dpi = params.get("dpi", 300)
    output_format = params.get("output_format", "jpg")

    # Optional parameters that may vary
    polar_inner = params.get("polar_inner_radius")
    nperseg = params.get("nperseg")
    max_freq = params.get("max_freq")
    title = params.get("title")
    title_font = params.get("title_font")

    # Format figsize as WxH
    figsize_str = f"{figsize[0]}x{figsize[1]}"

    # Build filename with base parameters
    filename = f"spectrogram_{cmap}_{projection}_{figsize_str}_gamma{gamma}_dpi{dpi}"

    # Add optional parameters if they differ from defaults
    if projection == "polar" and polar_inner is not None and polar_inner != 0.05:
        filename += f"_hole{polar_inner}"
    if nperseg is not None and nperseg != 256:
        filename += f"_seg{nperseg}"
    if max_freq is not None and max_freq != 18000:
        filename += f"_freq{max_freq}"
    if title_font is not None:
        # Clean font name for filename (remove spaces)
        font_clean = title_font.replace(" ", "")
        filename += f"_{font_clean}"
    if title is not None:
        # Clean title for filename (remove spaces, limit length)
        title_clean = title.replace(" ", "")[:20]
        filename += f"_{title_clean}"

    filename += f".{output_format}"

    return filename


# Example parameter grids for common use cases

EXAMPLE_MINIMAL_GRID = {
    "cmap": ["viridis", "magma", "inferno"],
    "projection": ["linear", "polar"],
}

EXAMPLE_FULL_GRID = {
    "projection": ["linear", "polar"],
    "cmap": ["viridis", "magma", "inferno", "plasma"],
    "figsize": [(11, 5), (12, 5)],
    "dpi": [150, 300, 600],
    "norm_gamma": [2, 4, 6],
    "background": ["transparent", "white", "black"],
    "title_size": [16, 20, 24],
}

EXAMPLE_COLORMAP_COMPARISON = {
    "cmap": [
        "viridis",
        "plasma",
        "inferno",
        "magma",
        "cividis",
        "twilight",
        "turbo",
        "gray",
        "gray_r",  # Reversed grayscale (like reference implementation)
    ],
}

EXAMPLE_DPI_COMPARISON = {
    "dpi": [72, 150, 300, 600],
}

EXAMPLE_GAMMA_COMPARISON = {
    "norm_gamma": [1, 2, 3, 4, 5, 6, 8, 10],
}
