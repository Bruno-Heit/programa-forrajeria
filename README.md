# Programa de gestión "Forrajería Torres"
El propósito de este proyecto es desarrollar un **programa de escritorio** adaptado a su ejecución en **Windows 10** para un **forraje local** y que permite al usuario realizar un *CRUD* a una base de datos que contiene los siguientes datos:

  - nombre, stock, categoría y precio de productos disponibles para su venta.
  - detalles sobre las ventas que se hacen durante las horas de atención.
  - detalles sobre las cuentas corrientes de los clientes, incluyendo algunos datos personales -no sensibles-.

El principal objetivo del programa es serle útil al usuario -obviamente- y al mismo tiempo que sea sencillo en su uso, intuitivo y no agobiante.


## TABLA DE CONTENIDOS

### INSTALACIÓN

### USO
El software se divide en 3 partes principales:
  - **INVENTARIO**  
  - **VENTAS**  
  - **CUENTAS CORRIENTES** (aún no en funcionamiento)


### INFORMACIÓN DEL DESARROLLO
El programa está desarrollado en ***Python*** en su versión 3.11, usando el framework para desarrollo de *GUIs* ***PySide6***.
El manejo de bases de datos es llevado a cabo con ***SQLite*** para lograr una mayor rapidez en la ejecución de las consultas.

### FUNCIONES A FUTURO
- [ ] Implementación de un **sistema de estadísticas** con respecto a los productos más vendidos -y menos vendidos- usando gráficos de barras (por ser valores discretos).
- [ ] Implementación de un **sistema de facturación** que permita crear facturas y distribuirlas a los clientes. **(a considerar)**
- [ ] Implementación de un sistema de pedidos a proveedores y registro de pedidos. **(a considerar)**

### LICENCIA
Software bajo licencia Apache v2.0.
URL oficial: [https://www.apache.org/licenses/LICENSE-2.0]
