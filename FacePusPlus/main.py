from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import ValidationError

import schemas
from crud import create_img, get_img, update_img, delete_img
from ImageFunc import draw, delete_trash
from FaceRequests import face_detect

'''
post_image - takes image's url, use it in Face Api and put result to db
get_image - takes id, color, returning image with borded faces by color
put_image - takes id, image's url, use it in Face Api and update current image from db
delete_image - takes id, obviously deleting image from db
'''

app = FastAPI()


@app.post("/image")
async def post_image(image):
    try:
        res = await face_detect(image)
        id = create_img(image, res)
        return id
    except ValidationError as e:
        return e.json()


@app.get("/image/{id}")
def get_image(id, color: str = ''):
    delete_trash()
    colors = {'red', 'blue', 'green'}
    if color in colors:
        try:
            image = get_img(id)
            new_image = draw(image, color)
            return FileResponse(new_image.img, media_type="image/jpg")
        except:
            return 'Seem\'s like wrong id!'
    return 'Wrong color! only str red/green/blue'


@app.put("/image/{id}")
async def put_image(id, image):
    try:
        res = await face_detect(image)
        new_image = schemas.ImageBase
        new_image.img = image
        new_image.faces = res
        update_img(id, new_image)
        return 'succes update image!'
    except:
        return 'Wrong id or image! image must be url!'



@app.delete("/image/{id}")
def delete_image(id):
    try:
        delete_img(id)
        return f'image with id={id} successfully deleted!!!'
    except:
        return 'Wrong id!'



















