#!/bin/sh

CONDA_ENV_NAME=points-env

echo "Esperando a la base de datos..."
sleep 5 

echo "Aplicando migraciones..."
conda run -n $CONDA_ENV_NAME python manage.py migrate --no-input

echo "Ejecutando seeder para crear datos de prueba..."
conda run -n $CONDA_ENV_NAME python manage.py seed_users

echo "Recolectando archivos estáticos..."
conda run -n $CONDA_ENV_NAME python manage.py collectstatic --no-input

echo "Iniciando servidor Gunicorn..."
conda run -n $CONDA_ENV_NAME gunicorn pointsapp.wsgi:application --bind 0.0.0.0:8000