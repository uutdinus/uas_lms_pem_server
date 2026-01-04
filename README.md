# Simple LMS Backend Django

Project ini merupakan aplikasi backend Learning Management System (LMS) yang dibuat untuk memenuhi Tugas UAS Backend Development. Aplikasi ini dibangun menggunakan framework Django dan Django Ninja untuk membuat REST API, serta menggunakan JWT Authentication untuk proses login dan otorisasi user. Aplikasi dijalankan menggunakan Docker agar dapat dijalankan di laptop lain tanpa konfigurasi tambahan.

Project ini menyediakan fitur manajemen user, course, lesson, assignment, dan submission, serta dilengkapi dengan dokumentasi API menggunakan Swagger UI.

--------------------------------------------------

# 1. Tujuan Project

Tujuan pembuatan project ini adalah untuk:
1. Menerapkan konsep backend menggunakan Django
2. Membuat REST API menggunakan Django Ninja
3. Mengimplementasikan authentication menggunakan JWT
4. Menggunakan Docker sebagai media deployment aplikasi
5. Menyediakan dokumentasi API yang mudah diuji

--------------------------------------------------

# 2. Teknologi yang Digunakan

Teknologi yang digunakan dalam project ini antara lain:
1. Python 3.12
2. Django 6.0
3. Django Ninja
4. JWT Authentication
5. SQLite Database
6. Docker
7. Docker Compose
8. Redis

--------------------------------------------------

# 3. Struktur Project

Struktur folder project adalah sebagai berikut:

simple_lms_docker  
├── docker-compose.yml  
├── requirements.txt  
├── README.md  
├── docker  
│   ├── Dockerfile  
│   └── entrypoint.sh  
└── app  
    ├── manage.py  
    ├── db.sqlite3  
    ├── simple_lms  
    └── lms  

--------------------------------------------------

# 4. Cara Menjalankan Aplikasi

Langkah-langkah untuk menjalankan aplikasi adalah sebagai berikut:

1. Pastikan Docker dan Docker Compose sudah terinstall di laptop
2. Buka folder project
3. Jalankan perintah berikut pada terminal:

docker compose up --build

4. Tunggu hingga proses build dan container selesai dijalankan

--------------------------------------------------

# 5. Akses Aplikasi

Setelah aplikasi berjalan, aplikasi dapat diakses melalui:

1. Django Admin Panel  
http://localhost:8000/admin  

2. Dokumentasi API (Swagger UI)  
http://localhost:8000/api/docs  

--------------------------------------------------

# 6. User dan Role

Aplikasi ini menggunakan custom user dengan beberapa role, yaitu:
1. Admin
2. Dosen
3. Mahasiswa

User dapat ditambahkan dan dikelola melalui Django Admin Panel.

--------------------------------------------------

# 7. Authentication JWT

Proses login dilakukan menggunakan JWT Authentication melalui endpoint:

POST /api/lms/login

Parameter yang digunakan:
1. username
2. password

Jika login berhasil, API akan mengembalikan token JWT yang digunakan untuk mengakses endpoint yang membutuhkan autentikasi.

Contoh response login:
{
  "access_token": "jwt_token",
  "token_type": "bearer",
  "role": "dosen"
}

--------------------------------------------------

# 8. Endpoint API

Beberapa endpoint utama yang tersedia pada aplikasi ini adalah:

1. POST /api/lms/login
2. GET /api/lms/users
3. GET /api/lms/courses
4. POST /api/lms/courses
5. GET /api/lms/lessons
6. POST /api/lms/lessons
7. GET /api/lms/assignments
8. POST /api/lms/assignments
9. GET /api/lms/submissions
10. POST /api/lms/submissions

Seluruh endpoint dapat diuji langsung melalui Swagger UI.

--------------------------------------------------

# 9. Validasi Project

Project ini telah diuji menggunakan perintah:

docker compose exec web python manage.py check

Hasil pengujian menunjukkan:
System check identified no issues (0 silenced).

--------------------------------------------------


