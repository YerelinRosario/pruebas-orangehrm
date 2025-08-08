# Pruebas Automatizadas – OrangeHRM Demo

Este proyecto contiene la automatización de pruebas funcionales sobre el sistema **OrangeHRM Demo**, utilizando **Selenium** y **Pytest** en Python, como parte de la tarea de Pruebas Automatizadas.

---

## 📌 Descripción del Proyecto
Las pruebas cubren el flujo de autenticación y operaciones CRUD sobre empleados en el módulo **PIM** de OrangeHRM Demo.

**Historias de Usuario Automatizadas:**
- **HU001** – Login exitoso.
- **HU002** – Login con credenciales incorrectas (prueba negativa).
- **HU003** – Registrar empleado (Create).
- **HU004** – Actualizar datos de empleado (Update) *(no pasó al 100%, se documenta como intento)*.
- **HU005** – Eliminar empleado (Delete).

---

## 🛠 Tecnologías y Librerías
- **Python** 3.12
- **Selenium** – Automatización del navegador.
- **Pytest** – Framework de ejecución de pruebas.
- **Pytest-HTML** – Generación de reportes HTML.
- **WebDriver Manager** – Gestión automática del driver de Chrome.

---

## 📂 Estructura del Proyecto
pruebas-orangehrm/
├── tests/
│ ├── pages/
│ │ ├── login_page.py
│ │ └── pim_page.py
│ ├── conftest.py
│ ├── test_login_success.py
│ ├── test_login_invalid.py
│ ├── test_create_employee.py
│ ├── test_update_employee.py
│ └── test_delete_employee.py
├── reports/ # Reportes HTML generados automáticamente
├── screenshots/ # Capturas automáticas de cada prueba
├── requirements.txt
└── README.md


