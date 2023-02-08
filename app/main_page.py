import flet as ft


def MainPage(page: ft.Page):
    row = ft.Row(controls=[], alignment=ft.MainAxisAlignment.CENTER)
    col = ft.Column(controls=[], alignment=ft.MainAxisAlignment.SPACE_AROUND)

    text = ft.Text("Hello There")

    col.controls.append(text)
    row.controls.append(col)

    page.add(row)

    page.update()
