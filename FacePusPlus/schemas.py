from pydantic import BaseModel


class ImageBase(BaseModel):
    img: str | bytes
    faces: str
    pass


class Image(ImageBase):
    id: int

    class Config:
        orm_mode = True
