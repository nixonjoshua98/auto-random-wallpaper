import asyncio
import os.path
import random
import os
from pathlib import Path
import keyboard
import ctypes

from src.configuration import read_configuration
from src.unsplash_client import UnsplashClient
from src import http_utility

config = read_configuration(
    file_path=Path(__file__).with_name("config.json")
)

client = UnsplashClient(config.unsplash_api)


async def _process_unsplash() -> bool:

    # Fetch a landscape photo using a random query
    resp = await client.get_random_photo(
        orientation="landscape",
        query=random.choice(config.unsplash_api.querys))

    # Assume its a jpg..can we find the photo format?
    if not os.path.isfile(path := os.path.join(config.photo_directory, f"{resp.id}.jpg")):

        # Download and save the image - Returns whether it was successful
        has_saved = await http_utility.download_image(resp.urls.raw, path)

        if not has_saved:
            return False

    ctypes.windll.user32.SystemParametersInfoW(20, 0, path, 0)

    return True


def _update_with_existing_file() -> bool:
    files = os.listdir(config.photo_directory)

    if len(files) == 0:
        return False

    random_file = os.path.join( config.photo_directory, random.choice(files))

    ctypes.windll.user32.SystemParametersInfoW(20, 0, random_file, 0)

    return True


async def _update_wallpaper():
    if random.randint(0, 10) <= 4:  # 0..4
        await _process_unsplash()
    else:
        _update_with_existing_file()


async def main():

    while True:

        await _update_wallpaper()

        await asyncio.sleep(config.update_delay * random.uniform(0.9, 1.1))


if __name__ == "__main__":
    loop = asyncio.get_event_loop()

    keyboard.add_hotkey("ctrl+q", lambda: asyncio.run_coroutine_threadsafe(_update_wallpaper(), loop))

    loop.run_until_complete(main())
