# Importar desde mysqlconnections
import sys
import os

# Agregar la ruta padre al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.mysqlconnections import MySQLConnection, connectToMySQL

__all__ = ['MySQLConnection', 'connectToMySQL']
