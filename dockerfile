# Utiliza una imagen oficial de Python como base
FROM python:3.12-slim-bookworm

# Establece el directorio de trabajo
WORKDIR /app

# Copia los archivos de requerimientos y los instala
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto de los archivos del proyecto
COPY . .

#RUN mkdir -p /app/staticfiles
# Collect static files
#RUN python manage.py collectstatic --noinput
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh
# Expone el puerto que Railway utilizará
EXPOSE 8000

# Comando para ejecutar la aplicación
#CMD ["gunicorn", "inventario_buses.wsgi:application", "--bind", "0.0.0.0:8000"]
CMD ["/app/entrypoint.sh"]
