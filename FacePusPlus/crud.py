import json
from sqlalchemy.orm import sessionmaker
import database
import schemas
from ImageFunc import delete_image
from schemas import Image

'''
init_session - create session for db connection

create-img - takes image's path and dict faces. Create row in db. Returning id in json

update_img- takes id and pydantic imageBase instanсe. Update row in db with imageBase values. Delete previous image from
static/img and add new from imageBase instance

get_img - takes id, returning pydantic Image instanсe

delete_img - takes id, deleting row in db and image from static/img   

'''


def init_session():
    session = sessionmaker(bind=database.engine)
    s = session()
    return s


def create_img(path, faces: dict):
    try:
        db = init_session()
        db_image = database.Image(image=path, faces=json.dumps(faces))
        db.add(db_image)
        db.commit()
        db.refresh(db_image)
        id = {'id': db_image.id}
        return json.dumps(id)
    except:
        return ConnectionError


def update_img(image: schemas.Image):
    try:
        db = init_session()
        db_image = db.query(database.Image).filter_by(id=image.id).one()
        print(db_image.image, image.img)
        if db_image != []:
            delete_image(db_image.image)
            db_image.image = image.img
            db_image.faces = json.dumps(image.faces)
            db.add(db_image)
            db.commit()
        return 'Success update!'
    except:
        return ValueError


def get_img(id: int):
    try:
        db = init_session()
        db_image = db.query(database.Image).filter_by(id=id).one()
        j = json.dumps({'id': db_image.id, 'img': db_image.image, 'faces': db_image.faces})
        img = Image.parse_raw(j)
        return img
    except:
        raise ValueError


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


