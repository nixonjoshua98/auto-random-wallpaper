import asyncio
import os.path
import random

from src.configuration import read_configuration
from src.unsplash_client import UnsplashClient
from src import http_utility, wallpaper_utility

config = read_configuration()

client = UnsplashClient(config.unsplash_api)


async def main():

    while True:

        # 10% either way jitter
        await asyncio.sleep(config.update_delay * random.uniform(0.9, 1.1))

        # Fetch a landscape photo using a random query
        resp = await client.get_random_photo(
            orientation="landscape",
            query=random.choice(config.unsplash_api.querys))

        if resp is None:
            continue

        # Assume its a jpg..can we find the photo format?
        file_path = os.path.join(config.photo_directory, f"{resp.id}.jpg")

        # Download and save the image - Returns whether it was successful
        has_saved = await http_utility.download_image(resp.urls.regular, file_path)

        if not has_saved:
            continue

        wallpaper_utility.set_wallpaper(file_path)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()

    loop.run_until_complete(main())
