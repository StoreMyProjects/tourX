FROM python:3.9-slim-buster

WORKDIR /project

COPY . /project

RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["python", "app.py"]