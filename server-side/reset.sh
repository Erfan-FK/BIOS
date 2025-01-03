#!/bin/bash

echo "Stopping and removing all containers..."
docker compose down --volumes --remove-orphans

echo "Deleting migrations..."
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc" -delete

echo "Building images and containers..."
docker compose build

echo "Applying migrations..."
sudo docker compose run --rm app sh -c  "python manage.py makemigrations"
docker compose run --rm app sh -c "python manage.py migrate"

echo "Starting the app..."
docker compose up
