import json

import aiohttp
from typing import Optional
from src.configuration import UnsplashAPIConfigurationSection
from src.unsplash_random_photo_response import UnsplashRandomPhotoResponse
import contextlib as cl


def _set_when_trueish(d: dict, key: str, value):
    if value:
        d[key] = value


class UnsplashClient:
    def __init__(self, config: UnsplashAPIConfigurationSection):
        self._config = config
        self._base_url = "https://api.unsplash.com"
        self._topic_lookup: dict[str, str] = {}

    @property
    def default_headers(self) -> dict:
        return {
            "Authorization": f"Client-ID {self._config.access_key}"
        }

    async def get_cached_topics(self):
        if not self._topic_lookup:
            topics = await self._get_topic_dict()

            if topics:
                self._topic_lookup = topics

        return self._topic_lookup

    async def _get_topic_dict(self) -> dict[str, str]:
        async with aiohttp.ClientSession(headers=self.default_headers) as session:
            async with session.get(f"{self._base_url}/topics") as r:
                json_body = await r.json()

                return {ele["title"]: ele["id"] for ele in json_body}

    async def _get_topic_ids(self, topic_names: Optional[list[str]]) -> list[str]:

        if topic_names is None:
            return []

        topics = await self.get_cached_topics()

        return [topic_id for name in topic_names if (topic_id := topics.get(name))]

    async def get_random_photo(
            self,
            orientation=None,
            query: Optional[str] = None,
            topic_names: list[str] = None) -> Optional[UnsplashRandomPhotoResponse]:

        params = {}

        topic_ids = await self._get_topic_ids(topic_names)

        _set_when_trueish(params, "orientation", orientation)
        _set_when_trueish(params, "topics", ",".join(topic_ids))
        _set_when_trueish(params, "query", query)

        async with aiohttp.ClientSession(headers=self.default_headers) as session:
            async with session.get(f"{self._base_url}/photos/random", params=params) as r:
                json_body = await r.json()

                with cl.suppress(Exception):
                    return UnsplashRandomPhotoResponse.parse_obj(json_body)

        return None

