# Simple LMS API (UAS Backend)

Project ini merupakan implementasi **Simple Learning Management System (LMS)** untuk memenuhi **Ujian Akhir Semester (UAS) Backend / SPAL**.  
Aplikasi dibangun menggunakan **Django + Django Ninja**, menerapkan **JWT Authentication**, **Role Based Access Control (RBAC)**, **Redis (Cache & Session)**, dan dijalankan menggunakan **Docker Compose**.

---

## Teknologi yang Digunakan
- Python 3.12
- Django
- Django Ninja (REST API)
- JWT Authentication
- Redis (Cache & Session)
- Docker & Docker Compose
- Swagger UI (API Documentation)

---

##  Arsitektur Sistem
Aplikasi dijalankan menggunakan **Docker Compose** dengan dua service utama:

- **web**  
  Backend Django API (JWT, RBAC, Redis Session)

- **redis**  
  Redis server untuk cache dan session backend

---

##  Fitur Utama
- Authentication menggunakan **JWT**
- Role Based Access Control (**RBAC**) dengan role:
  - `admin`
  - `dosen`
  - `mahasiswa`
- Redis digunakan sebagai:
  - Cache backend
  - Session backend (**WAJIB UAS**)
- Dokumentasi API otomatis menggunakan **Swagger UI**

---

##  Role & Hak Akses
| Role | Hak Akses |
|----|----------|
| Admin | Kelola user dan course |
| Dosen | Kelola course |
| Mahasiswa | Melihat course |

---

## Cara Menjalankan Project

### Masuk ke folder project
```bash
cd simple_lms_docker

Jalankan Docker Compose
docker compose up -d --build

 Pastikan Semua Service Aktif
docker compose ps


Status yang benar:

simple_lms_web → Up

simple_lms_redis → Up

🌐 Akses API

Swagger UI dapat diakses melalui:

http://localhost:8000/api/docs

Alur Penggunaan API (WAJIB UAS)
 Register User

Endpoint:

POST /api/lms/register


Contoh payload:

{
  "username": "admin1",
  "password": "admin123",
  "email": "admin1@test.com",
  "role": "admin"
}

 Login

Endpoint:

POST /api/lms/login


Response berhasil:

{
  "access_token": "<JWT_TOKEN>",
  "token_type": "bearer",
  "role": "admin"
}

 Authorize (Swagger)

Klik tombol Authorize di Swagger, lalu isi:

Bearer <JWT_TOKEN>

 Uji RBAC

Admin:

GET /api/lms/users → 200 OK


Mahasiswa:

GET /api/lms/users → 403 Forbidden


Ini membuktikan RBAC berjalan dengan benar.

 Redis Session (BUKTI WAJIB UAS)
Endpoint Test Session
GET /api/lms/test-session


Jika dipanggil berulang:

{ "count": 1 }
{ "count": 2 }
{ "count": 3 }


Menunjukkan session persisten dan tersimpan di Redis.

Verifikasi Redis via Terminal
docker compose exec redis redis-cli
INFO keyspace
SELECT 1
KEYS "*"


Contoh key session:

:1:django.contrib.sessions.cachexxxxxxxx
