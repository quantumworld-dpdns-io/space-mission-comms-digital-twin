from __future__ import annotations

from typing import Any, Dict


class Dashboard:
    def __init__(self):
        self.widgets: Dict[str, Any] = {}

    def add_widget(self, name: str, widget: Any):
        self.widgets[name] = widget

    def render(self) -> Dict[str, Any]:
        return {"widgets": list(self.widgets.keys()), "status": "active"}
