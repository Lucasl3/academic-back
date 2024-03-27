# Use the "builder" stage to install dependencies and packages
FROM python:3.10

ENV PYTHONUNBUFFERED 1

WORKDIR /usr/app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

# criar pod init container para o migrations: https://atlasgo.io/guides/deploying/k8s-init-container
CMD python manage.py migrate && python manage.py runserver 0.0.0.0:8000
