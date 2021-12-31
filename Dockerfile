FROM python:3.8
WORKDIR /app
COPY . /app/
RUN pip3 install -r requirements.txt
RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y
EXPOSE 5000
ENTRYPOINT [ “python3” ]
CMD [ “app.py” ]
#CMD flask run