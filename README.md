# TaskFlow API

**API REST para gestión de tareas, proyectos y equipos con autenticación JWT**

[![Django](https://img.shields.io/badge/Django-6.0-green.svg)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://www.python.org/)
[![DRF](https://img.shields.io/badge/DRF-3.16-red.svg)](https://www.django-rest-framework.org/)
[![Coverage](https://img.shields.io/badge/Coverage-93%25-brightgreen.svg)]()
[![Docker](https://img.shields.io/badge/Docker-ready-blue.svg)](https://www.docker.com/)

🔗 **[Demo en vivo](https://taskapi-30ij.onrender.com)**

---

## 🎯 ¿Qué es TaskFlow API?

API REST backend para gestión colaborativa de tareas y proyectos con sistema de equipos, permisos granulares y autenticación JWT.

**Ideal para:** Frontends (React, Vue, Angular), apps móviles (iOS, Android), integraciones con otros sistemas.

---

## ⚡ Características principales

**Autenticación:**
- Sistema completo de registro, login y logout
- Autenticación JWT con access token y refresh token
- Expiración automática y rotación de tokens
- Logout real con blacklist de tokens
- Gestión de perfiles de usuario

**Gestión de equipos y proyectos:**
- CRUD completo de equipos, proyectos, tareas y comentarios
- Sistema de roles (Admin, Jefe de equipo, Miembro)
- Control de permisos estricto (usuarios solo ven sus datos)

**Endpoints personalizados:**
- Completar tareas con un solo request
- Filtrar tareas pendientes
- Estadísticas avanzadas con ORM (aggregate, annotate, Case/When)
- Optimización de queries (select_related, prefetch_related)

**Documentación:**
- Swagger UI interactivo (drf-spectacular)
- Ejemplos de requests/responses

**Testing:**
- 30 tests unitarios e integración
- 93% de cobertura de código
- Tests de autenticación JWT, permisos, validaciones y modelos

**Docker:**
- Contenedores para Django y PostgreSQL
- Configuración lista para desarrollo con docker-compose

---

## 🛠️ Stack tecnológico

- **Backend:** Python 3.12 | Django 6.0 | Django REST Framework 3.16
- **Base de datos:** SQLite (desarrollo) | PostgreSQL (producción)
- **Autenticación:** JWT (djangorestframework-simplejwt)
- **Documentación:** drf-spectacular (Swagger/OpenAPI)
- **Testing:** Django TestCase + APITestCase | Coverage 93%
- **Contenedores:** Docker + Docker Compose
- **Deployment:** Render

---

## 📦 Instalación local

### Opción A — Con Docker (recomendado)

#### Requisitos previos
- Docker Desktop instalado y corriendo

```bash
# Clonar repositorio
git clone https://github.com/MauRyze22/taskApi.git
cd taskApi

# Configurar variables de entorno
cp .env.example .env
# Edita .env con tus valores

# Levantar contenedores
docker-compose up --build

# En otra terminal — correr migraciones
docker-compose exec web python manage.py migrate

# Crear superusuario
docker-compose exec web python manage.py createsuperuser

# Recolectar archivos estáticos
docker-compose exec web python manage.py collectstatic --noinput
```

Abre http://localhost:8000

---

### Opción B — Sin Docker

#### Requisitos previos
- Python 3.12+
- pip
- Git

```bash
# Clonar repositorio
git clone https://github.com/MauRyze22/taskApi.git
cd taskApi

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
cp .env.example .env
# Edita .env con tu SECRET_KEY

# Migraciones
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser

# Ejecutar servidor
python manage.py runserver
```

Abre http://127.0.0.1:8000

---

## 🔐 Autenticación JWT

Esta API usa **JSON Web Tokens (JWT)**. El flujo es:

1. Registrarse o hacer login → recibís **access token** + **refresh token**
2. Usás el **access token** en cada request (expira en 30 min)
3. Cuando expira, usás el **refresh token** para obtener uno nuevo
4. Para logout, invalidás el refresh token con blacklist

### Registro
```http
POST /api/accounts/register/
Content-Type: application/json

{
  "username": "usuario",
  "email": "usuario@example.com",
  "password": "Password123!",
  "password2": "Password123!",
  "first_name": "Nombre",
  "last_name": "Apellido"
}
```

**Respuesta:**
```json
{
  "user": "usuario",
  "message": "Usuario registrado exitosamente"
}
```

### Login
```http
POST /api/token/
Content-Type: application/json

{
  "username": "usuario",
  "password": "Password123!"
}
```

**Respuesta:**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

### Uso del access token
```http
GET /api-tasks/tasks/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

### Refrescar token
```http
POST /api/token/refresh/
Content-Type: application/json

{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

### Logout
```http
POST /api/token/blacklist/
Content-Type: application/json

{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

---

## 📚 Endpoints principales

| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| POST | `/api/accounts/register/` | Registrar usuario | ❌ |
| POST | `/api/token/` | Login (obtener tokens) | ❌ |
| POST | `/api/token/refresh/` | Refrescar access token | ❌ |
| POST | `/api/token/blacklist/` | Logout (invalidar token) | ✅ |
| GET | `/api/accounts/profile/` | Ver perfil | ✅ |
| PUT | `/api/accounts/profile/` | Actualizar perfil | ✅ |
| GET | `/api-tasks/teams/` | Listar equipos | ✅ |
| POST | `/api-tasks/teams/` | Crear equipo | ✅ |
| GET | `/api-tasks/projects/` | Listar proyectos | ✅ |
| POST | `/api-tasks/projects/` | Crear proyecto | ✅ |
| GET | `/api-tasks/tasks/` | Listar tareas | ✅ |
| POST | `/api-tasks/tasks/` | Crear tarea | ✅ |
| POST | `/api-tasks/tasks/{id}/completar/` | Completar tarea | ✅ |
| GET | `/api-tasks/tasks/pendientes/` | Ver tareas pendientes | ✅ |
| GET | `/api-tasks/tasks/details/` | Estadísticas avanzadas | ✅ |
| GET | `/api-tasks/comments/` | Listar comentarios | ✅ |
| POST | `/api-tasks/comments/` | Crear comentario | ✅ |

**Documentación completa:** http://localhost:8000/swagger/

---

## 📂 Estructura del proyecto

```
taskApi/
├── taskApi/              # Configuración Django
│   ├── settings.py       # Configuración con variables de entorno
│   ├── urls.py
│   └── wsgi.py
├── tasks/                # App principal
│   ├── models.py         # Team, Project, Task, Comment
│   ├── serializers.py    # Serializers optimizados
│   ├── views.py          # ViewSets con permisos
│   ├── tests.py          # 30 tests — 93% coverage
│   └── urls.py
├── accounts/             # Autenticación y perfiles
│   ├── models.py         # Profile
│   ├── serializers.py    # Register
│   ├── views.py          # Register, Profile views
│   └── urls.py
├── Dockerfile            # Imagen Docker
├── docker-compose.yml    # Orquestación de contenedores
├── .dockerignore         # Archivos excluidos de Docker
├── requirements.txt      # Dependencias
├── Procfile              # Config para deployment
├── .env.example          # Plantilla de variables
└── README.md
```

---

## 🧪 Testing

```bash
# Correr todos los tests
python manage.py test

# Ver cobertura de código
coverage run --source='.' manage.py test
coverage report

# Ver reporte visual
coverage html
```

**Cobertura actual: 93%** — incluye tests de:
- Autenticación JWT (obtener token, credenciales incorrectas, refresh, blacklist)
- Endpoints CRUD (crear, listar, editar, eliminar)
- Permisos (usuario no puede editar datos de otro)
- Validaciones (campos requeridos, datos incorrectos)
- Métodos de modelos (`esta_vencida`, `dias_para_vencer`, `__str__`)
- Estadísticas avanzadas

---

## 🐳 Docker

```bash
# Levantar el proyecto
docker-compose up --build

# Detener contenedores
docker-compose down

# Ejecutar comandos dentro del contenedor
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py test
```

**Servicios:**
- `web` — Django + Gunicorn en puerto 8000
- `db` — PostgreSQL 16 con datos persistentes

---

## 🔒 Seguridad

- Autenticación JWT obligatoria en todos los endpoints (excepto register/login)
- Access token con expiración de 30 minutos
- Refresh token con expiración de 1 día
- Blacklist de tokens para logout real
- Control de permisos granular (usuarios solo ven sus datos)
- CSRF protection en producción
- Variables de entorno para secretos

---

## 🚀 Deployment

### Variables de entorno necesarias:

```
SECRET_KEY=tu-secret-key-segura
DEBUG=False
ALLOWED_HOSTS=.onrender.com,tu-dominio.com
DATABASE_URL=postgresql://...
CSRF_TRUSTED_ORIGINS=https://tu-app.onrender.com
```

---

## 🤝 Sobre este proyecto

Proyecto de portfolio personal para demostrar habilidades en:

✓ Django REST Framework y arquitectura de APIs
✓ Autenticación JWT con simplejwt
✓ Serializers optimizados y datos anidados
✓ Control de permisos granular
✓ Optimización de queries (N+1 problem)
✓ ORM avanzado (aggregate, annotate, F expressions, Case/When)
✓ Testing con 93% de cobertura
✓ Docker y docker-compose
✓ Deployment en producción con Render

**Feedback y sugerencias son bienvenidos** → [Abrir issue](https://github.com/MauRyze22/taskApi/issues)

---

## 📬 Contacto

**Amaury Monteagudo** — Backend Developer

Especializado en Python, Django, APIs REST y bases de datos.

📧 amaurymonteagudop22@gmail.com
🔗 [GitHub](https://github.com/MauRyze22) | [LinkedIn](https://www.linkedin.com/in/amaury-monteagudo-40375b3a5)

---

## 📄 Licencia

[MIT License](LICENSE) — Uso libre con atribución.

---

⭐ **Si este proyecto te fue útil, considera darle una estrella — ¡gracias!**