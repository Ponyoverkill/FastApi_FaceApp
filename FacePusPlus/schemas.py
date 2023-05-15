from pydantic import BaseModel


class ImageBase(BaseModel):
    img: str
    faces: str


class Image(ImageBase):
    id: int

    class Config:
        orm_mode = True
