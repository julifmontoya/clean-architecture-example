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
│   ├── inventory/                 # Disponibilidad y tarifas de tours
│   │   ├── models.py               # TourAvailability, TourRate
│   │   ├── admin.py
│   │   ├── tests.py
│   │   ├── application/
│   │   │   └── use_cases/         # CreateAvailability, ListAvailabilities, ...
│   │   ├── presentation/
│   │   │   ├── serializers/
│   │   │   │   ├── availability_serializer.py
│   │   │   │   └── rate_serializer.py
│   │   │   ├── views/
│   │   │   │   └── availability_views.py
│   │   │   └── urls.py
│   │   └── migrations/
│   └── featured_tours/            # Tours destacados (reutiliza Tour de catalog)
│       ├── tests.py
│       ├── application/
│       │   └── use_cases/         # ListFeaturedTours
│       └── presentation/
│           ├── serializers/
│           │   └── featured_tour_serializer.py
│           ├── views/
│           │   └── featured_tour_views.py
│           └── urls.py
├── shared/                        # Código compartido entre módulos (vacío por ahora)
├── env/                            # Entorno virtual con las dependencias instaladas
├── requirements.txt
├── manage.py
└── README.md
```

- `config/` — configuración del proyecto Django, URLs raíz (`v1/` monta las URLs de cada módulo), puntos de entrada WSGI/ASGI.
- `modules/` — módulos de negocio (`catalog`, `inventory`, `featured_tours`), cada uno siguiendo las capas descritas arriba (modelo → caso de uso → presentación).
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

## 6. API

Todos los endpoints se montan bajo el prefijo de versión `v1/` del proyecto Django (`config/urls.py`). En desarrollo local, la URL base es:

```
http://127.0.0.1:8000/v1/
```

Ningún endpoint documentado a continuación requiere autenticación: el proyecto no define `REST_FRAMEWORK` en `config/settings.py` ni `permission_classes`/`authentication_classes` en ninguna vista, por lo que se aplican los valores por defecto de Django REST Framework (acceso público, `AllowAny`).

Las listas (`GET /v1/tours/`, `GET /v1/categories/`) no están paginadas: no hay una clase de paginación configurada, así que devuelven un array JSON plano con todos los resultados.

## 7. Catalog / Tours

Endpoints definidos en `modules/catalog/presentation/urls.py`, implementados por `TourListCreateAPIView` y `TourDetailAPIView` (`modules/catalog/presentation/views/tour_views.py`).

### 7.1 Listar tours

**Método**

GET

**Endpoint**

```
/v1/tours/
```

**Autenticación**

No requerida

**Descripción**

Devuelve todos los tours, con su categoría embebida y los precios tomados de su tarifa (`TourRate`) asociada, si existe. Implementado por `ListTours.execute()`, que hace `select_related("category", "rate")` y anota `min_price_adult`, `price_child`, `price_infant` desde `rate__price_adult`, `rate__price_child`, `rate__price_infant`.

**Parámetros de ruta**

Ninguno.

**Parámetros de consulta (query params)**

Definidos en `TourFilter` (`modules/catalog/presentation/filters/tour_filter.py`):

| Parámetro | Tipo | Comportamiento |
|---|---|---|
| `category` | entero | Filtra por `category_id` exacto. |
| `duration` | entero | Filtra por `duration` exacto. |
| `title` | texto | Filtra por coincidencia parcial, insensible a mayúsculas (`icontains`) sobre `title`. |

Ejemplo: `/v1/tours/?category=1&title=andes`

**Cuerpo de la petición**

No aplica.

**Respuesta exitosa**

`200 OK`, un array de tours:

```json
[
  {
    "id": 1,
    "title": "Andes Trek",
    "description": "A trek through the Andes.",
    "duration": 5,
    "itinerary_days": [
      { "day": 1, "description": "Arrival and city tour" },
      { "day": 2, "description": "Hiking excursion" }
    ],
    "included_not_included": {
      "included": ["Breakfast", "Transport"],
      "not_included": ["Flights", "Travel insurance"]
    },
    "category": { "id": 1, "title": "Adventure" },
    "min_price_adult": "100000.00",
    "price_child": "80000.00",
    "price_infant": "20000.00"
  }
]
```

Si el tour no tiene una `TourRate` asociada, `min_price_adult`, `price_child` y `price_infant` se devuelven como `null`.

**Posibles errores**

Ninguno específico: el endpoint siempre responde `200 OK`, incluso con filtros que no coinciden con ningún tour (devuelve un array vacío).

---

### 7.2 Crear tour

**Método**

POST

**Endpoint**

```
/v1/tours/
```

**Autenticación**

No requerida

**Descripción**

Crea un tour nuevo asociado a una categoría existente. Validado por `TourSerializer` y ejecutado por `CreateTour.execute()`.

**Parámetros de ruta**

Ninguno.

**Parámetros de consulta**

Ninguno.

**Cuerpo de la petición**

```json
{
  "title": "Andes Trek",
  "description": "A trek through the Andes.",
  "duration": 5,
  "itinerary_days": [
    { "day": 1, "description": "Arrival and city tour" },
    { "day": 2, "description": "Hiking excursion" }
  ],
  "included_not_included": {
    "included": ["Breakfast", "Transport"],
    "not_included": ["Flights", "Travel insurance"]
  },
  "category_id": 1
}
```

Campos: `title` (obligatorio), `itinerary_days` (obligatorio, JSON), `included_not_included` (obligatorio, JSON) y `category_id` (obligatorio, debe existir en `Category`). `description` es opcional (por defecto `""`) y `duration` es opcional (por defecto `0`).

**Respuesta exitosa**

`201 Created`, con el tour creado en el mismo formato que en el listado (incluyendo `category` embebida y precios `null` porque aún no tiene tarifa):

```json
{
  "id": 1,
  "title": "Andes Trek",
  "description": "A trek through the Andes.",
  "duration": 5,
  "itinerary_days": [
    { "day": 1, "description": "Arrival and city tour" },
    { "day": 2, "description": "Hiking excursion" }
  ],
  "included_not_included": {
    "included": ["Breakfast", "Transport"],
    "not_included": ["Flights", "Travel insurance"]
  },
  "category": { "id": 1, "title": "Adventure" },
  "category_id": 1,
  "min_price_adult": null,
  "price_child": null,
  "price_infant": null
}
```

**Posibles errores**

- `400 Bad Request`: falta algún campo obligatorio (p. ej. `itinerary_days`), error devuelto por `TourSerializer` con el nombre del campo inválido.
- `400 Bad Request`: `category_id` no corresponde a ninguna categoría existente (`CreateTour` lanza `ValueError`, traducido por la vista a `ValidationError`).

---

### 7.3 Obtener detalle de un tour

**Método**

GET

**Endpoint**

```
/v1/tours/<int:tour_id>/
```

**Autenticación**

No requerida

**Descripción**

Devuelve un tour por su id, con su categoría embebida y los precios de su tarifa asociada (si existe). Implementado por `GetTour.execute(tour_id)`.

**Parámetros de ruta**

| Parámetro | Tipo | Descripción |
|---|---|---|
| `tour_id` | entero | Id del tour a consultar. |

**Parámetros de consulta**

Ninguno.

**Cuerpo de la petición**

No aplica.

**Respuesta exitosa**

`200 OK`:

```json
{
  "id": 1,
  "title": "Andes Trek",
  "description": "A trek through the Andes.",
  "duration": 5,
  "itinerary_days": [
    { "day": 1, "description": "Arrival and city tour" },
    { "day": 2, "description": "Hiking excursion" }
  ],
  "included_not_included": {
    "included": ["Breakfast", "Transport"],
    "not_included": ["Flights", "Travel insurance"]
  },
  "category": { "id": 1, "title": "Adventure" },
  "min_price_adult": "100000.00",
  "price_child": "80000.00",
  "price_infant": "20000.00"
}
```

**Posibles errores**

- `404 Not Found`: no existe ningún tour con ese `tour_id` (`GetTour` lanza `ValueError`, traducido por la vista a `NotFound`).

---

### 7.4 Actualizar tour

**Método**

PUT

**Endpoint**

```
/v1/tours/<int:tour_id>/
```

**Autenticación**

No requerida

**Descripción**

Reemplaza los datos de un tour existente, incluyendo su categoría. Implementado por `UpdateTour.execute()`. No existe soporte para `PATCH` (actualización parcial); solo se implementa `PUT`.

**Parámetros de ruta**

| Parámetro | Tipo | Descripción |
|---|---|---|
| `tour_id` | entero | Id del tour a actualizar. |

**Parámetros de consulta**

Ninguno.

**Cuerpo de la petición**

Mismo formato que la creación (todos los campos se reemplazan):

```json
{
  "title": "Andes Trek",
  "description": "A trek through the Andes.",
  "duration": 8,
  "itinerary_days": [
    { "day": 1, "description": "Updated plan" }
  ],
  "included_not_included": {
    "included": ["Guide"],
    "not_included": ["Meals"]
  },
  "category_id": 1
}
```

**Respuesta exitosa**

`200 OK`, con el tour actualizado en el mismo formato que `GET /v1/tours/<id>/`.

**Posibles errores**

- `400 Bad Request`: falta algún campo obligatorio en el cuerpo de la petición (validación de `TourSerializer`).
- `404 Not Found`: no existe el tour con ese `tour_id`, o `category_id` no corresponde a ninguna categoría existente. En ambos casos `UpdateTour` lanza `ValueError`, que la vista traduce a `NotFound` (nótese que un `category_id` inválido también responde `404`, no `400`).

---

### 7.5 Eliminar tour

**Método**

DELETE

**Endpoint**

```
/v1/tours/<int:tour_id>/
```

**Autenticación**

No requerida

**Descripción**

Elimina un tour por su id. Implementado por `DeleteTour.execute()`, que hace `Tour.objects.filter(id=tour_id).delete()`.

**Parámetros de ruta**

| Parámetro | Tipo | Descripción |
|---|---|---|
| `tour_id` | entero | Id del tour a eliminar. |

**Parámetros de consulta**

Ninguno.

**Cuerpo de la petición**

No aplica.

**Respuesta exitosa**

`204 No Content`, sin cuerpo.

**Posibles errores**

Ninguno: al usar `filter(...).delete()`, el endpoint responde `204 No Content` incluso si el `tour_id` no existe (no distingue ese caso de una eliminación real).

## 8. Categories

Endpoint definido en `modules/catalog/presentation/urls.py`, implementado por `CategoryListCreateAPIView` (`modules/catalog/presentation/views/category_views.py`). No existe un endpoint de detalle, actualización o borrado de categorías individuales; solo listar y crear.

### 8.1 Listar categorías

**Método**

GET

**Endpoint**

```
/v1/categories/
```

**Autenticación**

No requerida

**Descripción**

Devuelve todas las categorías. Implementado por `ListCategories.execute()`.

**Parámetros de ruta**

Ninguno.

**Parámetros de consulta**

Ninguno (no admite filtros).

**Cuerpo de la petición**

No aplica.

**Respuesta exitosa**

`200 OK`:

```json
[
  { "id": 1, "title": "Adventure" }
]
```

**Posibles errores**

Ninguno específico: siempre responde `200 OK`.

---

### 8.2 Crear categoría

**Método**

POST

**Endpoint**

```
/v1/categories/
```

**Autenticación**

No requerida

**Descripción**

Crea una categoría nueva. Validado por `CategorySerializer` y ejecutado por `CreateCategory.execute()`.

**Parámetros de ruta**

Ninguno.

**Parámetros de consulta**

Ninguno.

**Cuerpo de la petición**

```json
{
  "title": "Adventure"
}
```

**Respuesta exitosa**

`201 Created`:

```json
{
  "id": 1,
  "title": "Adventure"
}
```

**Posibles errores**

- `400 Bad Request`: falta el campo `title` o está vacío (validación de `CategorySerializer`).

## 9. Featured Tours

Endpoint definido en `modules/featured_tours/presentation/urls.py`, implementado por `FeaturedTourListAPIView` (`modules/featured_tours/presentation/views/featured_tour_views.py`). No tiene modelo propio: reutiliza `Tour` de `catalog` a través de `ListFeaturedTours.execute()`, que llama a `ListTours().execute().order_by("id")[:limit]` (`modules/featured_tours/application/use_cases/list_featured_tours.py`).

### 9.1 Listar tours destacados

**Método**

GET

**Endpoint**

```
/v1/featured-tours/
```

**Autenticación**

No requerida

**Descripción**

Devuelve los primeros tours (ordenados por `id`), con su categoría embebida y `min_price_adult` tomado de su `TourRate` si existe. El límite es fijo en el código: `DEFAULT_FEATURED_TOURS_LIMIT = 3`, no configurable por query param.

**Parámetros de ruta**

Ninguno.

**Parámetros de consulta**

Ninguno.

**Cuerpo de la petición**

No aplica.

**Respuesta exitosa**

`200 OK`, un array de hasta 3 tours:

```json
[
  {
    "id": 1,
    "title": "Andes Trek",
    "description": "A trek through the Andes.",
    "duration": 5,
    "category": { "id": 1, "title": "Adventure" },
    "min_price_adult": "100000.00"
  }
]
```

Si el tour no tiene una `TourRate` asociada, `min_price_adult` se devuelve como `null`. A diferencia de `GET /v1/tours/`, esta respuesta no incluye `itinerary_days`, `included_not_included`, `price_child` ni `price_infant` (serializados por `FeaturedTourSerializer`, no por `TourSerializer`).

**Posibles errores**

Ninguno específico: el endpoint siempre responde `200 OK`, incluso sin tours (devuelve un array vacío).

## 10. Inventory / Availability

No hay endpoints de disponibilidad (`availability`) implementados actualmente en `modules/inventory/`. El modelo `TourAvailability` existió en la migración inicial del módulo (`modules/inventory/migrations/0001_initial.py`), pero fue eliminado por la migración `0002_simplify_tour_rate.py`; en el código actual `modules/inventory/models.py` solo define `TourRate`, y `modules/inventory/presentation/urls.py` solo expone el endpoint de tarifas documentado en la sección 10. No se documentan endpoints aquí para evitar describir funcionalidad que no existe en el código.

## 11. Inventory / Rates

Endpoint definido en `modules/inventory/presentation/urls.py`, implementado por `TourRateAPIView` (`modules/inventory/presentation/views/rate_views.py`). Gestiona la tarifa (`TourRate`) de un tour, en una relación uno a uno (`tour.rate`).

### 10.1 Obtener la tarifa de un tour

**Método**

GET

**Endpoint**

```
/v1/tours/<int:tour_id>/rate/
```

**Autenticación**

No requerida

**Descripción**

Devuelve la tarifa vigente de un tour. Implementado por `GetTourRate.execute(tour_id)`.

**Parámetros de ruta**

| Parámetro | Tipo | Descripción |
|---|---|---|
| `tour_id` | entero | Id del tour cuya tarifa se consulta. |

**Parámetros de consulta**

Ninguno.

**Cuerpo de la petición**

No aplica.

**Respuesta exitosa**

`200 OK`:

```json
{
  "price_adult": "100000.00",
  "price_child": "80000.00",
  "price_infant": "20000.00"
}
```

**Posibles errores**

- `404 Not Found`: el tour existe pero no tiene una tarifa asignada todavía (`GetTourRate` devuelve `None`, la vista lanza `NotFound`). El mismo `404` también ocurre si el `tour_id` no corresponde a ningún tour, ya que `GetTourRate` no distingue "tour inexistente" de "tour sin tarifa".

---

### 10.2 Crear o actualizar la tarifa de un tour

**Método**

PUT

**Endpoint**

```
/v1/tours/<int:tour_id>/rate/
```

**Autenticación**

No requerida

**Descripción**

Crea la tarifa del tour si no existe, o la actualiza si ya existe (`update_or_create` sobre `TourRate`, usando `tour` como clave). Implementado por `SetTourRate.execute()`.

**Parámetros de ruta**

| Parámetro | Tipo | Descripción |
|---|---|---|
| `tour_id` | entero | Id del tour al que se le asigna/actualiza la tarifa. |

**Parámetros de consulta**

Ninguno.

**Cuerpo de la petición**

```json
{
  "price_adult": "100000",
  "price_child": "80000",
  "price_infant": "20000"
}
```

Los tres campos (`price_adult`, `price_child`, `price_infant`) son obligatorios.

**Respuesta exitosa**

`200 OK` (tanto al crear como al actualizar la tarifa):

```json
{
  "price_adult": "100000.00",
  "price_child": "80000.00",
  "price_infant": "20000.00"
}
```

**Posibles errores**

- `400 Bad Request`: falta alguno de los tres campos de precio (validación de `TourRateSerializer`).
- `400 Bad Request`: `tour_id` no corresponde a ningún tour existente (`SetTourRate` lanza `ValueError`, traducido por la vista a `ValidationError`).

