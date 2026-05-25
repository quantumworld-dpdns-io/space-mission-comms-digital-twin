from __future__ import annotations

from typing import Any, Dict, List, Optional

import numpy as np


class OrbitPlotter:
    def plot_ground_track(self, lons: List[float], lats: List[float]):
        pass

    def plot_visibility(self, times: List[float], elevations: List[float]):
        pass


class LinkBudgetPlotter:
    def plot_snr_vs_distance(self, distances: List[float], snr_values: List[float]):
        pass

    def plot_margin_vs_frequency(self, frequencies: List[float], margins: List[float]):
        pass
