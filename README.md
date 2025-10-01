# Blog de Reseñas de Películas y Anime

Un blog desarrollado en Django para compartir reseñas de películas y anime con sistema de comentarios, reacciones y suscripciones.

## 🚀 Despliegue en Railway

### Archivos de configuración incluidos:

- `Procfile` - Comando de inicio para Railway
- `requirements.txt` - Dependencias de Python con versiones específicas
- `railway.json` - Configuración específica de Railway
- `runtime.txt` - Versión de Python
- `.gitignore` - Archivos a ignorar en Git

### Variables de entorno necesarias en Railway:

1. **SECRET_KEY** - Clave secreta de Django (generar una nueva para producción)
2. **DEBUG** - `False` para producción
3. **ALLOWED_HOSTS** - Tu dominio de Railway (ej: `tu-app.railway.app`)
4. **BASE_URL** - URL completa de tu app (ej: `https://tu-app.railway.app`)
5. **DATABASE_URL** - Railway la proporciona automáticamente

### Pasos para desplegar:

1. **Subir código a GitHub**
2. **Conectar Railway con tu repositorio**
3. **Agregar servicio PostgreSQL** en Railway
4. **Configurar variables de entorno**
5. **Desplegar**

### Comandos que se ejecutan automáticamente:

- `python manage.py migrate` - Migrar base de datos
- `python manage.py collectstatic` - Recopilar archivos estáticos
- `gunicorn myblog.wsgi` - Iniciar servidor web

## 🛠️ Desarrollo Local

```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar migraciones
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser

# Ejecutar servidor
python manage.py runserver
```

## 📋 Características

- ✅ Sistema de reseñas con calificaciones
- ✅ Comentarios con votos
- ✅ Reacciones a posts
- ✅ Sistema de suscripciones (RSS)
- ✅ Notificaciones por menciones
- ✅ Búsqueda avanzada
- ✅ Categorías y subcategorías
- ✅ Panel de administración
- ✅ Diseño responsive

## 🔧 Tecnologías

- **Backend:** Django 5.2.6
- **Frontend:** HTML, CSS, JavaScript, Bootstrap
- **Base de datos:** SQLite (desarrollo) / PostgreSQL (producción)
- **Servidor:** Gunicorn
- **Archivos estáticos:** WhiteNoise
- **Hosting:** Railway
