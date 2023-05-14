from pydantic import BaseModel


class UnsplashAPIConfigurationSection(BaseModel):
    access_key: str
    querys: list[str]


class Configuration(BaseModel):
    unsplash_api: UnsplashAPIConfigurationSection
    update_delay: int
    photo_directory: str


def read_configuration(file_name: str = "config.json") -> Configuration:

    with open(file_name, "r") as fh:
        data = fh.read()

    return Configuration.parse_raw(data)
