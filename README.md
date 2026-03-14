# 🛒 Django Vendor–Product–Course–Certification API

![Python](https://img.shields.io/badge/Python-3.11-blue?style=flat-square&logo=python)
![Django](https://img.shields.io/badge/Django-4.x-green?style=flat-square&logo=django)
![DRF](https://img.shields.io/badge/Django_REST_Framework-3.x-red?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)
![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=flat-square)

A modular **Django REST Framework** backend for managing **Vendors, Products, Courses, Certifications**, and their **hierarchical mappings**.

> Built using **APIView only** — no ViewSets, no GenericAPIView, no mixins, and no routers.

---

## 📚 Table of Contents

- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Setup & Installation](#-setup--installation)
- [Running the Server](#-running-the-server)
- [API Documentation](#-api-documentation)
- [API Endpoints](#-api-endpoints)
- [Validation Rules](#-validation-rules)
- [Query Parameter Filtering](#-query-parameter-filtering)
- [Models](#-models)
- [Admin Panel](#-admin-panel)

---

## 🛠 Tech Stack

| Tool | Purpose |
|------|---------|
| Python 3.11 | Programming language |
| Django 4.x | Web framework |
| Django REST Framework | API layer |
| drf-yasg | Swagger / ReDoc documentation |
| SQLite | Default development database |

---

## 📁 Project Structure

```
django_project/
├── django_project/                    # Core settings, URLs, WSGI
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── vendor/                            # Vendor master app
├── product/                           # Product master app
├── course/                            # Course master app
├── certification/                     # Certification master app
├── vendor_product_mapping/            # Vendor → Product mapping app
├── product_course_mapping/            # Product → Course mapping app
├── course_certification_mapping/      # Course → Certification mapping app
└── manage.py
```

Each app contains:

```
models.py
serializers.py
views.py
urls.py
admin.py
apps.py
```

---

## ⚙️ Setup & Installation

### 1. Install dependencies

```bash
pip install django djangorestframework drf-yasg
```

### 2. Apply migrations

```bash
cd django_project
python manage.py makemigrations
python manage.py migrate
```

### 3. (Optional) Create a superuser for Django Admin

```bash
python manage.py createsuperuser
```

---

## 🚀 Running the Server

```bash
cd django_project
python manage.py runserver 0.0.0.0:8000
```

Server runs at:

```
http://localhost:8000
```

---

## 📖 API Documentation

| URL | Description |
|-----|-------------|
| `/swagger/` | Swagger UI (interactive) |
| `/redoc/` | ReDoc documentation |
| `/swagger.json` | Raw OpenAPI JSON spec |

---

## 🔌 API Endpoints

### Vendors

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/vendors/` | List all vendors |
| `POST` | `/api/vendors/` | Create vendor |
| `GET` | `/api/vendors/<id>/` | Retrieve vendor |
| `PUT` | `/api/vendors/<id>/` | Full update |
| `PATCH` | `/api/vendors/<id>/` | Partial update |
| `DELETE` | `/api/vendors/<id>/` | Delete vendor |

### Products

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/products/` | List products |
| `POST` | `/api/products/` | Create product |
| `GET` | `/api/products/<id>/` | Retrieve product |
| `PUT` | `/api/products/<id>/` | Full update |
| `PATCH` | `/api/products/<id>/` | Partial update |
| `DELETE` | `/api/products/<id>/` | Delete product |

### Courses

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/courses/` | List courses |
| `POST` | `/api/courses/` | Create course |
| `GET` | `/api/courses/<id>/` | Retrieve course |
| `PUT` | `/api/courses/<id>/` | Full update |
| `PATCH` | `/api/courses/<id>/` | Partial update |
| `DELETE` | `/api/courses/<id>/` | Delete course |

### Certifications

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/certifications/` | List certifications |
| `POST` | `/api/certifications/` | Create certification |
| `GET` | `/api/certifications/<id>/` | Retrieve certification |
| `PUT` | `/api/certifications/<id>/` | Full update |
| `PATCH` | `/api/certifications/<id>/` | Partial update |
| `DELETE` | `/api/certifications/<id>/` | Delete certification |

### Vendor → Product Mappings

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/vendor-product-mappings/` | List mappings |
| `POST` | `/api/vendor-product-mappings/` | Create mapping |
| `GET` | `/api/vendor-product-mappings/<id>/` | Retrieve mapping |
| `PUT` | `/api/vendor-product-mappings/<id>/` | Full update |
| `PATCH` | `/api/vendor-product-mappings/<id>/` | Partial update |
| `DELETE` | `/api/vendor-product-mappings/<id>/` | Delete mapping |

### Product → Course Mappings

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/product-course-mappings/` | List mappings |
| `POST` | `/api/product-course-mappings/` | Create mapping |
| `GET` | `/api/product-course-mappings/<id>/` | Retrieve mapping |
| `PUT` | `/api/product-course-mappings/<id>/` | Full update |
| `PATCH` | `/api/product-course-mappings/<id>/` | Partial update |
| `DELETE` | `/api/product-course-mappings/<id>/` | Delete mapping |

### Course → Certification Mappings

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/course-certification-mappings/` | List mappings |
| `POST` | `/api/course-certification-mappings/` | Create mapping |
| `GET` | `/api/course-certification-mappings/<id>/` | Retrieve mapping |
| `PUT` | `/api/course-certification-mappings/<id>/` | Full update |
| `PATCH` | `/api/course-certification-mappings/<id>/` | Partial update |
| `DELETE` | `/api/course-certification-mappings/<id>/` | Delete mapping |

---

## ✅ Validation Rules

| Rule | Behaviour |
|------|-----------|
| Required fields | `name` and `code` required for all master entities |
| Unique code | Each entity's code must be unique and stored uppercase |
| Duplicate mapping | Same parent-child mapping cannot exist twice |
| Primary mapping | Only **one mapping per parent** can have `primary_mapping=true` |
| Valid foreign keys | Referenced entities must exist and be active |

### Example Error Responses

**Duplicate code:**
```json
{
  "code": ["A vendor with code 'ACME' already exists."]
}
```

**Duplicate mapping:**
```json
{
  "non_field_errors": [
    "A mapping between Vendor(1) and Product(1) already exists."
  ]
}
```

**Duplicate primary mapping:**
```json
{
  "primary_mapping": [
    "Vendor(1) already has a primary product mapping."
  ]
}
```

---

## 🔍 Query Parameter Filtering

```bash
GET /api/products/?vendor_id=1
GET /api/courses/?product_id=2
GET /api/certifications/?course_id=3
GET /api/vendors/?is_active=true
GET /api/vendors/?search=acme
GET /api/vendor-product-mappings/?vendor_id=1
GET /api/vendor-product-mappings/?primary_mapping=true
```

---

## 🗄 Models

### Master Entity Fields

| Field | Type | Notes |
|-------|------|-------|
| `id` | Integer | Auto primary key |
| `name` | CharField | Required |
| `code` | CharField | Required, unique, uppercase |
| `description` | TextField | Optional |
| `is_active` | Boolean | Default: `true` |
| `created_at` | DateTime | Auto created |
| `updated_at` | DateTime | Auto updated |

### Mapping Model Fields

| Field | Type | Notes |
|-------|------|-------|
| `id` | Integer | Auto primary key |
| `parent` | ForeignKey | e.g. vendor / product / course |
| `child` | ForeignKey | e.g. product / course / certification |
| `primary_mapping` | Boolean | Only one per parent |
| `is_active` | Boolean | Default: `true` |
| `created_at` | DateTime | Auto created |
| `updated_at` | DateTime | Auto updated |

---

## 🔧 Admin Panel

Access Django Admin at:

```
http://localhost:8000/admin/
```

After creating a superuser:

```bash
python manage.py createsuperuser
```

All models are registered and fully searchable through the **Django Admin interface**.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

<p align="center">Made with ❤️ using Django REST Framework</p>
