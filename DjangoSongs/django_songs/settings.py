from pathlib import Path
import environ

# ─── Ruta base del proyecto ────────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent

# ─── Leer variables de entorno desde .env ──────────────────────────────────────
env = environ.Env()
environ.Env.read_env(BASE_DIR / '.env')

# ─── Seguridad ─────────────────────────────────────────────────────────────────
# SECRET_KEY firma cookies, sesiones y tokens CSRF. Nunca la expongas en producción.
SECRET_KEY = env('SECRET_KEY')

# DEBUG=True muestra errores detallados. Siempre False en producción.
DEBUG = env.bool('DEBUG')

ALLOWED_HOSTS = ['darmanProg22.pythonanywhere.com']  

# ─── Apps instaladas ───────────────────────────────────────────────────────────
INSTALLED_APPS = [
    'django.contrib.admin',
    'widget_tweaks',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'canciones',  # ← Nuestra aplicación principal
]

# ─── Middleware ────────────────────────────────────────────────────────────────
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'django_songs.urls'

# ─── Plantillas ────────────────────────────────────────────────────────────────
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # ← Django buscará plantillas aquí
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'django_songs.wsgi.application'

# ─── Base de datos (MySQL FASE 2) ──────────────────────────────────────────────
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': env('DB_NAME'),
        'USER': env('DB_USER'),
        'PASSWORD': env('DB_PASSWORD'),
        'HOST': env('DB_HOST'),
        'PORT': env('DB_PORT'),
    }
}

# ─── Validadores de contraseñas ────────────────────────────────────────────────
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ─── Spotify API (vía RapidAPI) ────────────────────────────────────────────────
RAPIDAPI_KEY = env('RAPIDAPI_KEY')

# ─── Internacionalización ──────────────────────────────────────────────────────
LANGUAGE_CODE = 'es-co'
TIME_ZONE = 'America/Bogota'
USE_I18N = True
USE_TZ = True

# ─── Archivos estáticos ────────────────────────────────────────────────────────
STATIC_URL = 'static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'