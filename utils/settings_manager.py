'''
    En éste archivo se encuentran las funciones, variables y clases usadas 
    como configuraciones de la aplicación.
'''
from PySide6.QtCore import (QSettings, QObject, QSize, QPoint, QByteArray)

from utils.enumclasses import (ProgramValues as PV, SettingsDirs)

from typing import Any


# TODO: mover las direcciones de bases de datos acá
class SettingsManager(QObject):
    '''
    Clase *singleton* usada para llevar a cabo las actualizaciones en 
    configuraciones del programa.
    '''
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(SettingsManager, cls).__new__(cls)
            cls._instance.settings = QSettings(
                PV.APP_NAME.value,
                PV.APP_AUTHOR.value
            )
        return cls._instance
    
    def __init__(self, app_name:str=PV.APP_NAME.value, 
                 organization_name:str=PV.APP_AUTHOR.value) -> None:
        '''
        Instancia un objeto de tipo **SettingsManager** para llevar a cabo las 
        actualizaciones de las configuraciones y valores constantes de la 
        aplicación.

        Parameters
        ----------
        app_name : str, opcional
            nombre de la aplicación, por defecto *PV.APP_NAME.value*
        organization_name : str, opcional
            nombre de la organización, por defecto *PV.APP_AUTHOR.value*
        '''
        super(SettingsManager, self).__init__()
        
        self.settings:QSettings = QSettings(app_name, organization_name)
        return None
    
    def saveMainWindowGeometry(self, size:QSize, position:QPoint) -> None:
        '''
        Guarda el tamaño y la posición en pantalla de la ventana principal.

        Parámetros
        ----------
        size : QSize
            tamaño de la ventana principal
        position : QPoint
            posición de la ventana principal
        '''
        self.settings.setValue(SettingsDirs.MW_SIZE.value, size)
        self.settings.setValue(SettingsDirs.MW_POSITION.value, position)
        return None
    
    def getMainWindowGeometry(self) -> tuple[QSize, QPoint]:
        '''
        Devuelve el tamaño y la posición en pantalla guardados de la ventana 
        principal.

        Retorna
        -------
        tuple[QSize, QPoint]
            tupla con el tamaño y la posición de la ventana principal
        '''
        return (
            self.settings.value(SettingsDirs.MW_SIZE.value, QSize(1160, 605)),
            self.settings.value(SettingsDirs.MW_POSITION.value, QPoint(200, 200))
            )
    
    # estado expandido de la ventana
    def saveMainWindowState(self, geometry_bytes:QByteArray,
                            state_bytes:QByteArray) -> None:
        '''
        Guarda la geometría de la ventana principal y el estado en el que se 
        encuentra.

        Parámetros
        ----------
        geometry_bytes : QByteArray
            geometría de la ventana principal
        state_bytes : QByteArray
            el estado de los *toolbars*, *dockwidgets* y las esquinas de la 
            ventana principal
        '''
        self.settings.setValue(SettingsDirs.MW_GEOMETRY.value, geometry_bytes)
        self.settings.setValue(SettingsDirs.MW_STATE.value, state_bytes)
        return None
    
    def getMainWindowState(self) -> tuple[QByteArray, QByteArray]:
        '''
        Devuelve la geometría de la ventana principal y el estado en el que se 
        encontraba.

        Retorna
        -------
        tuple[QByteArray, QByteArray]
            tupla con la geometría como primer valor y el estado de los 
            *toolbars*, *dockwidgets* y esquinas de la ventana principal
        '''
        return (
            self.settings.value(SettingsDirs.MW_GEOMETRY.value, None),
            self.settings.value(SettingsDirs.MW_STATE.value, None)
        )
    
    # métodos genéricos
    def setValue(self, key:str, value:Any) -> None:
        '''
        Guarda el valor especificado en la clave (*key*) especificada.

        Parámetros
        ----------
        key : str
            la clave en la que se guarda el valor
        value : Any
            el valor que guardar
        '''
        self.settings.setValue(key, value)
        return None

    def getValue(self, key:str, default:Any=None, type_hint:str=str) -> Any:
        '''
        Devuelve el valor especificado a partir de la clave especificada.

        Parámetros
        ----------
        key : str
            la clave en la que se guarda el valor
        default : Any, opcional
            valor por defecto que devolverá el método si no encuentra el valor, 
            por defecto ***None***
        type_hint : str, opcional
            tipo de dato a buscar, por defecto ***str***
        '''
        return self.settings.value(key, defaultValue=default, type=type_hint)

    # exportar / importar configuraciones
    def getAllConfigs(self) -> dict[str, Any]:
        '''
        Devuelve todas las configuraciones como un diccionario.

        Retorna
        -------
        dict
            diccionario con las configuraciones
        '''
        config:dict = {}
        
        for key in self.settings.allKeys():
            config[key] = self.settings.value(key)
        return config

    def overwriteAllConfigs(self, config_dict:dict[str, Any]) -> None:
        '''
        Sobreescribe todas las configuraciones con las del diccionario 
        especificado.

        Parámetros
        ----------
        config_dict : dict[str, Any]
            diccionario con todas las configuraciones nuevas
        '''
        for key, value in config_dict.items():
            self.settings.setValue(key, value)
        return None
    
    def deleteAllConfigs(self) -> None:
        '''
        Borra todas las configuraciones guardadas.
        '''
        self.settings.clear()
        return None
