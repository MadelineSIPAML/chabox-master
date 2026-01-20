# Importamos la librería pymysql para interactuar con MySQL
import pymysql.cursors
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Esta clase proporciona una instancia para conectarse a la base de datos MySQL
class MySQLConnection:
    """Clase para gestionar conexiones a base de datos MySQL"""
    
    def __init__(self, db):
        """
        Método constructor que recibe el nombre de la base de datos como parámetro
        
        Args:
            db (str): Nombre de la base de datos
        """
        # Configuración de la conexión desde variables de entorno
        self.host = os.getenv('DB_HOST', 'localhost')
        self.port = int(os.getenv('DB_PORT', 3306))
        self.user = os.getenv('DB_USER', 'root')
        self.password = os.getenv('DB_PASSWORD', 'root')
        self.database = db
        
        # Establecer conexión
        try:
            self.connection = pymysql.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                db=self.database,
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor,
                autocommit=True
            )
            print(f"✅ Conectado a MySQL - Base de datos: {self.database}")
        except pymysql.Error as err:
            print(f"❌ Error de conexión a MySQL: {err}")
            raise

    def query_db(self, query, data=None):
        """
        Método para ejecutar consultas SQL en la base de datos
        
        Args:
            query (str): Consulta SQL
            data (tuple/list, optional): Datos para consultas parametrizadas
            
        Returns:
            - Para INSERT: ID de la última fila insertada
            - Para SELECT: Lista de diccionarios con los resultados
            - Para UPDATE/DELETE: None si fue exitoso, False si hubo error
        """
        with self.connection.cursor() as cursor:
            try:
                # Si deseas depurar, imprime la consulta
                if data:
                    print(f"🔍 Query: {query}")
                    print(f"📊 Data: {data}")

                # Ejecutar la consulta
                cursor.execute(query, data)

                # Si la consulta es un INSERT, devolver el ID de la última fila
                if query.lower().find("insert") >= 0:
                    self.connection.commit()
                    return cursor.lastrowid

                # Si es una consulta SELECT, devolver el resultado
                elif query.lower().find("select") >= 0:
                    result = cursor.fetchall()
                    return result if result else []

                # Para consultas UPDATE o DELETE, confirmar la transacción
                else:
                    self.connection.commit()
                    return True
                    
            except pymysql.Error as err:
                print(f"❌ Error en query MySQL: {err}")
                return False
            except Exception as e:
                print(f"❌ Error inesperado: {e}")
                return False

    def close(self):
        """Cerrar la conexión a MySQL"""
        try:
            if self.connection:
                self.connection.close()
                print("✅ Conexión cerrada")
        except Exception as e:
            print(f"Error al cerrar conexión: {e}")

def connectToMySQL(db):
    """
    Función para crear una instancia de MySQLConnection
    
    Args:
        db (str): Nombre de la base de datos
        
    Returns:
        MySQLConnection: Instancia de la clase MySQLConnection
    """
    return MySQLConnection(db)
