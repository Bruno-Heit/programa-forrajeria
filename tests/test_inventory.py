
from PySide6.QtWidgets import QPushButton, QDialogButtonBox, QDialog
from PySide6.QtCore import Qt
from PySide6.QtTest import QTest

from utils.dboperations import (DATABASE_MEMORY_SHARED)
from main import MainWindow
from utils.classes import (ProductDialog)
from utils.enumclasses import (TableViewId)

import pytest
from pytestqt.qtbot import QtBot
import sqlite3
import random
import string

@pytest.fixture
def db_connection():
    conn = sqlite3.connect(DATABASE_MEMORY_SHARED, uri=True)
    cursor = conn.cursor()
    
    cursor.executescript('''-- Categorias
                    CREATE TABLE IF NOT EXISTS Categorias (
                        IDcategoria      INTEGER    PRIMARY KEY AUTOINCREMENT
                                                    NOT NULL,
                        nombre_categoria TEXT (40)  NOT NULL
                                                    UNIQUE ON CONFLICT ROLLBACK,
                        descripcion      TEXT (255) 
                    );
                    
                    -- Productos
                    CREATE TABLE IF NOT EXISTS Productos (
                        IDproducto    INTEGER     PRIMARY KEY AUTOINCREMENT
                                                NOT NULL,
                        nombre        TEXT (50)   NOT NULL
                                                UNIQUE ON CONFLICT FAIL,
                        descripcion   TEXT (256),
                        stock         REAL        NOT NULL,
                        unidad_medida TEXT,
                        precio_unit   REAL        NOT NULL,
                        precio_comerc REAL,
                        IDcategoria   INTEGER     REFERENCES Categorias (IDcategoria) 
                                                NOT NULL,
                        eliminado     INTEGER (1) NOT NULL ON CONFLICT ROLLBACK
                                                DEFAULT (0) 
                    );
                    
                    -- Ventas
                    CREATE TABLE IF NOT EXISTS Ventas (
                        IDventa        INTEGER     PRIMARY KEY AUTOINCREMENT
                                                NOT NULL,
                        fecha_hora     TEXT        NOT NULL,
                        detalles_venta TEXT,
                        eliminado      INTEGER (1) DEFAULT (0) 
                                                NOT NULL ON CONFLICT ROLLBACK
                    );
                    
                    CREATE INDEX IF NOT EXISTS index_ventas_fecha_hora ON Ventas(fecha_hora);
                    
                    -- Deudores
                    CREATE TABLE IF NOT EXISTS Deudores (
                        IDdeudor      INTEGER    PRIMARY KEY AUTOINCREMENT
                                                NOT NULL,
                        nombre        TEXT (40)  NOT NULL,
                        apellido      TEXT (40)  NOT NULL,
                        num_telefono  TEXT,
                        direccion     TEXT (256),
                        codigo_postal TEXT
                    );
                    
                    -- Deudas
                    CREATE TABLE IF NOT EXISTS Deudas (
                        IDdeuda        INTEGER     PRIMARY KEY AUTOINCREMENT
                                                NOT NULL,
                        fecha_hora     TEXT        NOT NULL,
                        total_adeudado REAL        NOT NULL,
                        IDdeudor       INTEGER     REFERENCES Deudores (IDdeudor) 
                                                NOT NULL,
                        eliminado      INTEGER (1) NOT NULL ON CONFLICT ROLLBACK
                                                DEFAULT (0) 
                    );
                    
                    -- Detalle_Ventas
                    CREATE TABLE IF NOT EXISTS Detalle_Ventas (
                        ID_detalle_venta INTEGER     PRIMARY KEY AUTOINCREMENT
                                                    NOT NULL,
                        cantidad         REAL        NOT NULL,
                        costo_total      REAL        NOT NULL,
                        IDproducto       INTEGER     REFERENCES Productos (IDproducto) 
                                                    NOT NULL,
                        IDventa          INTEGER     REFERENCES Ventas (IDventa) 
                                                    NOT NULL,
                        abonado          REAL        NOT NULL,
                        IDdeuda          INTEGER     REFERENCES Deudas (IDdeuda),
                        eliminado        INTEGER (1) NOT NULL ON CONFLICT ROLLBACK
                                                    DEFAULT (0) 
                    );
            '''
    )
    
    conn.commit()
    yield conn
    conn.close()

def test_insert_in_inventory(qtbot:QtBot,
                             db_connection:sqlite3.Connection) -> None:
    mainwindow = MainWindow(db_path=DATABASE_MEMORY_SHARED)
    # insert_button = mainwindow.ui.btn_add_product_inventory
    products:list[str] = []
    dialog:ProductDialog
    inserted_in_model:bool = False
    inserted_in_db:bool = False
    
    # inserta categorías en la base de datos
    categories = __insert_categories_into_db(db_connection)
    
    # insert_button.clicked.disconnect(mainwindow.handleTableCreateRow)
    # insert_button.clicked.connect(__create_dialog)
    
    # obtiene los productos desde el archivo .txt
    with open("tests/test_products.txt", "r") as file:
        products = [line.strip() for line in file if line.strip()]
    
    # crea un producto en bd por cada producto en el archivo .txt
    for product_name in products:
        # simula click sobre el botón que abre el dialog para insertar registros
        # qtbot.mouseClick(insert_button, Qt.MouseButton.LeftButton)
        
        dialog = __create_dialog(
            mainwindow=mainwindow,
            product_name=product_name,
            categories=categories
        )
        ok_button = dialog.productDialog_ui.buttonBox.button(
            QDialogButtonBox.StandardButton.Ok
        )
        
        # confirma datos
        qtbot.mouseClick(ok_button, Qt.MouseButton.LeftButton)
        
        # por último, verifica que se haya ingresado bien
        inserted_in_model = verify_data_insert_in_model(
            mainwindow,
            product_name
        )
        inserted_in_db = verify_data_change_in_db(
            db_connection,
            product_name
        )
        
        assert inserted_in_model and inserted_in_db, "No se insertó el registro correctamente en ambos lados"
    return None

def __create_dialog(mainwindow:MainWindow, product_name:str, 
                    categories:list[str], db_path:str=DATABASE_MEMORY_SHARED) -> None:
    '''
    Crea y retorna una instancia de **ProductDialog** con valores en los 
    campos ya establecidos.

    Parámetros
    ----------
    mainwindow : MainWindow
        *widget* principal del programa
    product_name : str
        nombre del producto actual
    categories : list[str]
        lista con todas las categorías de la base de datos
    db_path : str, opcional
        *path* de la base de datos usada, por defecto *DATABASE_MEMORY_SHARED*

    Retorna
    -------
    ProductDialog
        instancia de *ProductDialog* con los valores en los campos llenados
    '''
    dialog = ProductDialog(db_path)
    dialog.setAttribute(Qt.WA_DeleteOnClose, True)
    
    # todo: crear una subclase de MainWindow con métodos específicos para testear (ej: dataToUpdate() pero para colocarlos en :memory:)
    # conecta señal para actualizar el MODELO de inventario
    dialog.dataFilled.connect(
        lambda data_to_insert: mainwindow.insertDataIntoModel(
            table_viewID=TableViewId.INVEN_TABLE_VIEW,
            data_to_insert=data_to_insert
        )
    )
    dialog.setAttribute(Qt.WidgetAttribute.WA_DontShowOnScreen, True)
        
    # nombre del producto
    dialog.productDialog_ui.lineedit_productName.setText(f"{product_name}")
    # categoría
    dialog.productDialog_ui.cb_productCategory.clear()
    dialog.productDialog_ui.cb_productCategory.addItems(categories)
    dialog.productDialog_ui.cb_productCategory.setCurrentIndex(
        random.randint(0, len(categories) - 1)
    )
    # descripción
    dialog.productDialog_ui.lineedit_productDescription.setText(
        generate_random_string(255)
    )
    # stock
    dialog.productDialog_ui.lineedit_productStock.setText(
        f"{random.uniform(0.00, 99_999_999.99):.2f}"
    )
    # unidad de medida
    dialog.productDialog_ui.lineedit_measurementUnit.setText(
        generate_random_string(20)
    )
    #precio público
    dialog.productDialog_ui.lineedit_productUnitPrice.setText(
        f"{random.uniform(0.00, 99_999_999.99):.2f}"
    )
    # precio comercial
    dialog.productDialog_ui.lineedit_productComercialPrice.setText(
        f"{random.uniform(0.00, 99_999_999.99):.2f}"
    )
    return dialog

def __insert_categories_into_db(db_connection:sqlite3.Connection) -> list[str]:
    '''
    Inserta las categorías del archivo *test_categories.txt* en la base de 
    datos en memoria.
    
    Parámetros
    ----------
    db_connection : sqlite3.Connection
        conexión a la base de datos en memoria en uso
    
    Retorna
    -------
    list[str]
        lista con cada categoría cargada como *str*
    '''
    categories:list[str]
    
    with open("tests/test_categories.txt", "r") as file:
        categories = [category.strip() for category in file if category.strip()]
    
    for category in categories:
        db_connection.execute(
            ''' INSERT INTO Categorias (
                    nombre_categoria,
                    descripcion) 
                VALUES (
                    ?,
                    ?
                )
            ''',
            (category, generate_random_string(length=255))
        )
        db_connection.commit()
    return categories

def generate_random_string(length:int) -> str:
    '''
    Genera un *str* aleatorio del largo indicado.

    Parámetros
    ----------
    length : int
        largo de la cadena de caracteres

    Retorna
    -------
    str
        cadena de caracteres del largo indicado
    '''
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def verify_data_insert_in_model(mainwindow:MainWindow, value:str) -> bool:
    '''
    Verifica que el registro creado se haya agregado al modelo de datos de la 
    tabla indicada.

    Parámetros
    ----------
    mainwindow : MainWindow
        *widget* principal del programa
    value : str
        el valor que buscar en el modelo de datos
    
    Retorna
    -------
    bool
        True si se agregó correctamente, sino False
    '''
    found:bool = False
    
    model = mainwindow.inventory_data_model
    print(f"\033[38;2;120;255;255m{data}\033[0m" for data in model._data)
    for row in range(model.rowCount()):
        prod_name = model.index(row, 1).data()
        if str(prod_name) == value:
            found = True
            break
    assert found, "No se insertó el registro correctamente en el modelo de datos"
    return found

def verify_data_change_in_db(db_connection:sqlite3.Connection, value:str) -> bool:
    '''
    Verifica que el registro creado se haya agregado a la base de datos de la 
    tabla indicada.

    Parámetros
    ----------
    db_connection : sqlite3.Connection
        conexión a la base de datos en memoria en uso
    value : str
        el valor que buscar en la base de datos
    
    Retorna
    -------
    bool
        True si se agregó correctamente, sino False
    '''
    found:bool = False
    
    res = db_connection.execute(
        ''' SELECT nombre 
            FROM Productos 
            WHERE nombre = ?;''',
        (value,)
    ).fetchall()
    if len(res) != 0:
        found = True
    assert found, "No se insertó el registro correctamente en la base de datos"
    return found
