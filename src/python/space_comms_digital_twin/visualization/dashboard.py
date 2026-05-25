from __future__ import annotations

from typing import Any


class Dashboard:
    def __init__(self):
        self.widgets: dict[str, Any] = {}

    def add_widget(self, name: str, widget: Any):
        self.widgets[name] = widget

    def render(self) -> dict[str, Any]:
        return {"widgets": list(self.widgets.keys()), "status": "active"}
