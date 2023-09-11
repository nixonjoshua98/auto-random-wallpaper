from pydantic import BaseModel
from pathlib import Path


class UnsplashAPIConfigurationSection(BaseModel):
    access_key: str
    topics: list[str]


class Configuration(BaseModel):
    unsplash_api: UnsplashAPIConfigurationSection
    update_delay: int
    photo_directory: str


def read_configuration(file_path: Path) -> Configuration:

    with file_path.open("r") as fh:
        data = fh.read()

    return Configuration.parse_raw(data)
