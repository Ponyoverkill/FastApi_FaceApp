import json
import os
from PIL import Image
import requests
import schemas
from datetime import datetime

'''
delete_image - takes image's path in static/img directory and delete current image

download_and_save_image - takes image's url, download it into static/img. Returning path to image

delete_trash - delete images from static/img by paths in static/trash/trashlist

draw - takes pydantic image model and color, draw borders by color in image.faces rectangles. Save it in static/trash
and return path to it

'''

def delete_image(image):
    os.remove(image)


def download_and_save_image(url: str):
    path = './static/img/' + datetime.utcnow().strftime("%d-%m-%Y_%H-%M-%S_%f") + '.jpeg'
    try:
        resp = requests.get(url, stream=True).raw
        new_image = Image.open(resp)
        new_image.save(path)
        return path
    except:
        return ValueError


def delete_trash():
    with open('./static/trash/trashlist.txt', 'r') as trash:
        items = trash.readlines()
        for i in items:
            os.remove(i)
    with open('./static/trash/trashlist.txt', 'w') as trash:
        trash.seek(0)
        trash.close()


def draw(image: schemas.Image, color: str):
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

