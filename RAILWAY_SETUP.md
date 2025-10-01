# Railway Configuration Guide

## Variables de entorno necesarias en Railway:

### OBLIGATORIAS:
- SECRET_KEY: Tu clave secreta de Django (genera una nueva)
- DEBUG: False (para producción)
- ALLOWED_HOSTS: tu-dominio.railway.app
- BASE_URL: https://tu-dominio.railway.app

### AUTOMÁTICAS (Railway las proporciona):
- DATABASE_URL: PostgreSQL connection string
- PORT: Puerto del servidor
- RAILWAY_STATIC_URL: URL para archivos estáticos

## Comandos de build (Railway los ejecuta automáticamente):

```bash
# Instalar dependencias
pip install -r requirements.txt

# Recopilar archivos estáticos
python manage.py collectstatic --noinput

# Ejecutar migraciones
python manage.py migrate
```

## Estructura de archivos para Railway:

```
blog1/
├── requirements.txt    ✅ Lista de dependencias
├── Procfile           ✅ Comando de inicio
├── runtime.txt        ✅ Versión de Python
├── railway.json       ✅ Configuración específica
├── manage.py          ✅ Script de Django
├── myblog/            ✅ Configuración del proyecto
└── blog/              ✅ App principal
```

## Pasos para desplegar:

1. Subir código a GitHub
2. Conectar Railway con GitHub
3. Configurar variables de entorno
4. Agregar base de datos PostgreSQL
5. Desplegar automáticamente

¡Tu blog estará listo en minutos! 🚀
