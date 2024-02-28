# Programa de gestión "Forrajería Torres"
El propósito de este proyecto es desarrollar un **programa de escritorio** adaptado a su ejecución en **Windows 10** para un **forraje local** y que permite al usuario realizar un *CRUD* a una base de datos que contiene los siguientes datos:

  - nombre, stock, categoría y precio de productos disponibles para su venta.
  - detalles sobre las ventas que se hacen durante las horas de atención.
  - detalles sobre las cuentas corrientes de los clientes, incluyendo algunos datos personales -no sensibles-.

El principal objetivo del programa es serle útil al usuario -obviamente- y al mismo tiempo que sea sencillo en su uso, intuitivo y no agobiante.


## TABLA DE CONTENIDOS
  - [INSTALACIÓN](#INSTALACIÓN)
  - [USO](#USO)
    - [INVENTARIO](#INVENTARIO)
    - [VENTAS](#VENTAS)
  - [INFORMACIÓN DEL DESARROLLO](#INFORMACIÓN-DEL-DESARROLLO)
  - [FUNCIONES A FUTURO](#FUNCIONES-A-FUTURO)
  - [LICENCIA](#LICENCIA)

### INSTALACIÓN

### USO
El software se divide en 3 partes principales:
  #### **INVENTARIO**  
  La sección de Inventario sirve para mostrar los productos disponibles junto con algunos datos de interés como se muestra en la imagen siguiente.
  ![inventario ejemplo prueba datos tabla](images/sct_inventory.png)
    - **MUESTRA DE DATOS**:  
      Se pueden mostrar los datos principalmente de 2 formas:  
       1. usando la barra de búsqueda que hay encima de la tabla de inventario
       2. desde el menú desplegable, al cual se puede acceder haciendo *click* sobre las 3 líneas de la parte superior izquierda.
          ![inventario ejemplo prueba datos tabla menu-desplegable](images/sct_inventory_menu_opened.png)
          El menú desplegable permite mostrar productos que pertenezcan a una ***categoría determinada***, o directamente ***mostrarlos todos***.
    - **ELIMINACIÓN DE DATOS**:  
      Para eliminar datos simplemente se deben ***seleccionar los productos que se quieren borrar*** y luego hacer *click* en el botón rojo *"Eliminar producto"*.
    - **AGREGADO DE DATOS**:
      Por el contrario, para agregar datos nuevos es necesario presionar el botón azul *"Nuevo producto"*, lo que hará que se muestre un diálogo que pida varios datos
      sobre el nuevo producto. Para finalizar, simplemente presionar *"Aceptar"* y, ¡listo!. El producto fue creado exitosamente.
  #### **VENTAS**  
  #### **CUENTAS CORRIENTES** (aún no en funcionamiento)


### INFORMACIÓN DEL DESARROLLO
El programa está desarrollado en ***Python*** en su versión 3.11, usando el framework para desarrollo de *GUIs* ***PySide6***.
El manejo de bases de datos es llevado a cabo con ***SQLite*** para lograr una mayor rapidez en la ejecución de las consultas.

### FUNCIONES A FUTURO
- [ ] Las tablas aún no se pueden ordenar, por lo que antes de avanzar con las funciones de abajo pienso realizar esta.
- [ ] Implementación de un **sistema de estadísticas** con respecto a los productos más vendidos -y menos vendidos- usando gráficos de barras (por ser valores discretos).
- [ ] Implementación de un **sistema de facturación** que permita crear facturas y distribuirlas a los clientes. **(a considerar)**
- [ ] Implementación de un sistema de pedidos a proveedores y registro de pedidos. **(a considerar)**

### LICENCIA
Software bajo licencia Apache v2.0.
URL oficial: [https://www.apache.org/licenses/LICENSE-2.0]
