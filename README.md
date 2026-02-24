# TaskFlow API

**API REST para gestión de tareas, proyectos y equipos con autenticación por token**

[![Django](https://img.shields.io/badge/Django-6.0-green.svg)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![DRF](https://img.shields.io/badge/DRF-3.16-red.svg)](https://www.django-rest-framework.org/)

🔗 **[Demo en vivo](https://taskflow-api.onrender.com)** *(próximamente)*

---

## 🎯 ¿Qué es TaskFlow API?

API REST backend para gestión colaborativa de tareas y proyectos con sistema de equipos, permisos granulares y autenticación por token.

**Ideal para:** Frontends (React, Vue, Angular), apps móviles (iOS, Android), integraciones con otros sistemas.

---

## ⚡ Características principales

**Autenticación:**
- Sistema completo de registro, login y logout
- Autenticación por Token (Django REST Framework)
- Gestión de perfiles de usuario

**Gestión de equipos y proyectos:**
- CRUD completo de equipos, proyectos, tareas y comentarios
- Sistema de roles (Admin, Jefe de equipo, Miembro)
- Control de permisos estricto (usuarios solo ven sus datos)

**Endpoints personalizados:**
- Completar tareas con un solo request
- Filtrar tareas pendientes
- Optimización de queries (select_related, prefetch_related)

**Documentación:**
- Swagger UI interactivo (drf-yasg)
- Ejemplos de requests/responses

---

## 🛠️ Stack tecnológico

- **Backend:** Python 3.11+ | Django 6.0 | Django REST Framework 3.16
- **Base de datos:** SQLite (desarrollo) | PostgreSQL (producción)
- **Autenticación:** Token Authentication
- **Documentación:** drf-yasg (Swagger/OpenAPI)
- **Deployment:** Render

---

## 📦 Instalación local

### Requisitos previos
- Python 3.11+
- pip
- Git

### Setup

```bash
# Clonar repositorio
git clone https://github.com/MauRyze22/taskflow-api.git
cd taskflow-api

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

## 🔐 Autenticación

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
  "token": "abc123def456...",
  "message": "Usuario registrado exitosamente"
}
```

### Login
```http
POST /api/accounts/login/
Content-Type: application/json

{
  "username": "usuario",
  "password": "Password123!"
}
```

**Respuesta:**
```json
{
  "user": "usuario",
  "token": "abc123def456...",
  "message": "Inicio de sesión exitoso"
}
```

### Uso del token
```http
GET /api/tasks/tasks/
Authorization: Token abc123def456...
```

---

## 📚 Endpoints principales

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/accounts/register/` | Registrar usuario |
| POST | `/accounts/login/` | Iniciar sesión |
| POST | `/accounts/logout/` | Cerrar sesión |
| GET | `/accounts/profile/` | Ver perfil |
| GET | `/api-tasks/teams/` | Listar equipos |
| POST | `/api-tasks/teams/` | Crear equipo |
| GET | `/api-tasks/projects/` | Listar proyectos |
| POST | `/api-tasks/projects/` | Crear proyecto |
| GET | `/api-tasks/tasks/` | Listar tareas |
| POST | `/api-tasks/tasks/` | Crear tarea |
| POST | `/api-tasks/tasks/{id}/completar/` | Completar tarea |
| GET | `/api-tasks/tasks/pendientes/` | Ver tareas pendientes |
| GET | `/api-tasks/comments/` | Listar comentarios |
| POST | `/api-tasks/comments/` | Crear comentario |

**Documentación completa:** http://localhost:8000/swagger/

---

## 📂 Estructura del proyecto

```
taskflow-api/
├── taskApi/              # Configuración Django
│   ├── settings.py       # Configuración con variables de entorno
│   ├── urls.py
│   └── wsgi.py
├── tasks/                # App principal
│   ├── models.py         # Team, Project, Task, Comment
│   ├── serializers.py    # Serializers optimizados
│   ├── views.py          # ViewSets con permisos
│   └── urls.py
├── accounts/             # Autenticación
│   ├── models.py         # Profile
│   ├── serializers.py    # Register, Login
│   ├── views.py          # Auth views
│   └── urls.py
├── requirements.txt      # Dependencias
├── Procfile             # Config para deployment
├── .env.example         # Plantilla de variables
└── README.md
```

---

## 🔒 Seguridad

- Autenticación obligatoria en todos los endpoints (excepto register/login)
- Control de permisos granular (usuarios solo ven sus datos)
- Tokens con expiración configurable
- CSRF protection en producción
- Variables de entorno para secretos

---

## 🧪 Testing

*Testing en desarrollo* - Próximamente se agregarán tests unitarios y de integración.

Para ejecutar el servidor de desarrollo:
```bash
python manage.py runserver
```

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
✓ Autenticación y autorización con tokens  
✓ Serializers optimizados y datos anidados  
✓ Control de permisos granular  
✓ Optimización de queries (N+1 problem)  
✓ Deployment en producción  

**Feedback y sugerencias son bienvenidos** → [Abrir issue](https://github.com/MauRyze22/taskflow-api/issues)

---

## 📬 Contacto

**Amaury Monteagudo** — Backend Developer

Especializado en Python, Django, APIs REST y arquitecturas escalables.

📧 amaurymonteagudop22@gmail.com  
🔗 [GitHub](https://github.com/MauRyze22) | [LinkedIn](https://www.linkedin.com/in/amaury-monteagudo-40375b3a5)

---

## 📄 Licencia

[MIT License](LICENSE) — Uso libre con atribución.

---

⭐ **Si este proyecto te fue útil, considera darle una estrella — ¡gracias!**