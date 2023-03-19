import flet as ft
from .base import BaseControl
from .menu_bar import MenuBar
from .tabs import Tabs


class MainApp(BaseControl):
    _column_items = []

    def build(self):
        self._column_items.append(MenuBar(width=self._width, height=20))
        self._column_items.append(Tabs(width=self._width, height=self._height - 20))

        return ft.Column(
            spacing=10,
            controls=self._column_items,
            expand=True,
            width=self._width,
            height=self._height,
        )
