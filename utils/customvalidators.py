"""
En este archivo se encuentran los QValidators -y sus variantes- que he tenido que modificar
para poder lograr una mejor validación de datos en QComboBoxes, QLineEdits, QDateTimeEdits y
demás widgets donde el usuario pueda ingresar datos.
"""

from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Signal, QLocale, QObject
from PySide6.QtGui import (
    QValidator,
    QRegularExpressionValidator,
    QIntValidator,
    QDoubleValidator,
)

from utils.dboperations import (
    makeReadQuery,
    DatabaseRepository,
    DATABASE_DIR,
    DATABASE_MEMORY_SHARED,
)
from utils.enumclasses import Regex, CommonCategories

from re import fullmatch, compile, Pattern, IGNORECASE
import logging


# ¡ search bars ========================================================================================
class SearchBarValidator(QValidator):
    """Validador para las barras de búsquedas. A diferencia de otros validadores, este no emite señales."""

    def __init__(self, parent=None):
        super(SearchBarValidator, self).__init__()
        self.pattern: Pattern = compile(
            Regex.GENERIC_CHARS_TO_AVOID.value, flags=IGNORECASE
        )

    def validate(self, text: str, pos: int) -> object:
        if text.strip() == "":  # si el campo está vacío devuelve Acceptable
            return self.State.Acceptable, text, pos

        elif fullmatch(self.pattern, text):  # si coincide el patrón devuelve Acceptable
            return self.State.Acceptable, text, pos

        else:  # en cualquier otro caso devuelve Invalid
            return self.State.Invalid, text, pos


# ¡ tabla INVENTARIO ===================================================================================
class ProductNameValidator(QValidator):
    """Validador para los campos donde el usuario pueda modificar el nombre de un producto."""

    validationSucceeded = Signal()  # se emite cuando el estado es 'Acceptable'. Sirve para esconder el label con feedback
    validationFailed = Signal(
        str
    )  # se emite cuando el estado es 'Invalid', envía un str con feedback para mostrar

    def __init__(self, prev_name: str, db_path: str = DATABASE_DIR):
        """
        Inicializa un validador para los nombres de productos.

        Parámetros
        ----------
        prev_name : str
            el nombre del producto anterior del campo
        db_path : str, opcional
            el *path* de la base de datos utilizada, por defecto DATABASE_DIR
        """
        super(ProductNameValidator, self).__init__()
        self.pattern: Pattern = compile(Regex.PROD_NAME.value, flags=IGNORECASE)
        self.prev_name: str = prev_name
        self._db_path: str = db_path

    def validate(self, text: str, pos: int) -> object:
        names: list = []

        # ? no quiero validar cuando el nombre sea el mismo que el que estaba antes
        if text != self.prev_name:
            # lista para verificar si el nombre existe en la base de datos
            with DatabaseRepository(self._db_path) as db_repo:
                names = db_repo.selectRegisters(
                    data_sql="""SELECT nombre 
                                FROM Productos 
                                WHERE nombre = ?;""",
                    data_params=(text,),
                )
                names = [name[0] for name in names] if names else names

            # si el nombre ya existe devuelve Intermediate
            if text in names:
                self.validationFailed.emit("El nombre del producto ya existe")
                return QValidator.State.Intermediate, text, pos

            # si el campo está vacío devuelve Intermediate
            elif text.strip() == "":
                self.validationFailed.emit(
                    "El campo del nombre del producto no puede estar vacío"
                )
                return QValidator.State.Intermediate, text, pos

            # # si coincide el patrón devuelve Acceptable
            elif fullmatch(self.pattern, text):
                self.validationSucceeded.emit()
                return QValidator.State.Acceptable, text, pos

            # en cualquier otro caso devuelve Invalid
            else:
                self.validationFailed.emit("El nombre del producto es inválido")
                return QValidator.State.Invalid, text, pos
        return self.State.Acceptable, text, pos


class ProductStockValidator(QRegularExpressionValidator):
    """Validador para los campos donde el usuario pueda modificar el stock y
    la unidad de medida de un producto. Si no se especifica el 'pattern' se
    asigna automáticamente el valor de 'enumclasses.Regex.PROD_STOCK_FULL'.

    Parámetros
    ----------
    pattern: re.Pattern | str, opcional
        Patrón de expresión regular para validar el stock; por defecto es None
    """

    validationSucceeded = Signal()
    validationFailed = Signal(str)

    def __init__(self, pattern: Pattern | str = None, parent=None):
        super(ProductStockValidator, self).__init__()
        if not pattern:
            self.pattern: Pattern = compile(Regex.PROD_STOCK_FULL.value, IGNORECASE)
        else:
            self.pattern: Pattern = compile(pattern, IGNORECASE)

    def validate(self, text: str, pos: int) -> object:
        if text.strip() == "":
            self.validationFailed.emit("El campo de stock no puede estar vacío")
            return QRegularExpressionValidator.State.Intermediate, text, pos

        elif fullmatch(self.pattern, text):
            self.validationSucceeded.emit()
            return QRegularExpressionValidator.State.Acceptable, text, pos

        elif text.split(" ")[0].endswith((".", ",")):  # llama automáticamente a fixup()
            return QRegularExpressionValidator.State.Invalid, text, pos

        else:
            self.validationFailed.emit("El stock del producto es inválido")
            return QRegularExpressionValidator.State.Invalid, text, pos


class ProductUnitPriceValidator(QRegularExpressionValidator):
    """Validador para los campos donde el usuario pueda modificar el precio unitario de un producto."""

    validationSucceeded = Signal()
    validationFailed = Signal(str)

    def __init__(self, parent=None):
        super(ProductUnitPriceValidator, self).__init__()
        self.pattern: Pattern = compile(Regex.PROD_UNIT_PRICE.value)

    def validate(self, text: str, pos: int) -> object:
        if text == "":
            self.validationFailed.emit(
                "El campo de precio unitario no puede estar vacío"
            )
            return QRegularExpressionValidator.State.Intermediate, text, pos

        elif fullmatch(self.pattern, text):
            self.validationSucceeded.emit()
            return QRegularExpressionValidator.State.Acceptable, text, pos

        elif text.endswith((",", ".")):  # llama automáticamente a fixup()
            return QRegularExpressionValidator.State.Invalid, text, pos

        else:
            self.validationFailed.emit("El precio unitario es inválido")
            return QRegularExpressionValidator.State.Invalid, text, pos


class ProductComercPriceValidator(QRegularExpressionValidator):
    """Validador para los campos donde el usuario pueda modificar el precio comercial de un producto."""

    validationSucceeded = Signal()
    validationFailed = Signal(str)

    def __init__(self, parent=None):
        super(ProductComercPriceValidator, self).__init__()
        self.pattern: Pattern = compile(Regex.PROD_COMERC_PRICE.value)

    def validate(self, text: str, pos: int) -> object:
        if text.strip() == "":
            self.validationSucceeded.emit()
            return QRegularExpressionValidator.State.Acceptable, text, pos

        elif fullmatch(self.pattern, text):
            self.validationSucceeded.emit()
            return QRegularExpressionValidator.State.Acceptable, text, pos

        elif text.endswith((",", ".")):  # llama automáticamente a fixup()
            return QRegularExpressionValidator.State.Invalid, text, pos

        else:
            self.validationFailed.emit("El precio comercial es inválido")
            return QRegularExpressionValidator.State.Invalid, text, pos


class PercentageValidator(QRegularExpressionValidator):
    """Validador para el campo de cambio de precios de productos mediante porcentajes."""

    validationSucceeded = Signal()
    validationFailed = Signal(str)

    def __init__(self, parent=None) -> None:
        super(PercentageValidator, self).__init__()
        self.pattern: Pattern = compile(Regex.PERCENTAGE_CHANGE.value)

    def validate(self, text: str, pos: int) -> object:
        if text.strip() == "":
            self.validationFailed.emit("Se debe ingresar un porcentaje")
            return self.State.Intermediate, text, pos

        elif fullmatch(self.pattern, text):
            try:
                if float(text.replace(",", ".")) < -100:
                    self.validationFailed.emit("El valor no puede ser menor a -100%")
                    return self.State.Invalid, text, pos
            except ValueError:
                pass
            self.validationSucceeded.emit()
            return self.State.Acceptable, text, pos

        else:
            self.validationFailed.emit("El porcentaje es inválido")
            return self.State.Invalid, text, pos


# ¡ tabla CATEGORÍAS ==============================================================================
class CategoryNameValidator(QRegularExpressionValidator):
    """Validador para los campos donde el usuario pueda modificar el nombre de
    una categoría."""

    validationSucceeded = Signal()
    validationFailed = Signal(str)
    isEmpty = Signal()

    def __init__(self, parent: QWidget = None, prev_name: str = None):
        """
        Valida el campo del nombre de la categoría.

        Parámetros
        ----------
        parent : QWidget, opcional
            el widget padre, por defecto None
        prev_name : bool, opcional
            el nombre anterior de la categoría, por defecto None; se usa
            cuando el nombre está siendo modificado
        """
        super(CategoryNameValidator, self).__init__()
        self.pattern: Pattern = compile(Regex.CATEGORY_NAME.value, flags=IGNORECASE)
        self.__prev_name: str = prev_name

    def prevName(self) -> str:
        """
        Devuelve el nombre de categoría anterior.

        Retorna
        -------
        str
            el nombre de categoría anterior como *str*, incluso si no hay un
            nombre anterior declarado y se esté creando una nueva categoría,
            en ese caso será una cadena con valor ***None***
        """
        return str(self.__prev_name)

    def nameExists(self, name: str) -> bool:
        """
        Verifica si el nombre existe en la base de datos
        """
        return makeReadQuery(
            sql="""SELECT EXISTS (
                        SELECT 1 
                        FROM Categorias 
                        WHERE nombre_categoria = ?
                        COLLATE NOCASE
                    );""",
            params=(name,),
        )[0][0]

    def validate(self, text: str, pos: int) -> object:
        # ? si el nombre es igual al anterior no valida, lo considera válido
        if text.strip().upper() != self.prevName().upper():
            # verifica si el nombre existe
            name_exists: bool = makeReadQuery(
                sql="""SELECT EXISTS (
                            SELECT 1 
                            FROM Categorias 
                            WHERE nombre_categoria = ?
                            COLLATE NOCASE
                        );""",
                params=(text.strip(),),
            )[0][0]

            # si el nombre ya existe devuelve Intermediate
            if name_exists or text.strip().upper() == CommonCategories.SHOW_ALL.value:
                self.validationFailed.emit("El nombre de la categoría ya existe")
                return QValidator.State.Intermediate, text, pos

            # si el campo está vacío devuelve Intermediate
            elif text.strip() == "":
                self.isEmpty.emit()
                return QValidator.State.Acceptable, text, pos

            # # si coincide el patrón devuelve Acceptable
            elif fullmatch(self.pattern, text):
                self.validationSucceeded.emit()
                return QValidator.State.Acceptable, text, pos

            # en cualquier otro caso devuelve Invalid
            else:
                self.validationFailed.emit("El nombre de la categoría es inválida")
                return QValidator.State.Invalid, text, pos

        else:
            self.validationSucceeded.emit()
            return QValidator.State.Acceptable, text, pos


class CategoryDescValidator(QRegularExpressionValidator):
    """Validador para los campos donde el usuario pueda modificar la
    descripción de una categoría."""

    def __init__(self, MAX_LENGTH: int, parent: QWidget = None):
        super(CategoryDescValidator, self).__init__()
        self.pattern: Pattern = compile(Regex.CATEGORY_DESC.value, flags=IGNORECASE)
        self._MAX_LENGTH: int = MAX_LENGTH

    def validate(self, text: str, pos: int) -> object:
        if len(text) > self._MAX_LENGTH:
            return QRegularExpressionValidator.State.Invalid, text, pos

        if not fullmatch(self.pattern, text):
            return QRegularExpressionValidator.State.Invalid, text, pos

        else:
            return QRegularExpressionValidator.State.Acceptable, text, pos


# ¡ tabla VENTAS ===================================================================================
class SaleDetailsValidator(QRegularExpressionValidator):
    """Validador para los campos donde el usuario pueda modificar los detalles de una venta."""

    validationSucceeded = Signal()
    validationFailed = Signal(str)

    def __init__(self, parent=None):
        super(SaleDetailsValidator, self).__init__()
        self.pattern: Pattern = compile(Regex.SALES_DETAILS_EDITION.value)

    def validate(self, text: str, pos: int) -> object:
        if text.strip() == "" or fullmatch(self.pattern, text):
            self.validationSucceeded.emit()
            return QRegularExpressionValidator.State.Acceptable, text, pos

        else:
            self.validationFailed.emit(
                "El campo de detalle de venta no admite ese caracter"
            )
            return QRegularExpressionValidator.State.Invalid, text, pos


class SaleQuantityValidator(QRegularExpressionValidator):
    """Validador para los campos donde el usuario pueda modificar la cantidad de un producto."""

    validationSucceeded = Signal()
    validationFailed = Signal(str)

    def __init__(self, parent=None):
        super(SaleQuantityValidator, self).__init__()
        self.AVAILABLE_STOCK: tuple[float, str] = None
        self.pattern: Pattern = compile(Regex.SALES_QUANTITY.value)

    def setAvailableStock(self, stock: tuple[float, str]) -> None:
        """
        Coloca el valor de 'stock' en 'self.AVAILABLE_STOCK'.

        Parámetros
        ----------
        stock : tuple[float, str]
            la cantidad en stock del producto como float y la unidad de medida
            como str

        Retorna
        -------
        None
        """
        self.AVAILABLE_STOCK = stock
        return None

    def getAvailableStock(self) -> tuple[float, str] | None:
        """
        Devuelve el stock disponible.

        Retorna
        -------
        tuple[float, str] | None
            si hay un stock guardado en el validador devuelve una
            tupla[cantidad, unidad de medida], sino None
        """
        if self.AVAILABLE_STOCK:
            return self.AVAILABLE_STOCK
        return None

    def fixup(self, text: str) -> str:
        while text.split(" ")[0].endswith((".", ",")):
            text = text.rstrip(",")
            text = text.rstrip(".")
        return super().fixup(text)

    def validate(self, text: str, pos: int) -> object:
        _text_to_float: float

        if text.strip() == "":
            self.validationFailed.emit("La cantidad no puede estar vacía")
            return QRegularExpressionValidator.State.Intermediate, text, pos

        elif fullmatch(self.pattern, text):
            # si el stock disponible existe
            if self.AVAILABLE_STOCK:
                try:
                    _text_to_float = float(text.replace(",", "."))

                    # si la cantidad es 0 o cualquier valor nulo devuelve Invalid
                    if not _text_to_float:
                        self.validationFailed.emit(f"La cantidad debe ser mayor a 0")
                        return QRegularExpressionValidator.State.Invalid, text, pos

                    # si el stock es menor que la cantidad introducida devuelve Invalid
                    elif _text_to_float > self.AVAILABLE_STOCK[0]:
                        self.validationFailed.emit(
                            f"Cantidad mayor al stock (stock: {self.AVAILABLE_STOCK[0]} {self.AVAILABLE_STOCK[1]})"
                        )
                        return QRegularExpressionValidator.State.Invalid, text, pos

                except TypeError as err:
                    logging.error(err)
                    return QRegularExpressionValidator.State.Invalid, text, pos

            self.validationSucceeded.emit()
            return QRegularExpressionValidator.State.Acceptable, text, pos

        elif text.split(
            " "
        )[
            0
        ].endswith(
            (".", ",")
        ):  # si pasa, automáticamente llama a 'fixup' y lo corrige, y el programa sigue como si nada...
            return QRegularExpressionValidator.State.Invalid, text, pos

        else:
            self.validationFailed.emit("La cantidad es inválida")
            return QRegularExpressionValidator.State.Invalid, text, pos


class SaleTotalCostValidator(QRegularExpressionValidator):
    """Validador para los campos donde el usuario pueda modificar el costo total de un producto."""

    validationSucceeded = Signal()
    validationFailed = Signal(str)

    def __init__(self, parent=None):
        super(SaleTotalCostValidator, self).__init__()
        self.pattern: Pattern = compile(Regex.SALES_TOTAL_COST.value)

    def fixup(self, text: str) -> str:
        while text.endswith((".", ",")):
            text = text.rstrip(",")
            text = text.rstrip(".")
        return super().fixup(text)

    def validate(self, text: str, pos: int) -> object:
        if text.strip() == "":
            self.validationFailed.emit("El campo de costo total no puede estar vacío")
            return QRegularExpressionValidator.State.Intermediate, text, pos

        elif fullmatch(self.pattern, text):
            self.validationSucceeded.emit()
            return QRegularExpressionValidator.State.Acceptable, text, pos

        elif text.endswith(
            (".", ",")
        ):  # si pasa, automáticamente llama a 'fixup' y lo corrige, y el programa sigue como si nada...
            return QRegularExpressionValidator.State.Invalid, text, pos

        else:
            self.validationFailed.emit("El costo total es inválido")
            return QRegularExpressionValidator.State.Invalid, text, pos


class SalePaidValidator(QValidator):
    """Validador para los campos donde el usuario pueda modificar la cantidad paga de un producto."""

    validationSucceeded = Signal()
    validationFailed = Signal(str)

    def __init__(self, parent=None, is_optional: bool = False):
        super(SalePaidValidator, self).__init__()
        self.is_optional = is_optional
        self.pattern: Pattern = compile(Regex.SALES_PAID.value)

    def validate(self, text: str, pos: int) -> object:
        if (
            self.is_optional and text == ""
        ):  # si el campo es opcional y está vacío emite Acceptable
            self.validationSucceeded.emit()
            return QValidator.State.Acceptable, text, pos

        elif (
            not self.is_optional and text == ""
        ):  # si el campo es obligatorio y está vacío emite Itermediate
            self.validationFailed.emit(
                "El campo del total abonado no puede estar vacío"
            )
            return QValidator.State.Intermediate, text, pos

        elif fullmatch(self.pattern, text):
            self.validationSucceeded.emit()
            return QIntValidator.State.Acceptable, text, pos

        else:
            self.validationFailed.emit("El valor abonado es inválido")
            return QValidator.State.Invalid, text, pos


# ¡ tabla VENTAS/CUENTA CORRIENTE ===================================================================================
class DebtorNameValidator(QRegularExpressionValidator):
    """Validador para los campos donde el usuario pueda modificar el nombre de una persona en cuenta corriente."""

    validationSucceeded = Signal()
    validationFailed = Signal(str)

    def __init__(self, parent=None):
        super(DebtorNameValidator, self).__init__()
        self.pattern: Pattern = compile(Regex.DEBTS_NAME.value)

    def validate(self, text: str, pos: int) -> object:
        if text.strip() == "":
            self.validationFailed.emit("El nombre no puede estar vacío")
            return QRegularExpressionValidator.State.Intermediate, text, pos

        elif fullmatch(self.pattern, text):
            self.validationSucceeded.emit()
            return QRegularExpressionValidator.State.Acceptable, text, pos

        else:
            self.validationFailed.emit("El nombre es inválido")
            return QRegularExpressionValidator.State.Invalid, text, pos


class DebtorSurnameValidator(QRegularExpressionValidator):
    """Validador para los campos donde el usuario pueda modificar el apellido de una persona en cuenta corriente."""

    validationSucceeded = Signal()
    validationFailed = Signal(str)

    def __init__(self, parent=None):
        super(DebtorSurnameValidator, self).__init__()
        self.pattern: Pattern = compile(Regex.DEBTS_SURNAME.value)

    def validate(self, text: str, pos: int) -> object:
        if text.strip() == "":
            self.validationFailed.emit("El apellido no puede estar vacío")
            return QRegularExpressionValidator.State.Intermediate, text, pos

        elif fullmatch(self.pattern, text):
            self.validationSucceeded.emit()
            return QRegularExpressionValidator.State.Acceptable, text, pos

        else:
            self.validationFailed.emit("El apellido es inválido")
            return QRegularExpressionValidator.State.Invalid, text, pos


class DebtorPhoneNumberValidator(QRegularExpressionValidator):
    """Validador para los campos donde el usuario pueda modificar el número de
    teléfono de una persona en cuenta corriente."""

    validationSucceeded = Signal()
    validationFailed = Signal(str)

    def __init__(self, parent=None):
        super(DebtorPhoneNumberValidator, self).__init__()
        self.pattern: Pattern = compile(Regex.DEBTS_PHONE_NUMB.value)

    def validate(self, text: str, pos: int) -> object:
        if text.strip() == "":  # si el texto está vacío devuelve Acceptable
            self.validationSucceeded.emit()
            return QRegularExpressionValidator.State.Acceptable, text, pos

        elif fullmatch(self.pattern, text):
            self.validationSucceeded.emit()
            return QRegularExpressionValidator.State.Acceptable, text, pos

        else:
            self.validationFailed.emit("El número de teléfono es inválido")
            return QRegularExpressionValidator.State.Invalid, text, pos


class DebtorDirectionValidator(QRegularExpressionValidator):
    """Validador para los campos donde el usuario pueda modificar la dirección
    de una persona en cuenta corriente."""

    validationSucceeded = Signal()
    validationFailed = Signal(str)

    def __init__(self, parent=None):
        super(DebtorDirectionValidator, self).__init__()
        self.pattern: Pattern = compile(Regex.DEBTS_DIRECTION.value)

    def validate(self, text: str, pos: int) -> object:
        if text.strip() == "":  # si el texto está vacío devuelve Acceptable
            self.validationSucceeded.emit()
            return QRegularExpressionValidator.State.Acceptable, text, pos

        elif fullmatch(self.pattern, text):
            self.validationSucceeded.emit()
            return QRegularExpressionValidator.State.Acceptable, text, pos

        else:
            self.validationFailed.emit("La dirección es inválida")
            return QRegularExpressionValidator.State.Invalid, text, pos


class DebtorPostalCodeValidator(QIntValidator):
    validationSucceeded = Signal()
    validationFailed = Signal(str)

    def __init__(self, parent=None):
        super(DebtorPostalCodeValidator, self).__init__()
        self.setRange(1, 9_999)
        self.setLocale(QLocale(QLocale.Language.Spanish, QLocale.Country.Argentina))

    def validate(self, text: str, pos: int) -> object:
        if text.strip() == "":  # si el texto está vacío devuelve Acceptable
            self.validationSucceeded.emit()
            return QIntValidator.State.Acceptable, text, pos

        elif text.isnumeric() and (self.bottom() <= int(text) <= self.top()):
            self.validationSucceeded.emit()
            return QIntValidator.State.Acceptable, text, pos

        elif text.isalnum():
            self.validationFailed.emit(
                "El código postal sólo admite números entre [1, 9.999]"
            )
            return QIntValidator.State.Invalid, text, pos

        else:
            self.validationFailed.emit("El código postal es inválido")
            return QIntValidator.State.Invalid, text, pos


# ¡ tabla PRODUCTOS ADEUDADOS =======================================================================================
class ProductBalanceValidator(QRegularExpressionValidator):
    """Validador para los campos donde el usuario pueda modificar el balance de un producto."""

    validationSucceeded = Signal()
    validationFailed = Signal()

    def __init__(self, parent=None):
        super(ProductBalanceValidator, self).__init__()
        self.pattern: Pattern = compile(Regex.PRODS_BAL_BALANCE.value, IGNORECASE)

    def validate(self, text: str, pos: int) -> object:
        if text.strip() == "":
            return self.State.Intermediate, text, pos

        elif fullmatch(self.pattern, text):
            return self.State.Acceptable, text, pos

        else:
            return self.State.Invalid, text, pos


class ProductReduceDebtValidator(QRegularExpressionValidator):
    """Validador para los campos donde el usuario pueda modificar el balance de un producto."""

    isEmpty: Signal = Signal()

    def __init__(self, parent=None):
        super(ProductReduceDebtValidator, self).__init__()
        self.pattern: Pattern = compile(Regex.SALES_PAID.value, IGNORECASE)

    def validate(self, text: str, pos: int) -> object:
        if text.strip() == "":
            self.isEmpty.emit()
            return self.State.Intermediate, text, pos

        elif fullmatch(self.pattern, text):
            return self.State.Acceptable, text, pos

        else:
            return self.State.Invalid, text, pos
