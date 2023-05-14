import aiohttp
import contextlib as cl


async def download_image(url: str, filepath: str) -> bool:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:

            if resp.status != 200:
                return False

            with cl.suppress(Exception), open(filepath, 'wb') as fh:
                content = await resp.content.read()
                fh.write(content)
                return True

    return False
