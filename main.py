import flet as ft

def main(page: ft.Page):
    text = ft.Text("Hello World")

    page.controls.append(text)

    page.update()

if __name__ == "__main__":
    ft.app(target = main)