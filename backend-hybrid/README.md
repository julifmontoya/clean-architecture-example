# clean-architecture-hybrid

Backend en Django + Django REST Framework para un catálogo de tours.

## Arquitectura
Híbrido pragmático de Clean Architecture:

- **Entidades/persistencia**: los modelos de Django ORM actúan como entidades y modelos de persistencia.
- **Casos de uso**: workflows de aplicación/negocio, aislados de las preocupaciones HTTP.
- **Presentación**: serializers, views y urls de DRF.
- **Puertos y adaptadores**: se introducen solo donde aportan valor real, especialmente para sistemas externos.

Se evitan las abstracciones innecesarias — los módulos se mantienen tan simples como lo permita el caso de uso.

## Estructura de carpetas
```
clean-architecture-hybrid/
├── config/                        # Proyecto Django: settings, URLs raíz, WSGI/ASGI
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── modules/                       # Módulos de negocio
│   ├── catalog/                   # Tours y categorías
│   │   ├── models.py
│   │   ├── admin.py
│   │   ├── tests.py
│   │   ├── application/
│   │   │   └── use_cases/         # CreateTour, UpdateTour, DeleteTour, GetTour,
│   │   │       ├── ...            # ListTours, CreateCategory, ListCategories, ...
│   │   ├── presentation/
│   │   │   ├── serializers/
│   │   │   │   ├── tour_serializer.py
│   │   │   │   └── category_serializer.py
│   │   │   ├── views/
│   │   │   │   ├── tour_views.py
│   │   │   │   └── category_views.py
│   │   │   └── urls.py
│   │   └── migrations/
│   └── inventory/                 # Disponibilidad y tarifas de tours
│       ├── models.py               # TourAvailability, TourRate
│       ├── admin.py
│       ├── tests.py
│       ├── application/
│       │   └── use_cases/         # CreateAvailability, ListAvailabilities, ...
│       ├── presentation/
│       │   ├── serializers/
│       │   │   ├── availability_serializer.py
│       │   │   └── rate_serializer.py
│       │   ├── views/
│       │   │   └── availability_views.py
│       │   └── urls.py
│       └── migrations/
├── shared/                        # Código compartido entre módulos (vacío por ahora)
├── env/                            # Entorno virtual con las dependencias instaladas
├── requirements.txt
├── manage.py
└── README.md
```

- `config/` — configuración del proyecto Django, URLs raíz (`v1/` monta las URLs de cada módulo), puntos de entrada WSGI/ASGI.
- `modules/` — módulos de negocio (`catalog`, `inventory`), cada uno siguiendo las capas descritas arriba (modelo → caso de uso → presentación).
- `shared/` — código compartido entre módulos, agnóstico de app.

## Cómo ejecutar el proyecto
Requiere Python 3.13.

### 1. Entorno virtual
Si ya existe la carpeta `env/` con las dependencias instaladas, puedes usarla directamente sin activarla, invocando su Python:

```
./env/Scripts/python.exe manage.py runserver
```

Si no existe (o quieres crear una desde cero):

```
python -m venv env
./env/Scripts/python.exe -m pip install -r requirements.txt
```

### 2. Migraciones de base de datos
El proyecto usa SQLite (`db.sqlite3`, no versionado). Antes de levantar el servidor por primera vez:

```
./env/Scripts/python.exe manage.py migrate
```

### 3. Levantar el servidor de desarrollo
```
./env/Scripts/python.exe manage.py runserver
```

La API queda disponible en `http://127.0.0.1:8000/`, con los endpoints de cada módulo bajo el prefijo `v1/` (p. ej. `http://127.0.0.1:8000/v1/tours/`). El panel de administración está en `http://127.0.0.1:8000/admin/`.

### 4. Crear un superusuario (opcional, para el admin)

```
./env/Scripts/python.exe manage.py createsuperuser
```

### 5. Ejecutar las pruebas
```
./env/Scripts/python.exe manage.py test
./env/Scripts/python.exe manage.py test modules.catalog
./env/Scripts/python.exe manage.py test modules.inventory
```

### Otros comandos útiles
```
./env/Scripts/python.exe manage.py check
./env/Scripts/python.exe manage.py makemigrations catalog
./env/Scripts/python.exe manage.py makemigrations inventory
```
