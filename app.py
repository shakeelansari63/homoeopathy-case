import flet as ft
from main_app.main import MainApp


def app(page: ft.Page):
    page.title = "Homoeopathy Case"

    # create application instance
    main_app = MainApp(width=1200, height=800)

    # add application's root control to the page
    page.add(main_app)

    page.update()


if __name__ == "__main__":
    ft.app(target=app)
