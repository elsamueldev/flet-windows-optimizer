import flet as ft
import os, winreg


def main(page: ft.Page) -> None:
    page.title = "Windows optimizer by Samuel"

    popup = ft.SnackBar(content=ft.Text(value="You shouldn't be reading this!")) # to show info to the user
    page.add(popup)
    text = ft.Text()
    
    def open_url(e):
        page.launch_url(e.data)
    # Functions for making my life easier (And a cleaner code I guess)
    def remove_files(path: str) -> None:
        try:
            files = os.listdir(path)
        except PermissionError:
            popup.content = ft.Text("This program must be run as administrator to use that function")
            popup.open = True
            page.update()
            return
        deleted = 0
        for f in files:
            try:
                os.remove(os.path.join(path, f))
                deleted += 1
            except PermissionError:
                print(f"\"{f}\" file not deleted, since it's being used by another process")

        popup.content = ft.Text(f"{deleted} file/s deleted successfully!")
        popup.open = True
        page.update()
    
    def disable_telemetry() -> None:
        key_path = r"SOFTWARE\Policies\Microsoft\Windows\DataCollection"
        key_name = "AllowTelemetry"
        key_value = 0

        try:
            # Open the registry key
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path, 0, winreg.KEY_SET_VALUE)

            # Set value
            winreg.SetValueEx(key, key_name, 0, winreg.REG_DWORD, key_value)
            winreg.CloseKey(key)

            popup.content = ft.Text(f"Success! Telemetry was disabled! (You should restart your PC)")

        except Exception as e:
            popup.content = ft.Text(f"Error: {e}")

        finally:
            popup.open = True
            page.update()

    # Env
    user = os.getenv("USERNAME", "usuario")

    # Paths
    WINDOWS_TEMP = "C:\\Windows\\Temp"
    USER_TEMP = f"C:\\Users\\{user}\\AppData\\Local\\Temp"
    PREFETCH = "C:\\Windows\\Prefetch"


    # Elements!
    very_cute_message = ft.AlertDialog(title=ft.Markdown(value="Made with ❤️ by [Samuel Jiménez](https://github.com/xsamueljr)", on_tap_link=open_url))
    def show_credits(e: ft.ControlEvent) -> None:
        very_cute_message.open = True
        page.update()

    appbar = ft.AppBar(title=ft.Text(value="Windows optimizer"), bgcolor="blue", actions=[ft.IconButton(icon=ft.icons.INFO, on_click=show_credits)])

    home_buttons = ft.Row([
        ft.ElevatedButton(text="Clean temporary files", on_click=lambda _: page.go("/clean")),
        ft.ElevatedButton(text="Register manipulations", on_click=lambda _: page.go("/register"))
    ], alignment=ft.MainAxisAlignment.CENTER)

    clean_buttons = ft.Row([
        ft.ElevatedButton(text="Windows temp", on_click=lambda _: remove_files(WINDOWS_TEMP)),
        ft.ElevatedButton(text="User temp", on_click=lambda _: remove_files(USER_TEMP)),
        ft.ElevatedButton(text="Prefetch", on_click=lambda _: remove_files(PREFETCH))
    ], alignment=ft.MainAxisAlignment.CENTER)

    register_buttons = ft.Row([
        ft.ElevatedButton(text="Disable telemetry", on_click=lambda _: disable_telemetry())
    ], alignment=ft.MainAxisAlignment.CENTER)

    # Go to the home section when the user press the escape key
    def on_keyboard(e: ft.KeyboardEvent) -> None:
        if e.key == "Escape" and page.route != "/":
            if very_cute_message.open:
                very_cute_message.open = False
                page.update()
            else:
                page.go("/")
    page.on_keyboard_event = on_keyboard

    # Functions to handle more than 1 view
    def route_change(e: ft.RouteChangeEvent) -> None:
        page.views.clear()

        # Home
        appbar.title.value = "Windows Optimizer"
        text.value = "Welcome!"
        page.views.append(
            ft.View(
                route="/",
                controls=[appbar, ft.Text(value="Welcome!", size=30), popup, home_buttons, very_cute_message],
                vertical_alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=26
                )
            )


        # Section for cleaning functions
        if page.route == "/clean":
            appbar.title.value = "Cleaning section"
            text.value = "Click on these buttons to clean your temp files of each directory"
            page.views.append(
                ft.View(
                    route="/clean",
                    controls=[appbar, text, popup, clean_buttons, very_cute_message],
                    vertical_alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                )
            )
            
        # Section for regedit
        if page.route == "/register":
            appbar.title.value = "Windows register manipulations"
            text.value = "Click on these buttons to manipulate Windows register right away!"
            page.views.append(
                ft.View(
                    route="/register",
                    controls=[appbar, text, popup, register_buttons, very_cute_message],
                    vertical_alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                )
            )
    
        page.update()
    
    def view_pop(e: ft.ViewPopEvent) -> None:
        page.views.pop()
        top_view: ft.View = page.views[-1]
        page.go(top_view.route)
    
    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)


if __name__ == "__main__":
    ft.app(target=main)