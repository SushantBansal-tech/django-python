# Workspace

## Overview

pnpm workspace monorepo using TypeScript. Each package manages its own dependencies.
Also contains a Django REST Framework project at `django_project/`.

## Stack

- **Monorepo tool**: pnpm workspaces
- **Node.js version**: 24
- **Package manager**: pnpm
- **TypeScript version**: 5.9
- **API framework**: Express 5 (Node.js), Django REST Framework (Python)
- **Database**: PostgreSQL + Drizzle ORM (Node.js), SQLite (Django dev)
- **Validation**: Zod (`zod/v4`), `drizzle-zod` (Node.js), DRF Serializers (Django)
- **API codegen**: Orval (from OpenAPI spec)
- **Build**: esbuild (CJS bundle)

## Structure

```text
artifacts-monorepo/
├── artifacts/              # Deployable applications
│   └── api-server/         # Express API server
├── lib/                    # Shared libraries
│   ├── api-spec/           # OpenAPI spec + Orval codegen config
│   ├── api-client-react/   # Generated React Query hooks
│   ├── api-zod/            # Generated Zod schemas from OpenAPI
│   └── db/                 # Drizzle ORM schema + DB connection
├── django_project/         # Django REST Framework project
│   ├── django_project/     # Main settings, urls, wsgi
│   ├── vendor/             # Vendor master app
│   ├── product/            # Product master app
│   ├── course/             # Course master app
│   ├── certification/      # Certification master app
│   ├── vendor_product_mapping/        # Vendor→Product mapping app
│   ├── product_course_mapping/        # Product→Course mapping app
│   └── course_certification_mapping/  # Course→Certification mapping app
├── scripts/                # Utility scripts
└── package.json            # Root package
```

## Django Project

The Django project lives at `django_project/` and runs on port 8000.

### Apps

**Master apps:** `vendor`, `product`, `course`, `certification`
**Mapping apps:** `vendor_product_mapping`, `product_course_mapping`, `course_certification_mapping`

### Running the Django server

```bash
cd django_project && python manage.py runserver 0.0.0.0:8000
```

### API Endpoints

- `GET/POST /api/vendors/`
- `GET/PUT/PATCH/DELETE /api/vendors/<id>/`
- `GET/POST /api/products/`
- `GET/PUT/PATCH/DELETE /api/products/<id>/`
- `GET/POST /api/courses/`
- `GET/PUT/PATCH/DELETE /api/courses/<id>/`
- `GET/POST /api/certifications/`
- `GET/PUT/PATCH/DELETE /api/certifications/<id>/`
- `GET/POST /api/vendor-product-mappings/`
- `GET/PUT/PATCH/DELETE /api/vendor-product-mappings/<id>/`
- `GET/POST /api/product-course-mappings/`
- `GET/PUT/PATCH/DELETE /api/product-course-mappings/<id>/`
- `GET/POST /api/course-certification-mappings/`
- `GET/PUT/PATCH/DELETE /api/course-certification-mappings/<id>/`

### Docs

- `GET /swagger/` — Swagger UI
- `GET /redoc/` — ReDoc
- `GET /swagger.json` — OpenAPI JSON spec

### Migrations

```bash
cd django_project && python manage.py makemigrations
cd django_project && python manage.py migrate
```
