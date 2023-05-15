import aiohttp
from config import API_KEY, API_SECRET, FACE_URL

'''
Requests to FacePlusPlus API
tried being async(
if face_detect takes file, base64 and url, priority is file/base64/url
'''

PARAMS = {'api_key': API_KEY, 'api_secret': API_SECRET}


async def face_detect_base64(image):
    async with aiohttp.ClientSession() as session:
        async with session.post(FACE_URL, data={'image_base64': image}, params=PARAMS) as resp:
            r = await resp.json()
    return r



async def face_detect_file(image):
    async with aiohttp.ClientSession() as session:
        async with session.post(FACE_URL, data={'image_file': await image.read()}, params=PARAMS) as resp:
            r = await resp.json()
    return r



async def face_detect_url(image):
    async with aiohttp.ClientSession() as session:
        async with session.post(FACE_URL, data={'image_url': image}, params=PARAMS) as resp:
            r = await resp.json()
    return r



async def face_detect(image_file, image_base64, image_url):
    if image_file:
        try:
            r = await face_detect_file(image_file)
            r['type'] = 'file'
            return r
        except:
            raise ConnectionError
    elif image_base64:
        try:
            r = await face_detect_base64(image_base64)
            r['type'] = 'base64'
            return r
        except:
            raise ConnectionError
    elif image_url:
        try:
            r = await face_detect_url(image_url)
            r['type'] = 'url'
            return r
        except:
            raise ConnectionError
    else:
        raise ValueError



