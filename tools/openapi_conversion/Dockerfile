FROM python:3.8-alpine

ADD ./requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt
RUN rm -rf __pycache__
ADD . /app
WORKDIR /app

ENTRYPOINT ["python", "convert_openapi_to_implicitdict.py"]
