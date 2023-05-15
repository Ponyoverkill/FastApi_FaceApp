import io
import json
import os
import re
from base64 import b64decode as dec64
from PIL import Image
import requests
import schemas
from datetime import datetime

'''
delete_image - takes image's path in static/img directory and delete current image

save_image - takes image's file, base64 and url, and trying to save/decode&save/download&save into ./static/img
Returning path to image

delete_trash - delete images from static/img by paths in static/trash/trashlist

draw - takes pydantic image model and color, draw borders by color in image.faces rectangles. Save it in static/trash
and return path to it

'''


def generate_path():
    return './static/img/' + datetime.utcnow().strftime("%d-%m-%Y_%H-%M-%S_%f") + '.jpeg'


def delete_image(image):
    os.remove(image)


def base64_save_image(image: str):
    path = generate_path()
    image = dec64(re.sub('^data:image/.+;base64,', '', image))
    new_image = Image.open(io.BytesIO(image))
    new_image.save(path)
    return path


def file_save_image(image):
    path = generate_path()
    print(image)
    new_image = Image.open(image)
    new_image.save(path)
    return path


def url_save_image(url: str):
    path = generate_path()
    try:
        resp = requests.get(url, stream=True).raw
        new_image = Image.open(resp)
        new_image.save(path)
        return path
    except:
        return ConnectionError


def save_image(image_file, image_base64, image_url):
    if image_file:
        path = file_save_image(image_file.file)
    elif image_base64:
        path = base64_save_image(image_base64)
    elif image_url:
        path = url_save_image(image_url)
    return path


def delete_trash():
    with open('./static/trash/trashlist.txt', 'r') as trash:
        items = trash.readlines()
        for i in items:
            os.remove(i)
    with open('./static/trash/trashlist.txt', 'w') as trash:
        trash.seek(0)
        trash.close()


def draw(image: schemas.Image, color: str):
    delete_trash()
    new_image = Image.open(image.img)
    for i in json.loads(image.faces):
        width = i['face_rectangle']['width']
        height = i['face_rectangle']['height']
        top = i['face_rectangle']['top']
        left = i['face_rectangle']['left']
        artTop = Image.new('RGBA', (width, 2), color)
        artBot = Image.new('RGBA', (width, 2), color)
        artLeft = Image.new('RGBA', (2, height), color)
        artRight = Image.new('RGBA', (2, height), color)
        new_image.paste(artTop, (left, top))
        new_image.paste(artBot, (left, top+height))
        new_image.paste(artLeft, (left, top))
        new_image.paste(artRight, (left+width, top))
    path = './static/trash/' + image.img[13:]
    new_image.save(path)
    with open('./static/trash/trashlist.txt', 'w') as file:
        file.write(path)
        file.close()
    image.img = path
    return image

