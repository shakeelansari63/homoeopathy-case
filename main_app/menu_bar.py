import flet as ft
from .base import BaseControl


class MenuBar(BaseControl):
    _menu_row_items = []

    def build(self):
        self._menu_row_items.append(ft.Text("This is Menubar"))
        self._menu_row_items.append(ft.Text("This is another item in Menubar"))

        return ft.Row(
            controls=self._menu_row_items,
            height=self._height,
            width=self._width,
            expand=True,
        )
