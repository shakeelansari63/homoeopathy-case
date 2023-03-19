import flet as ft


class BaseControl(ft.UserControl):
    def __init__(
        self, width: ft.OptionalNumber, height: ft.OptionalNumber, *args, **kwargs
    ):
        self._height = height
        self._width = width

        super().__init__(*args, **kwargs)
