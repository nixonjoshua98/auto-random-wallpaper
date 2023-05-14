import ctypes


def set_wallpaper(file_path: str):
    ctypes.windll.user32.SystemParametersInfoW(20, 0, file_path, 0)
