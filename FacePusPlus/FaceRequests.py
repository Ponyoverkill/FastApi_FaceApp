import aiohttp
from config import API_KEY, API_SECRET, FACE_URL

'''
Requests to FacePlusPlus API
tried being async(
Gets only image url
'''


PARAMS = {'api_key': API_KEY, 'api_secret': API_SECRET}

async def face_detect(image):
    if 'image_file' in PARAMS.keys():
        del PARAMS['image_file']
    async with aiohttp.ClientSession() as session:
        if image[0:4] == "http":
            PARAMS['image_url'] = image
            async with session.post(FACE_URL, params=PARAMS) as resp:
                r = await resp.json()
        if 'faces' in r:
            return r['faces']
        else:
            return False