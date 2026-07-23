# 🎵 Django Songs

Catálogo musical personal construido con **Django 6.0**, como parte de la *Fase 2 — Django* del Roadmap Arquitecto de Software.

---

## 📋 Requisitos

- Python 3.12+
- pip / venv
- Opcional: MySQL 8.0+ (solo para despliegue en PythonAnywhere)

## 🚀 Instalación (local — SQLite)

```bash
# 1. Clonar el repositorio
git clone <repo-url>
cd DjangoSongs

# 2. Crear y activar entorno virtual
python -m venv venv
.\venv\Scripts\activate   # Windows
source venv/bin/activate  # Linux/Mac

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar variables de entorno
#    Copiar .env.example a .env y editar SECRET_KEY y RAPIDAPI_KEY
copy .env.example .env     # Windows
cp .env.example .env       # Linux/Mac

# 5. Ejecutar migraciones (crea db.sqlite3 automáticamente)
python manage.py migrate

# 6. Iniciar servidor de desarrollo
python manage.py runserver
```

## ⚙️ Configuración

Las variables de entorno se definen en `.env` (local) o en las Environment Variables del web tab de PythonAnywhere:

| Variable       | Requerido | Descripción                                          |
|----------------|-----------|------------------------------------------------------|
| `DEBUG`        | Sí        | `True` para desarrollo / `False` en producción       |
| `SECRET_KEY`   | Sí        | Clave secreta de Django                              |
| `RAPIDAPI_KEY` | Sí        | API Key de RapidAPI para el endpoint Spotify23        |
| `DATABASE_URL` | No*       | Solo en PythonAnywhere — conexión MySQL (`mysql://user:pass@host/db`) |

> \* Si `DATABASE_URL` no está definida, el proyecto usa **SQLite** (`db.sqlite3`) automáticamente.
>
> **⚠️ Importante:** `.env` contiene credenciales sensibles y está excluido del repositorio via `.gitignore`.

### PythonAnywhere

1. En el Web tab, añadir estas variables en la sección **"Environment variables"**:
   - `DATABASE_URL` — conexión MySQL (ej: `mysql://usuario:pass@host/mydb$django_songs`)
   - `SECRET_KEY`, `DEBUG=False`, `RAPIDAPI_KEY`
2. Asegurarse de que el **WSGI file** apunte a `django_songs.settings`
3. Activar el virtualenv y ejecutar `python manage.py migrate` desde una Bash console

## 🏗️ Estructura del proyecto

```
DjangoSongs/
├── django_songs/              # Configuración del proyecto
│   ├── settings.py            # Settings (DB condicional, rate limit, etc.)
│   ├── urls.py                # Rutas raíz
│   ├── wsgi.py / asgi.py      # Entry points de producción
│   └── __init__.py            # pymysql.install_as_MySQLdb()
├── canciones/                 # App principal
│   ├── models.py              # Modelo Cancion
│   ├── views.py               # Vistas + rate limiting en Spotify
│   ├── urls.py                # Rutas de la app
│   ├── forms.py               # Formulario ModelForm
│   ├── admin.py               # Configuración del admin
│   ├── tests.py               # Pruebas unitarias
│   ├── apps.py                # Configuración de la app
│   ├── utils.py               # Utilidades (extraer_youtube_id)
│   ├── services/
│   │   ├── song_service.py    # Lógica de negocio (CRUD local)
│   │   └── spotify_client.py  # Cliente de la API de Spotify (RapidAPI)
│   └── migrations/            # Migraciones de base de datos
├── templates/                 # Plantillas HTML
│   ├── base.html              # Layout base (Cyberpunk dark)
│   └── canciones/
│       ├── lista.html         # Listado con modal YouTube
│       ├── crear.html         # Formulario de creación
│       ├── form_cancion.html  # Formulario de edición
│       ├── song_search.html   # Búsqueda en Spotify
│       └── song_detail.html   # Detalle con reproductor embebido
├── manage.py                  # CLI de Django
├── .env                       # Variables de entorno (no se sube)
├── .env.example               # Template de variables de entorno
└── .gitignore
```

## 🧠 Modelo de datos

**`Cancion`**

| Campo           | Tipo           | Descripción                              |
|-----------------|----------------|------------------------------------------|
| `titulo`        | CharField(150) | Título de la canción                     |
| `artista`       | CharField(100) | Artista/banda                            |
| `album`         | CharField(100) | Álbum (opcional, default `"Single"`)     |
| `duracion`      | DurationField  | Duración en formato `HH:MM:SS`           |
| `youtube_url`   | URLField       | URL de YouTube (opcional)                |
| `fecha_creacion`| DateTimeField  | Fecha de alta (automática)               |

**Propiedades del modelo**:
| Propiedad             | Descripción                                       |
|-----------------------|---------------------------------------------------|
| `youtube_embed_url`   | URL de embed `youtube-nocookie.com/embed/VIDEO_ID`|
| `youtube_video_id`    | ID del video extraído de la URL de YouTube        |

**Validación**: El método `clean()` del modelo rechaza URLs que no sean de YouTube (`youtube.com/watch?v=`, `youtu.be/`, `youtube.com/embed/`).

## 🔗 Endpoints

| Ruta                              | Nombre              | Descripción                     |
|-----------------------------------|---------------------|---------------------------------|
| `GET /`                           | `canciones:index`   | Listado de canciones            |
| `GET /crear/`                     | `canciones:create`  | Formulario de nueva canción     |
| `POST /crear/`                    | —                   | Guardar nueva canción           |
| `GET /editar/<id>/`               | `canciones:editar_cancion` | Formulario de edición    |
| `POST /editar/<id>/`              | —                   | Guardar cambios                 |
| `POST /eliminar/<id>/`            | `canciones:delete`  | Eliminar canción                |
| `GET /admin/`                     | —                   | Panel de administración Django  |
| `GET /spotify/`                   | `canciones:spotify_search` | Búsqueda en Spotify       |
| `GET /spotify/<track_id>/`        | `canciones:spotify_detail` | Detalle y reproductor Spotify |

## ▶️ Integración con YouTube

Cada canción del catálogo puede tener una **URL de YouTube** opcional. Si está configurada, aparece un botón rojo de YouTube en la columna de acciones del listado.

**Modal reproductor**: Al hacer clic en el botón:
- Se abre un modal de Bootstrap (oscuro, consistente con el diseño Cyberpunk)
- **Pre-check vía oEmbed**: antes de cargar el iframe, se consulta `youtube.com/oembed` para verificar que el video existe y permite incrustación. Si falla, se muestra el fallback directo.
- Si oEmbed responde OK, se usa el `src` que YouTube devuelve en su HTML (incluye `feature=oembed`), solo reemplazando `www.youtube.com` → `www.youtube-nocookie.com` y agregando `autoplay=1&origin=...`.
- El iframe incluye todos los permisos necesarios (`accelerometer`, `autoplay`, `clipboard-write`, `encrypted-media`, `gyroscope`, `picture-in-picture`, `web-share`)
- **Detección runtime via postMessage**: un listener captura errores internos del player de YouTube (códigos 101/150/153). Si se detecta Error 153, se oculta el embed y se muestra el botón "Ver en YouTube".
- Si la red falla durante el pre-check, el sistema carga el iframe igual como defensa (puede funcionar).
- Al cerrar el modal, el `src` del iframe se vacía para detener el audio en segundo plano
- **`SECURE_REFERRER_POLICY = "strict-origin-when-cross-origin"`** en settings.py para que YouTube reciba el origin correcto

**URLs soportadas** (formato `utils.extraer_youtube_id()`):
- `https://www.youtube.com/watch?v=VIDEO_ID`
- `https://youtu.be/VIDEO_ID`
- `https://www.youtube.com/embed/VIDEO_ID`

## 🎵 Integración con Spotify API (vía RapidAPI)

El proyecto se integra con Spotify a través de **RapidAPI** usando el endpoint [`spotify23.p.rapidapi.com`](https://rapidapi.com/Glavier/api/spotify23), que actúa como proxy de la API oficial de Spotify.

**Autenticación**: API Key simple vía header `x-rapidapi-key` (no requiere OAuth ni refresh tokens).

**Manejo de errores**:
- Rate limit (HTTP 429) → mensaje amigable
- Timeout / fallo de conexión → mensaje de error en template

**Persistencia**: No se guardan datos de Spotify en la base de datos local. Las consultas se realizan en tiempo real contra la API.

### Cómo obtener la API Key

1. Ir a https://rapidapi.com/Glavier/api/spotify23
2. Crear una cuenta en RapidAPI o iniciar sesión
3. Suscribirse al plan **Basic** (gratuito, 100 requests/día)
4. Copiar la **API Key** que aparece en la sección "Code Snippets"
5. Pegarla en el `.env` como `RAPIDAPI_KEY=tu_key_aqui`

## 🎨 Frontend

- **Bootstrap 5.3.3** (tema oscuro)
- **Iconos**: Bootstrap Icons
- **Tipografía**: Bebas Neue + Space Grotesk (Google Fonts)
- **Estilo**: Cyberpunk / neon con acentos verdes (`#00e676`)
- **Fondo**: Cuadrícula tenue con glow radial superior

## 🧪 Pruebas

```bash
python manage.py test
```

## 🛠️ Tecnologías

- Python 3.12+
- Django 6.0
- SQLite (local) / MySQL 8.0 (PythonAnywhere)
- django-environ
- django-ratelimit (límite por IP en vistas Spotify)
- django-widget-tweaks
- PyMySQL (driver MySQL cross-platform)
- requests
- Bootstrap 5.3.3 + Bootstrap Icons
- RapidAPI (spotify23 — proxy Spotify)
- YouTube IFrame API + oEmbed pre-check + postMessage error detection

## 🚦 Rate Limiting

Las vistas que consumen la API de Spotify están protegidas con **django-ratelimit** (cache en memoria, sin Redis):

| Vista                      | Límite    | Cuando se excede                          |
|----------------------------|-----------|-------------------------------------------|
| `GET /spotify/`            | 10/min/IP | Mensaje "Demasiadas búsquedas" en la misma página |
| `GET /spotify/<id>/`       | 20/min/IP | Mensaje "Demasiadas solicitudes"          |
