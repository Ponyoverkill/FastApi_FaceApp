# FastApi_FaceApp
For post image you can use file, image base64 encoded or image URL
If you will post more than 1 image in 1 request:
The priority is: 1) file 2) base64 3)URL

Before run:
Register on https://console.faceplusplus.com/login
take secret key and api key.
paste them into .env in the same fields
from /FacePusPlus->

docker compose build
docker compose up

try it on port 1234
