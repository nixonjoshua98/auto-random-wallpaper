from pydantic import BaseModel


class UnsplashPhotoUrls(BaseModel):
    raw: str
    full: str
    regular: str


class UnsplashRandomPhotoResponse(BaseModel):
    id: str
    urls: UnsplashPhotoUrls
