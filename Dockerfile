FROM debian:11

RUN apt update
RUN apt -fy install python3.9
RUN apt -fy install python3-pip

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt

RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y

COPY . /app

EXPOSE 8000

CMD ["python3.9", "manage.py", "runserver", "0.0.0.0:8000"]
