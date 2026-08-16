# Clean Architecture Example
Ejemplo full-stack de una app de catálogo de tours, con un backend y un frontend independientes, cada uno organizado en módulos de negocio siguiendo principios de Clean Architecture.

## Proyectos
| Proyecto | Stack | Descripción |
|---|---|---|
| [`backend-hybrid/`](backend-hybrid/README.md) | Django + Django REST Framework | API REST para el catálogo de tours (tours, categorías, disponibilidad y tarifas). |
| [`frontend/`](frontend/README.md) | Vue 3 + Vite + Tailwind CSS | SPA que consume la API para buscar y mostrar tours. |

Cada carpeta tiene su propio README con instrucciones detalladas de instalación, arquitectura y ejecución. Resumen rápido:

## Backend (`backend-hybrid/`)
```
./env/Scripts/python.exe manage.py migrate
./env/Scripts/python.exe manage.py runserver
```
Levanta la API en `http://127.0.0.1:8000/`, con los endpoints bajo `v1/` (p. ej. `http://127.0.0.1:8000/v1/tours/`).

Ver [`backend-hybrid/README.md`](backend-hybrid/README.md) para setup del entorno virtual, migraciones y tests.

## Frontend (`frontend/`)
```
npm install
npm run dev
```
Levanta la SPA en `http://localhost:5173`, consumiendo la API en `http://127.0.0.1:8000/v1/` (configurable en `src/core/http/api.js`).

Ver [`frontend/README.md`](frontend/README.md) para build de producción y convenciones de arquitectura.

## Cómo correr todo junto
1. Backend: `cd backend-hybrid && ./env/Scripts/python.exe manage.py runserver`
2. Frontend (en otra terminal): `cd frontend && npm install && npm run dev`
3. Abrir `http://localhost:5173`.

## Arquitectura
Ambos proyectos aplican una versión pragmática de Clean Architecture: cada módulo de negocio (`catalog`, `inventory` en el backend; `catalog`, `home` en el frontend) separa modelo/datos, casos de uso de aplicación y presentación, evitando abstracciones que no aporten valor real. Los detalles de capas y convenciones están documentados en el README de cada proyecto.
