# Proyecto: E-commerce D'asaro (Vitaminas y Suplementos)
## Arquitectura Backend y Directrices de Desarrollo

**1. Stack y Arquitectura Base:**
- Patrón: API RESTful o GraphQL.
- Backend Sugerido: Node.js o Python (para fácil manejo de lógica de recomendaciones).
- Base de Datos: PostgreSQL (esquemas relacionales para usuarios, inventario y órdenes).

**2. Módulos Principales:**
- **Catálogo y Usuarios:** Gestión de perfiles, autenticación (JWT) y control de stock.
- **Motor de Encuesta Nutricional:** Lógica para procesar respuestas del test, ejecutar el algoritmo de recomendación y almacenar el perfil de salud de forma segura.
- **Portal Educativo:** Estructura tipo CMS (Content Management System) para artículos de nutrición.
- **Gestión de Órdenes:** Carrito de compras, cálculo de costos de envío e impuestos.

**3. Seguridad y Privacidad (Prioridad Alta):**
- Cumplimiento de la Ley 1581 de 2012 (Habeas Data Colombia).
- Encriptación de datos sensibles (perfiles de salud/encuestas) en reposo y tránsito (HTTPS/TLS).

**4. Procesamiento de Pagos:**
- Integración vía API y Webhooks exclusivamente con **Wompi** o **PayU**.
- D'asaro NO procesará ni almacenará números de tarjetas (cumplimiento PCI-DSS delegado a la pasarela).