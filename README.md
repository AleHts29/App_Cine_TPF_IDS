# 🎬 Sistema de Cine IDS 2025

## 🧾 Descripción General
Este proyecto corresponde al **Trabajo Práctico Final de Introducción al Desarrollo de Software (IDS)**.  
El objetivo es desarrollar una aplicación web para la gestión de un **Cine**, que permita consultar la cartelera, reservar asientos, comprar entradas y administrar funciones.

---

## 🚀 Tecnologías Utilizadas
- **Backend:** Flask (Python 3)
- **Frontend:** Flask Templates (Jinja + HTML + CSS + Bootstrap)
- **Base de Datos:** MySQL
- **Hosting:** PythonAnywhere
- **Control de Versiones:** GitHub + Kanban (GitHub Projects)
- **Formato de datos:** JSON
- **Opcional:** Docker, Swagger, App mobile con Kivy UI

---

## 🎯 Funcionalidades Principales

### 👥 Usuarios
- Registro, inicio y cierre de sesión.
- Perfiles con historial de compras y reservas.
- Roles: *Cliente* y *Administrador*.

### 🎬 Películas
- Listado y detalle de películas (sinopsis, género, duración, clasificación).
- Administración de películas (alta, baja, modificación).

### 🕓 Funciones y Salas
- Gestión de funciones (película, sala, horario, precio).
- Gestión de salas (capacidad, tipo: 2D / 3D / IMAX).

### 🎟️ Entradas y Reservas
- Selección de asientos disponibles.
- Reserva y compra de entradas.
- Emisión de ticket con código **QR**.
- Envío de confirmación por mail o WhatsApp.

### 📊 Reportes (solo admin)
- Ventas por película / día.
- Ocupación por sala.
- Gráficos estadísticos (Chart.js).

---

## 🗂️ Estructura de la Base de Datos

### Tablas principales:
- `usuarios` → id, nombre, apellido, email, password, rol
- `peliculas` → id, titulo, sinopsis, genero, duracion, clasificacion, imagen
- `salas` → id, nombre, capacidad, tipo
- `funciones` → id, pelicula_id, sala_id, fecha, hora, precio
- `reservas` → id, usuario_id, funcion_id, asientos, codigo_qr, fecha_compra

---

## 🔧 Requerimientos Obligatorios
- Uso de **GitHub** con commits claros y participación de todos los miembros.
- Tablero **Kanban** con backlog y tareas.
- **Flask Backend RESTful** conectado a MySQL.
- **Frontend Flask** que consuma el backend.
- **Archivo init.sh** con instalación de dependencias.
- **Informe** final con diseño, decisiones y conclusiones.
- Deploy en **https://www.pythonanywhere.com**.

---

## 💡 Requerimientos Deseables
- Contenerización con Docker.
- Documentación de endpoints con Swagger.
- Aplicación móvil desarrollada con Kivy UI.

---

## 🧱 Arquitectura del Sistema

```bash
Flask (Backend REST)  <-->  MySQL
        ↑
        ↓
Flask Templates / Frontend (Jinja + Bootstrap)
        ↓
PythonAnywhere (Hosting)
```
*(Opcional: App Mobile en Kivy que consume la API REST)*

---

## 🗓️ Cronograma de Entregas

| Fecha | Entregable |
|--------|-------------|
| 30/10 | Alcance + Mockups + Backlog |
| 11/11 | Repositorio + Templates + Endpoints + Tablas SQL |
| 18/11 | Integración API + BD + Frontend |
| 25/11 | Proyecto completo para revisión |
| 27/11 | 1° Entrega + Defensa |
| 05/12 | 2° Entrega (recuperación) |

---

## 🧩 Instalación y Ejecución

### 1️⃣ Clonar el repositorio
```bash
git clone https://github.com/tuusuario/sistema-cine.git
cd sistema-cine
```

### 2️⃣ Crear entorno virtual e instalar dependencias
```bash
pip install -r requirements.txt
```

### 3️⃣ Configurar la base de datos
```bash
# Crear base de datos MySQL
mysql -u root -p
CREATE DATABASE cine_db;
source scripts/init.sql
```

### 4️⃣ Ejecutar la aplicación
```bash
flask run
```

La aplicación se ejecutará en `http://localhost:5000`.

---

## 👨‍💻 Autores
Equipo IDS 2025 — Universidad Tecnológica Nacional  
Materia: *Introducción al Desarrollo de Software*

---

## 📜 Licencia
Este proyecto se distribuye con fines educativos bajo licencia MIT.
