import json
from sqlalchemy.orm import sessionmaker
import database
import schemas
from ImageFunc import download_and_save_image, delete_image
from schemas import Image

'''
init_session - create session for db connection

create-img - takes image's url and dict faces. Create row in db. image value is path to static/img. Returning id in json

update_img- takes id and pydantic imageBase instanсe. Update row in db with imageBase values. Delete previous image from
static/img and add new from imageBase instance

get_img - takes id, returning pydantic Image instanсe

delete_img - takes id, deleting row in db and image from static/img   

'''


def init_session():
    session = sessionmaker(bind=database.engine)
    s = session()
    return s


def create_img(image, faces: dict):
    if faces:
        try:
            db = init_session()
            db_image = database.Image(image=download_and_save_image(image), faces=json.dumps(faces))
            db.add(db_image)
            db.commit()
            db.refresh(db_image)
            id = {'id': db_image.id}
            return json.dumps(id)
        except:
            return ValueError


def update_img(id: int, image: schemas.ImageBase):
    if image.faces:
        try:
            db = init_session()
            db_image = db.query(database.Image).filter_by(id=id).one()
            print(db_image.image, image.img)
            if db_image != []:
                delete_image(db_image.image)
                db_image.image = download_and_save_image(image.img)
                db_image.faces = json.dumps(image.faces)
                db.add(db_image)
                db.commit()
            return 'Success update!'
        except:
            return ValueError


def get_img(id:int):
    try:
        db = init_session()
        db_image = db.query(database.Image).filter_by(id=id).one()
        j = json.dumps({'id': db_image.id, 'img': db_image.image, 'faces': db_image.faces})
        img = Image.parse_raw(j)
        return img
    except:
        return False


def delete_img(id):
    try:
        db = init_session()
        db_image = db.query(database.Image).filter_by(id=id).one()
        if db_image != []:
            delete_image(db_image.image)
            db.delete(db_image)
            db.commit()
    except:
        return ValueError


