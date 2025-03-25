## notas de usuarios
- todo lo relacionado con usuarios y roles, se debera usar CustomUser del modulo usuarios, el cual extiende del modelo de usuarios por defecto de django

- usa postgresql como base de datos
- comando para iniciar proyecto:  python manage.py runserver

### variables de entorno a setear:
- SECRET_KEY
#### base de datos
- DB_NAME
- DB_USER
- DB_PASSWORD
- DB_HOST
- DB_PORT


ejemplo de post de crear buses y conductores:
```json
{
  "conductor": {
    "nombre": "Carlos Pérez",
    "numero_licencia": "LIC-7788",
    "dpi": "1234567890101",
    "expiracion_licencia": "2026-12-31"
  },
  "bus": {
    "numero_id": "B-88",
    "modelo": "Mercedes 2020",
    "ruta_asignada": "R-101"
  }
}
```
