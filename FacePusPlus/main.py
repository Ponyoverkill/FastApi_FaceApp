from fastapi import FastAPI, UploadFile
from fastapi.responses import FileResponse
from crud import create_img, get_img, update_img, delete_img
from ImageFunc import draw, save_image
from FaceRequests import face_detect

'''
post_image - takes image's file, base64 or url, use it in Face Api and put result to db
get_image - takes id, color, returning image with borded faces by color
put_image - takes id, image's file, base64 or url, use it in Face Api and update current image from db
delete_image - takes id, obviously deleting image from db
'''

app = FastAPI()


@app.post("/image")
async def post_image(image_url: str = None, image_base64: str = None, image_file: UploadFile = None):
        try:
            res = await face_detect(image_file, image_base64, image_url)
            if 'faces' in res:
                print(res)
                path = save_image(image_file, image_base64, image_url)
                id = create_img(path, res['faces'])
                return id
            else:
                return res
        except ValueError:
            return {'status': 'error',
                    'data': 'none',
                    'details': 'No images posted'}
        except ConnectionError:
            return {'status': 'error',
                    'data': 'none',
                    'details': 'Failed connection to face service or database'}




@app.get("/image/{id}")
def get_image(id, color: str = ''):
    colors = {'red', 'blue', 'green'}
    if color in colors:
        try:
            image = get_img(id)
            new_image = draw(image, color)
            return FileResponse(new_image.img, media_type="image/jpg")
        except ValueError:
            return 'Seem\'s like wrong id!'
        except:
            return 'Unknown error'
    return 'Wrong color! only str red/green/blue'


@app.put("/image/{id}")
async def put_image(id: int, image_url: str = None, image_base64: str = None, image_file: UploadFile = None):
        try:
            res = await face_detect(image_file, image_base64, image_url)
            if 'faces' in res:
                print(res)
                image = get_img(id)
                image.img = save_image(image_file, image_base64, image_url)
                image.faces = res['faces']
                update_img(image)
                return 'succes update image id=' + str(image.id)
            else:
                return res
        except ValueError:
            return {'status': 'error',
                    'data': 'none',
                    'details': 'No images to put'}
        except ConnectionError:
            return {'status': 'error',
                    'data': 'none',
                    'details': 'Failed connection to face service or database'}


@app.delete("/image/{id}")
def delete_image(id):
    try:
        delete_img(id)
        return f'image with id={id} successfully deleted!!!'
    except ValueError:
        return 'Wrong id!'
    except:
        return 'Something goes wrong)'



















