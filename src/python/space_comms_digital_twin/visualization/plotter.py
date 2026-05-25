from __future__ import annotations


class OrbitPlotter:
    def plot_ground_track(self, lons: list[float], lats: list[float]):
        pass

    def plot_visibility(self, times: list[float], elevations: list[float]):
        pass


class LinkBudgetPlotter:
    def plot_snr_vs_distance(self, distances: list[float], snr_values: list[float]):
        pass

    def plot_margin_vs_frequency(self, frequencies: list[float], margins: list[float]):
        pass
