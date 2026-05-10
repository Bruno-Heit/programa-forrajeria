
from pathlib import Path
import logging
import pandas as pd
from re import (Pattern, match, Match, fullmatch, compile, sub, IGNORECASE)
from utils.enumclasses import Regex, LogAnalyzerRegex as laregex

# alias
CountResult = dict[str, tuple | int] # { "indexes": tuple(idx_1, idx_2, ..., idx_n),
                                     #   "count": len(indexes) }
Log = dict[str, CountResult] # {"nivel": CountResult}


class LogAnalyzer():
    """
    Clase analizadora de logs. Contiene métodos para contar la cantidad de 
    logs que hubo según su tipo.
    Los resultados obtenidos son guardados en un archivo *log_analysis.log* en 
    la carpeta *logs*.
    """
    def __init__(self):
        self._log_file:Path = Path("program.log")
        self._analysis_dir:Path = Path("logs")
        self._analysis_file:Path = Path(
            f"{self._analysis_dir}\{self.__rotate_analysis_log()}"
        )
        
        self._pattern:Pattern = compile(
            laregex.MATCH_DAY.value +
            laregex.MATCH_DATE.value +
            laregex.MATCH_TIME.value +
            laregex.MATCH_LEVEL.value +
            laregex.MATCH_FUNC_NAME.value +
            laregex.MATCH_MSG.value,
            flags=IGNORECASE
        )
        
        self.create_log_analysis_file()
        return None
    
    def __rotate_analysis_log(self) -> str:
        """
        Rota secuencialmente el número del log actual para que haya hasta 7 
        logs distintos.
        
        Retorna
        -------
        str
            el *nombre de archivo completo con el número cambiado* que 
            tendrá el archivo *log_analysis* actual en base al número que 
            tienen los otros logs de análisis
        """
        LOGS_LIMIT:int = 7 # no quiero más de 7 logs (aunque podría tener más)
        logs_count:int = len(
            [f for f in self._analysis_dir.iterdir() if f.is_file()]
        )
        current_log_n:int = 1
        
        print(logs_count)
        # log1
        # log2
        # log3
        # log4
        # log5
        # log6
        # log7
        
        if logs_count < LOGS_LIMIT:
            current_log_n = logs_count + 1
        else:
            current_log_n = 1
        return f"log_analysis{current_log_n}.log"
    
    def create_log_analysis_file(self) -> None:
        """
        Crea/reinicia el archivo *log_analysis.log*.
        """
        try:
            with self._analysis_file.open(mode="w"):
                logging.info(f"archivo '{self._analysis_file.name}' creado exitosamente")
        
        except Exception as e:
            logging.error(e)
        return None
    
    def start_analysis(self) -> None:
        """
        Realiza el análisis de los mensajes en el archivo *program.log* y 
        escribe el archivo *log_analysis.log* correspondiente.
        """
        logs:list[dict] = []
        
        with open(self._log_file, "r") as file:
            for line in file:
                parsed_line = self.parse_log_line(line.strip())
                if parsed_line:
                    logs.append(parsed_line)
        
        self.write_log_analysis_file(data=logs)
        return None
    
    def parse_log_line(self, line:str) -> dict|None:
        """
        Parsea la línea actual como un diccionario.
        
        Parámetros
        ----------
        line : str
            la línea actual como *string* a formatear
        
        Retorna
        -------
        dict
            la línea actual seccionada como valores de un diccionario
        """
        match = self._pattern.match(line)
        if not match:
            return None
        
        data = match.groupdict()
        return data

    def write_log_analysis_file(self, data:list[dict]) -> None:
        """
        Escribe las líneas parseadas en el archivo *log_analysis.log* actual.
        
        Parámetros
        ----------
        data : list[dict]
            lista con cada línea del *program.log* parseada en forma de 
            dicccionario
        """
        try:
            with open(self._analysis_file, "w+") as file:
                file.writelines([line for line in data])
            logging.info(f"archivo '{self._analysis_file.name}' escrito exitosamente")
        
        except Exception as e:
            logging.error(e)
        return None


