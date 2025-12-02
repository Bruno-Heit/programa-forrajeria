<a id="readme-top"></a>

[![Issues][issues-shield]][issues-url]
[![project_license][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]



<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/Bruno-Heit/programa-forrajeria">
    <img src="icons/program_icon.png" alt="Logo" width="80" height="80">
  </a>

<h3 align="center">programa-forrajeria</h3>

  <p align="center">
    Programa de escritorio para gestionar un forraje con control de productos, ventas y cuentas corrientes
    <br />
    <a href="https://github.com/Bruno-Heit/programa-forrajeria"><strong>Ver documentación »</strong></a>
    <br />
    <br />
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Tabla de contenidos</summary>
  <ol>
    <li>
      <a href="#acerca-del-proyecto">Acerca del proyecto</a>
      <ul>
        <li><a href="#hecho-con">Hecho con</a></li>
      </ul>
    </li>
    <li>
      <a href="#para-empezar">Para empezar</a>
      <ul>
        <li><a href="#instalación">Instalación</a></li>
        <ul>
          <li><a href="#ejecutable">Ejecutable</a></li>
          <li><a href="#proyecto-completo">Proyecto completo</a></li>
        </ul>
      </ul>
    </li>
    <li><a href="#uso">Uso</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#licencia">Licencia</a></li>
    <li><a href="#contacto">Contacto</a></li>
    <li><a href="#agradecimientos">Agradecimientos</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## Acerca del proyecto

Éste proyecto apunta a ayudar en la digitalización de la información que maneja el comercio, mejorar su organización a corto, medio y largo plazo y simplificar algunas tareas diarias.
<ul>
  <li>
    <strong>¿Cómo está compuesto el programa?</strong>
    <p>
    Por el momento está separado en tres secciones principales: inventario, ventas y cuentas corrientes.
    </p>
  </li>

  <br>

  <li>
    <strong>¿Qué datos contiene cada sección?</strong>
    <p>
    La sección de inventario contiene información sobre cada producto, como su stock, precio público, precio comercial, entre otros detalles.
    </p>
    <br>
    <p>
    La sección de ventas contiene información sobre cada venta concretada (es decir, cada producto vendido) y su cantidad, costo total y cantidad abonada, entre otros.
    </p>
    <br>
    <p>
    La sección de cuentas corrientes guarda información sobre cada una de las cuentas corrientes abiertas en el negocio, y naturalmente contiene datos personales del propietario de la cuenta. Para cumplir con la ley de protección de datos personales 25.326 (República Argentina) los únicos datos que son obligatorios de cada cuenta corriente son el nombre y apellido del propietario, el resto de datos pedidos en el programa son considerados opcionales.
    </p>
  </li>

  <br>

  <li>
    <strong>¿Qué operaciones se pueden realizar sobre los datos?</strong>
    <p>
    todas las secciones permiten mostrar, actualizar, eliminar o agregar datos nuevos dependiendo de la necesidad del usuario.
    </p>
  </li>

  <br>

  <li>
    <strong>¿Cuál es el propósito de "digitalizar la información"?</strong>
    <p>
    De todos los datos que el negocio maneja se lleva registro a mano usando lapicera y papel pero a medida que la clientela ha aumentado con el paso del tiempo han surgido problemas al llevar dichos registros; por ejemplo: <i>se olvidan llenar datos, la información es deficiente o ambigua</i>, entre otras razones. Estos problemas de información llevan a otros problemas, como los siguientes: <i>imposiblidad de llevar un stock al día, dificultad al hacer pedidos a proveedores, omisiones accidentales de registros de ventas, omisiones accidentales con respecto a cuentas corrientes.</i>
    </p>
    <br>
    <p>
    Por suerte estos problemas son evitables automatizando algunos procesos intermedios.
    </p>
  </li>

  <br>

  <li>
    <strong>¿Cómo se logra la "simplificación de las tareas"?</strong>
    <p>
    El programa está hecho a medida para el usuario, por lo que la simplificación de tareas probablemente será diferente a la de otros programas de gestión. Algunos ejemplos de esto son: una interfaz de usuario diseñada específicamente para acceder rápida y fácilmente a las operaciones que más se llevan a cabo en el negocio, además que permite realizar cambios eficientes en la información cuando se necesite; un menú que permite aumentar o disminuir precios de productos usando porcentajes en uno o más de ellos simultáneamente; la posiblidad de ver un resumen de qué productos hubo históricamente en una cuenta corriente dada; o una validación de datos personalizada de acuerdo a la necesidad del usuario.
    </p>
  </li>

  <br>

</ul>

<p align="right">(<a href="#readme-top">volver al inicio</a>)</p>



### Hecho con

* [![Python][Python]][Python-url]
* [![Qt][Qt]][Qt-url]
* [![SQLite][SQLite]][SQLite-url]
* [![Numpy][Numpy]][Numpy-url]
* [![Css][Css]][Css-url]

<p align="right">(<a href="#readme-top">volver al inicio</a>)</p>



<!-- GETTING STARTED -->
## Para empezar
Para ejecutar el programa simplemente es necesario abrir el archivo *main.exe* y listo.

### Instalación
#### Ejecutable
Descargar el archivo *main.exe* usado para ejecutar el programa, no requiere instalación.

#### Proyecto completo
Contiene el código fuente y todos los demás archivos necesarios para ejecutar el programa (Se recomienda clonar el repositorio dentro de un entorno virtual):
   ```sh
   git clone https://github.com/Bruno-Heit/programa-forrajeria.git
   ```
En la carpeta raíz se encuentra un archivo *requirements.txt* con las librerías necesarias para correr el programa.
Luego de clonado el repositorio es necesario instalar esas dependencias:
   ```sh
   pip install -r requirements.txt
   ```
Para ejecutar el código hay que ejecutar *main.py*.

<p align="right">(<a href="#readme-top">volver al inicio</a>)</p>



<!-- USAGE EXAMPLES -->
## Uso

Como ya se ha mencionado, el programa se divide en 3 secciones principales:
<ul>
  <li>Inventario</li>
  <li>Ventas</li>
  <li>Cuentas corrientes</li>
</ul>
Todas las secciones contienen <i>tablas</i> que permiten <strong>mostrar, modificar, añadir o eliminar datos</strong> según se necesite, pero además contienen subsecciones o funciones adicionales exclusivas que permiten modificar, ver o interactuar con los datos de una forma más simple, efectiva y adaptada a cada sección.
<br>
<br>
En <strong>inventario</strong> se muestran los productos disponibles y hay funciones exclusivas para modificar precios directamente usando porcentajes en tandas de productos.
<br>
<br>
En <strong>ventas</strong> se muestran todas las ventas efectuadas y cuenta con una subsección referida como <i>formulario de venta</i> que brinda una interfaz más simple para concretar las ventas.
<br>
<br>
En <strong>cuentas corientes</strong> se muestran las cuentas corrientes activas y el saldo que cada una tiene, además al interactuar con la columna del saldo es posible ver los productos en la cuenta corriente.
<br>
<br>

<p align="right">(<a href="#readme-top">volver al inicio</a>)</p>



<!-- ROADMAP -->
## Roadmap

- [x] pestaña de inventario:
    - [x] tabla con productos con CRUD.
    - [x] muestra de productos mediante categorías.
    - [x] personalización de categorías.
    - [x] cambios en precios en tanda mediante porcentajes.
    - [x] actualización automática en cuentas corrientes cuando hay cambios en los precios de los productos.
- [x] pestaña de ventas:
    - [x] tabla con ventas con CRUD.
    - [x] muestra de ventas por fechas (máximo 6 meses).
    - [x] formulario de ventas para ventas cotidianas.
    - [x] regulación de deudas y redireccionamiento a cuentas corrientes desde el formulario de ventas.
- [x] pestaña de cuentas corrientes:
    - [x] tabla con ventas con CRUD.
    - [x] muestra de productos en cuenta corriente seleccionada con detalles históricos.
- [x] búsqueda y ordenamiento básico en todas las tablas.
- [ ] copias de seguridad de la base de datos automáticas.
- [ ] borrado automático de ventas con más de 5 años (?) de antigüedad.
- [ ] mejorar interactividad en el formulario de ventas permitiendo ingresar el <u>precio de un producto</u> ó <u>su cantidad</u> y llenando el otro campo automáticamente.
- [ ] filtrado en tablas más complejo:
    - [ ] filtrado usando operadores lógicos y matemáticos.
    - [ ] permitir un márgen de error al escribir (distancia de Levenshtein).
    - [ ] reconocimiento de caracteres "similares" usando el módulo "unicodedata".
- [ ] pestaña de análisis estadístico:
    - [ ] mostrar productos más/menos vendidos.
    - [ ] mostrar productos con mayor márgen de ganancia.
    - [ ] mostrar precios de los productos a lo largo del tiempo.
    - [ ] mostrar márgenes de ganancia.
    - [ ] mostrar tendencias de demanda.
    - [ ] mostrar horarios/días con mayor actividad.
    

<p align="right">(<a href="#readme-top">volver al inicio</a>)</p>



<!-- LICENSE -->
## Licencia

Distribuído bajo la licencia "Apache Version 2.0". Ver `LICENSE.txt` para más información.

<p align="right">(<a href="#readme-top">volver al inicio</a>)</p>



<!-- CONTACT -->
## Contacto

Bruno Heit - Brunoh19@hotmail.com

Project Link: [https://github.com/Bruno-Heit/programa-forrajeria](https://github.com/Bruno-Heit/programa-forrajeria)

<p align="right">(<a href="#readme-top">volver al inicio</a>)</p>


<!-- AKNOWLEDGEMENTS -->
## Agradecimientos
* [Best-README-Template](https://github.com/othneildrew/Best-README-Template/tree/main?tab=readme-ov-file)
* [md-badges](https://github.com/inttter/md-badges?tab=readme-ov-file)
* [python-phonenumbers](https://github.com/daviddrysdale/python-phonenumbers?tab=readme-ov-file)
* [Coolors](https://coolors.co/)
* [Wordmark](https://wordmark.it/)
* [Feather Icons](https://feathericons.com/)
* [Google Fonts & Icons](https://fonts.google.com/icons)
* [RegExr](https://regexr.com/)

<p align="right">(<a href="#readme-top">volver al inicio</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[issues-shield]: https://img.shields.io/github/issues/Bruno-Heit/programa-forrajeria.svg?style=for-the-badge
[issues-url]: https://github.com/Bruno-Heit/programa-forrajeria/issues

[license-shield]: https://img.shields.io/github/license/Bruno-Heit/programa-forrajeria.svg?style=for-the-badge
[license-url]: https://github.com/Bruno-Heit/programa-forrajeria/blob/master/LICENSE.txt

[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/Bruno-Heit

[product-screenshot]: images/sct_form_venta_nueva.png

<!-- Shields.io badges. You can a comprehensive list with many more badges at: https://github.com/inttter/md-badges -->
[Python]: https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=fff
[Python-url]: https://www.python.org/

[Qt]: https://img.shields.io/badge/Qt-2CDE85?style=for-the-badge&logo=Qt&logoColor=fff
[Qt-url]: https://www.qt.io/product/framework/

[SQLite]: https://img.shields.io/badge/SQLite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white
[SQLite-url]: https://sqlite.org/

[Numpy]: https://img.shields.io/badge/NumPy-4DABCF?style=for-the-badge&logo=numpy&logoColor=fff
[Numpy-url]: https://numpy.org/

[Css]: https://img.shields.io/badge/CSS-639?style=for-the-badge&logo=css&logoColor=fff
[Css-url]: https://www.w3.org/Style/CSS/Overview.en.html
