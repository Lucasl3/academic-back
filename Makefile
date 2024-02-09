db:
	docker compose up -d db

run:
	python3 manage.py runserver localhost:8000

down:
	docker compose down

migrate:
	python3 manage.py migrate

data:
	python3 manage.py loaddata data.json

makemigrations:
	python3 manage.py makemigrations
