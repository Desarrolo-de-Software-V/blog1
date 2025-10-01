# 🎬 Blog de Reseñas de Películas

Un blog moderno y funcional para reseñas de películas y anime, construido con Django.

## ✨ Características

- **📝 Sistema de reseñas** con calificaciones por estrellas
- **🏷️ Categorías y subcategorías** para organizar contenido
- **💬 Sistema de comentarios** con votos y respuestas
- **❤️ Reacciones** a las reseñas (me gusta, me encanta, etc.)
- **🔔 Sistema de notificaciones** y menciones
- **📡 Suscripciones RSS** por autor y categoría
- **🔍 Búsqueda avanzada** con filtros
- **👤 Sistema de usuarios** con perfiles personalizados
- **📱 Diseño responsivo** para móviles y escritorio

## 🚀 Despliegue en Railway

### Requisitos previos

1. **Cuenta en Railway**: Regístrate en [railway.app](https://railway.app)
2. **Cuenta en GitHub**: Para conectar tu repositorio
3. **Git instalado**: Para subir tu código

### Pasos para desplegar

#### 1. Preparar el repositorio

```bash
# Inicializar git si no lo has hecho
git init

# Agregar todos los archivos
git add .

# Hacer commit inicial
git commit -m "Initial commit - Blog de reseñas"

# Conectar con GitHub (crea el repositorio primero en GitHub)
git remote add origin https://github.com/tu-usuario/tu-repositorio.git
git branch -M main
git push -u origin main
```

#### 2. Configurar Railway

1. **Ve a [railway.app](https://railway.app)** y haz login
2. **Haz clic en "New Project"**
3. **Selecciona "Deploy from GitHub repo"**
4. **Conecta tu cuenta de GitHub** y selecciona el repositorio
5. **Railway detectará automáticamente** que es un proyecto Django

#### 3. Configurar variables de entorno

En el dashboard de Railway, ve a **Variables** y agrega:

```env
SECRET_KEY=tu-clave-secreta-super-segura-aqui
DEBUG=False
ALLOWED_HOSTS=tu-proyecto.railway.app
BASE_URL=https://tu-proyecto.railway.app
```

#### 4. Configurar base de datos

1. **En Railway, haz clic en "New"**
2. **Selecciona "Database" → "PostgreSQL"**
3. **Railway creará automáticamente** la variable `DATABASE_URL`
4. **Conecta la base de datos** a tu proyecto

#### 5. Ejecutar migraciones

En el dashboard de Railway:
1. **Ve a "Deployments"**
2. **Haz clic en los tres puntos** del deployment más reciente
3. **Selecciona "Open Console"**
4. **Ejecuta los comandos**:

```bash
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser
```

#### 6. ¡Listo! 🎉

Tu blog estará disponible en `https://tu-proyecto.railway.app`

## 🛠️ Desarrollo local

### Instalación

```bash
# Clonar el repositorio
git clone https://github.com/tu-usuario/tu-repositorio.git
cd tu-repositorio

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
cp env.example .env
# Edita .env con tus configuraciones

# Ejecutar migraciones
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser

# Ejecutar servidor
python manage.py runserver
```

### Estructura del proyecto

```
blog1/
├── blog/                    # App principal del blog
│   ├── models.py           # Modelos de datos
│   ├── views.py            # Vistas y lógica
│   ├── urls.py             # URLs del blog
│   ├── forms.py            # Formularios
│   ├── admin.py            # Panel de administración
│   └── templates/          # Plantillas HTML
├── myblog/                 # Configuración del proyecto
│   ├── settings.py         # Configuraciones
│   ├── urls.py             # URLs principales
│   └── wsgi.py             # WSGI para producción
├── static/                 # Archivos estáticos (CSS, JS)
├── media/                  # Archivos subidos por usuarios
├── requirements.txt        # Dependencias de Python
├── Procfile               # Configuración para Railway
├── runtime.txt            # Versión de Python
└── railway.json           # Configuración específica de Railway
```

## 📋 Características técnicas

- **Framework**: Django 5.2.6
- **Base de datos**: SQLite (desarrollo) / PostgreSQL (producción)
- **Servidor web**: Gunicorn
- **Archivos estáticos**: WhiteNoise
- **Configuración**: python-decouple
- **Imágenes**: Pillow para procesamiento

## 🔧 Comandos útiles

```bash
# Crear migraciones
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate

# Recopilar archivos estáticos
python manage.py collectstatic

# Crear superusuario
python manage.py createsuperuser

# Ejecutar servidor de desarrollo
python manage.py runserver

# Abrir shell de Django
python manage.py shell
```

## 📞 Soporte

Si tienes problemas con el despliegue o el desarrollo, puedes:

1. **Revisar los logs** en Railway Dashboard
2. **Verificar las variables de entorno**
3. **Comprobar que todas las migraciones** se ejecutaron
4. **Asegurarte de que el repositorio** esté actualizado

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

---

**¡Disfruta creando reseñas increíbles!** 🍿✨