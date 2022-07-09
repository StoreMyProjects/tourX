FROM python:3.9-slim-buster

WORKDIR /project

ENV FLASK_RUN_HOST=0.0.0.0

COPY . /project

RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["python", "app.py"]