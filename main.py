import flet as ft
import os


def main(page: ft.Page) -> None:
    page.title = "Windows optimizer by @elsamueldev"
    page.window_height = 180
    page.window_width = 600
    page.window_full_screen = False
    page.padding = 20

    message = ft.SnackBar(content=ft.Text("You shouldn't be reading this!")) # to show info to the user
    page.add(message)
    # Functions for making my life easier (And a cleaner code I guess)
    def remove_files(path: str) -> None:
        try:
            files = os.listdir(path)
        except PermissionError:
            message.content = ft.Text("This program must be run as administrator to use that function")
            message.open = True
            message.update()
            return
        deleted = 0
        for f in files:
            try:
                os.remove(os.path.join(path, f))
                deleted += 1
            except PermissionError:
                print(f"\"{f}\" file not deleted, since it's being used by another process")

        message.content = ft.Text(f"{deleted} file/s deleted successfully!")
        message.open = True
        message.update()


    # Functions for buttons
    def remove_windows_temp(e: ft.ControlEvent) -> None:
        remove_files("C:\\Windows\\Temp")


    def remove_user_temp(e: ft.ControlEvent) -> None:
        user = os.getenv("USERNAME", "usuario")
        remove_files(f"C:\\Users\\{user}\\AppData\\Local\\Temp")


    def remove_prefetch(e: ft.ControlEvent) -> None:
        remove_files("C:\\Windows\\Prefetch")


    # Buttons to remove temporary files
    remove_temporary_files = ft.Row([
        ft.ElevatedButton(text="Remove Windows temp", on_click=remove_windows_temp),
        ft.ElevatedButton(text="Remove user temp", on_click=remove_user_temp),
        ft.ElevatedButton(text="Remove prefetch", on_click=remove_prefetch),
    ])
    page.add(remove_temporary_files)


if __name__ == "__main__":
    ft.app(target=main)