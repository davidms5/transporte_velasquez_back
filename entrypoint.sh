#!/bin/bash
set -e

# Ejecutar migraciones
echo "Aplicando migraciones..."
python manage.py migrate --noinput

# Recolectar archivos estáticos
echo "Recolectando archivos estáticos..."
python manage.py collectstatic --noinput

# Iniciar el servidor
echo "Iniciando el servidor..."
exec gunicorn inventario_buses.wsgi:application --bind 0.0.0.0:8000
