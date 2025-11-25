# Learning BD2 2025 - Full Stack

Tarea de crear un formulario de registro de usuarios

## Estructura

- **learning-litestar-bd2-2025/** — Backend (Litestar + SQLite)
- **learning-vue-bd2-2025/** — Frontend (Vue 3 + TypeScript + Vuetify)

## Requisitos

- Python 3.13+
- Node.js 18+
- uv (gestor de paquetes Python)

## Instalación y uso

### Backend

cd learning-litestar-bd2-2025
uv sync
uv run alembic upgrade head
uv run python seed_users.py
uv run litestar run

### El backend correrá en http://localhost:8000.

cd learning-vue-bd2-2025
npm install
npm run dev

### El Frontend correrá en http://localhost:5173 (por defecto).
