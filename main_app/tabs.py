import flet as ft
from .base import BaseControl


class Tabs(BaseControl):
    _tab_items = []

    def build(self):
        self._tab_items.append(
            ft.Tab(
                text="This is First Tab",
                content=ft.Text("This is tab content"),
            )
        )

        self._tab_items.append(
            ft.Tab(
                text="This is Second Tab",
                content=ft.Text("This is also tab content"),
            )
        )

        return ft.Tabs(
            selected_index=0,
            animation_duration=300,
            tabs=self._tab_items,
            expand=1,
            height=self._height,
            width=self._width,
        )
