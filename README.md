# TechShop Pro - E-commerce de Tecnología de Alta Gama 🚀

![Django](https://img.shields.io/badge/django-%23092e20.svg?style=for-the-badge&logo=django&logoColor=white)
![TailwindCSS](https://img.shields.io/badge/tailwindcss-%2338B2AC.svg?style=for-the-badge&logo=tailwind-css&logoColor=white)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)

TechShop es una plataforma de comercio electrónico profesional diseñada con un enfoque en **rendimiento, usabilidad y conversión**. Inspirada en los estándares de las grandes tiendas de hardware de Paraguay y la región, el sistema permite una gestión autónoma de productos y un cierre de ventas directo a través de WhatsApp.

---

## ✨ Características Principales

### 🖥️ Experiencia de Usuario (Frontend)
- **Diseño Ultra-Responsive:** Adaptado perfectamente para celulares, tablets y computadoras.
- **Sliders Inteligentes:** Carruseles de banners y productos con ciclo infinito y navegación manual, optimizados para una carga rápida.
- **Menú Lateral Multi-Nivel:** Sistema de navegación estilo "drill-down" (inspirado en Shopping China) que permite explorar categorías y subcategorías sin recargas de página.
- **Buscador Funcional:** Motor de búsqueda que filtra en tiempo real sobre toda la base de datos.
- **Galería de Productos Interactiva:** Visualización de múltiples ángulos de producto con cambio de imagen instantáneo.

### ⚙️ Funcionalidad y Gestión (Backend)
- **Panel Administrativo Robusto:** Gestión completa de Banners, Categorías, Marcas, Productos y Stock desde el Administrador de Django.
- **Lógica de Carrito Persistente:** Sistema de carrito basado en **Sesiones**, permitiendo agrupar productos por cantidad y calcular subtotales automáticamente.
- **Gestión de Stock:** Visualización dinámica de disponibilidad (En Stock, Bajo Consulta, Agotado).
- **Checkout vía WhatsApp:** Integración con la API de WhatsApp que genera un mensaje automático detallado con el pedido y el total en Guaraníes (Gs.).

---

## 🛠️ Stack Tecnológico
*   **Lenguaje:** Python 3.x
*   **Framework Web:** Django (MVT Architecture)
*   **Diseño:** Tailwind CSS (Framework de utilidad primero)
*   **Base de Datos:** SQLite3 (Escalable a PostgreSQL/MySQL)
*   **Formato de Datos:** Django Humanize para moneda local (Gs.)

---

## 🚀 Instalación y Uso Local

1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com/Fatima6510/mi-ecommerce.git

Crear y activar entorno virtual:
code
Bash
python -m venv venv
venv\Scripts\activate
Instalar dependencias:
code
Bash
pip install -r requirements.txt
Ejecutar migraciones e iniciar:
code
Bash
python manage.py migrate
python manage.py runserver

---

## 👤 Autor
Desarrollado por **Fatima Rojas** - **Desarrolladora Web Python/Django**.
Especializada en la creación de soluciones digitales interactivas y plataformas de comercio electrónico escalables.