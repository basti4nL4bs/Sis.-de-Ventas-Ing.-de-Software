======================================================================
           SISTEMA WEB DE VENTAS - COMERCIO LOCAL
======================================================================

DESCRIPCION:
Aplicacion web para la automatizacion y registro de ventas en 
comercios minoristas, con calculo impositivo automatico del 19% de IVA, 
control de jornada comercial y emision diferenciada de Boletas y Facturas.

----------------------------------------------------------------------
1. TECNOLOGIAS UTILIZADAS
----------------------------------------------------------------------
- Frontend: React (Vite), Axios, React Router DOM, HTML5, CSS3.
- Backend: Python, Django 4.2, Django REST Framework, Django CORS Headers.
- Base de Datos: MySQL Server 8.0 (XAMPP).
- Control de Versiones: Git y GitHub.

----------------------------------------------------------------------
2. REQUISITOS PREVIOS
----------------------------------------------------------------------
- XAMPP instalado con servicios Apache y MySQL iniciados.
- Python 3.10 o superior instalado.
- Node.js (version LTS) instalado.

----------------------------------------------------------------------
3. PUESTA EN MARCHA (PASO A PASO)
----------------------------------------------------------------------

PASO A: BASE DE DATOS (XAMPP)
1. Abrir panel de control de XAMPP e iniciar "Apache" y "MySQL".
2. Ingresar al navegador en: http://localhost/phpmyadmin/
3. Crear una nueva base de datos llamada: sistema_ventas

PASO B: BACKEND (DJANGO)
Abrir una terminal en la raiz del proyecto (sistema-ventas):

1. Crear entorno virtual:
   python -m venv venv

2. Activar entorno virtual (Windows PowerShell):
   .\venv\Scripts\activate

3. Instalar librerias:
   pip install "django<5.0" djangorestframework mysqlclient django-cors-headers

4. Crear tablas en MySQL:
   python manage.py makemigrations core
   python manage.py migrate

5. Iniciar servidor backend:
   python manage.py runserver

PASO C: FRONTEND (REACT)
Abrir una SEGUNDA terminal en la raiz del proyecto (sistema-ventas):

1. Entrar a la carpeta frontend:
   cd frontend

2. Instalar modulos de Node:
   npm install

3. Iniciar servidor de desarrollo:
   npm run dev

----------------------------------------------------------------------
4. DIRECCIONES DE ACCESO
----------------------------------------------------------------------
- Terminal de Ventas (Frontend): http://localhost:5173/
- API REST (Backend):             http://127.0.0.1:8000/api/
- Panel Administrador Django:    http://127.0.0.1:8000/admin/

----------------------------------------------------------------------
5. FUNCIONALIDADES CLAVE
----------------------------------------------------------------------
- Catalogo dinamico de productos conectado a MySQL.
- Calculo automatico en tiempo real de Subtotal Neto, 19% IVA y Total.
- Emision de Boleta simple o Factura (con RUT, Razon Social, Giro y Direccion).
- Modal de vista previa y confirmacion previa al guardado definitivo.
- Arquitectura con patrones de diseno: Factory Method y Singleton.
======================================================================