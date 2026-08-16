# Clean Architecture Frontend
Aplicación frontend construida con **Vue 3**, **Vite** y **Tailwind CSS**, organizada siguiendo los principios de **Clean Architecture** mediante módulos independientes por dominio.

## Requisitos previos
- [Node.js](https://nodejs.org/) 18 o superior
- npm (incluido con Node.js)
- Un backend disponible en `http://127.0.0.1:8000/v1/` (configurado en `src/core/http/api.js`), necesario para que las vistas que consumen datos de tours funcionen correctamente.

## Instalación
```bash
npm install
```

## Ejecución del proyecto
### Entorno de desarrollo

Levanta el servidor de desarrollo con recarga en caliente:

```bash
npm run dev
```

Por defecto la aplicación queda disponible en `http://localhost:5173`.

### Compilación para producción
Genera el build optimizado en la carpeta `dist/`:

```bash
npm run build
```

### Previsualizar el build de producción
Sirve localmente el contenido ya compilado en `dist/`:

```bash
npm run preview
```

## Estructura del proyecto
```text
clean-architecture-frontend/
├── public/                            # Archivos estáticos servidos tal cual
├── src/
│   ├── app/                           # Capa de aplicación/shell: piezas compartidas de UI y assets globales
│   │   ├── assets/                    # Imágenes e íconos globales
│   │   └── components/                # Componentes de UI reutilizables y globales
│   │       └── Footer.vue             # Pie de página, visible en todas las páginas
│   │
│   ├── core/                          # Configuración técnica transversal, sin lógica de negocio
│   │   └── http/
│   │       └── api.js                 # Instancia de Axios con la URL base del backend
│   │
│   ├── modules/                       # Módulos de negocio, cada uno con su propia Clean Architecture
│   │   │
│   │   ├── home/                      # Módulo de la página de inicio
│   │   │   └── presentation/
│   │   │       ├── router/            # Rutas propias del módulo (ruta "home")
│   │   │       └── views/
│   │   │           └── HomeView.vue   # Vista de bienvenida con buscador de tours
│   │   │
│   │   └── catalog/                   # Módulo de catálogo de tours
│   │       ├── application/
│   │       │   └── use-cases/
│   │       │       └── GetTours.js    # Caso de uso: obtener tours según filtros
│   │       ├── infrastructure/
│   │       │   └── repositories/
│   │       │       └── ApiTourRepository.js  # Implementación del repositorio vía API REST
│   │       └── presentation/
│   │           ├── composables/       # Lógica de estado y comportamiento reutilizable por vista
│   │           │   ├── useTourList.js
│   │           │   └── useTourDetails.js
│   │           ├── router/            # Rutas propias del módulo ("tours", "tour-details")
│   │           └── views/
│   │               ├── TourListView.vue     # Listado y búsqueda de tours
│   │               └── TourDetailsView.vue  # Detalle de un tour específico
│   │
│   ├── router/
│   │   └── index.js                   # Router raíz: combina las rutas de todos los módulos
│   │
│   ├── App.vue                        # Componente raíz: layout global (RouterView + Footer)
│   ├── main.js                        # Punto de entrada de la aplicación
│   └── style.css                      # Estilos globales y configuración de Tailwind CSS
│
├── index.html                         # HTML raíz de la aplicación
├── vite.config.js                     # Configuración de Vite (plugins, alias "@")
└── package.json                       # Dependencias y scripts del proyecto
```

### Convenciones de la arquitectura
Cada módulo dentro de `src/modules` se organiza siguiendo las capas de Clean Architecture:

- **`application/use-cases`**: casos de uso con la lógica de negocio, independientes de frameworks o de la UI.
- **`infrastructure/repositories`**: implementaciones concretas que acceden a servicios externos (API, HTTP, etc.).
- **`presentation`**: todo lo relacionado con la interfaz de usuario del módulo (`views`, `composables` y `router`).

El router raíz (`src/router/index.js`) únicamente combina las rutas expuestas por cada módulo, sin definirlas directamente.

## Alias de importación
El proyecto usa el alias `@` para referenciar la carpeta `src`, por ejemplo:

```js
import Footer from "@/app/components/Footer.vue";
```
