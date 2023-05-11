FROM python:3.11

RUN mkdir /FaceApp

WORKDIR /FaceApp

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN chmod a+x *.sh




