FROM python:3.10
COPY . /home
WORKDIR /home
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y
RUN pip install -r requirements.txt
EXPOSE 5000
CMD python app.py