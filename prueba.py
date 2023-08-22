import speedtest, socket, subprocess, os
import logging
from dotenv import load_dotenv
from datetime import datetime
from ping3 import ping, verbose_ping
from pymongo import MongoClient
from pymongo.errors import PyMongoError, ConnectionFailure

# carga de variables de entorno
load_dotenv()

db_host = os.getenv('DB_HOST')
db_user = os.getenv('DB_USER')
db_pass = os.getenv('DB_PASSWD')

# formato normalizado de fecha
hoy = datetime.today().strftime('%Y-%m-%d %H:%M:%S')

mongo_uri = f"mongodb+srv://{db_user}:{db_pass}@{db_host}/?retryWrites=true&w=majority"

# nombre del servidor (sonda) que correra el script
server_name = socket.gethostname()

# manejo de errores
current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
logging.basicConfig(filename=f'error_log_{current_time}.log', level=logging.ERROR)


def mide_latencia(host='8.8.8.8'):
    tiempo = ping(host)
    return tiempo

def verifica_intermitencia(host='8.8.8.8', count=4):
    result = subprocess.run(['ping', '-c', str(count), host], stdout=subprocess.PIPE)
    output = result.stdout.decode()

    if "0 packets received" in output:
        return count

    if "packets transmitted" in output:
        try:
            sent, received = map(int, output.split(',')[0].split()[-2:])
            return sent - received
        except:
            return None

    return None

def prueba_resolucion_dns(dominio="www.google.com"):
    try:
        socket.gethostbyname(dominio)
        return True
    except socket.gaierror:
        return False

def prueba_speedtest(fecha, nodo):
    speed = speedtest.Speedtest(secure=True)
    speed.get_best_server()
    download_speed = speed.download() / (10**6)  # Convertir de bits a Mbps
    upload_speed = speed.upload() / (10**6)  # Convertir de bits a Mbps
    ping = speed.results.ping

    result = {
            'date': fecha,
            'download_speed_mbps': download_speed,
            'upload_speed_mbps': upload_speed,
            'ping_ms': ping,
            'nodo': nodo
            }
    
    return result

def insertar_db(data, coleccion):
    try:
        client = MongoClient(mongo_uri)
        db = client.Cluster0
        collection = db[coleccion]
        collection.insert_one(data)
    except ConnectionFailure as c:
        logging.error(f"Fallo en la conexionn: {c}")
    except PyMongoError as e:
        logging.error(f"Error en PyMongo: {e}")
    finally:
        if 'client' in locals():
            client.close()

if __name__ == "__main__":
    host = "8.8.8.8"
    dominio = "www.google.com"

    latencia = mide_latencia(host)
    data = {
            'nodo': server_name, 
            'date': hoy, 
            'host': host, 
            'latencia': latencia 
            }
    insertar_db(data, "latencias")

    perdidos = verifica_intermitencia(host)
    if perdidos is not None:
        data = {
                'nodo': server_name, 
                'date': hoy, 
                'host': host, 
                'paquetes_perdidos': perdidos
                }
        insertar_db(data, "intermitencias")

    dns_exitoso = prueba_resolucion_dns(dominio)
    data = {
            'nodo': server_name, 
            'date': hoy, 
            'dominio': dominio, 
            'resolucion_exitosa': dns_exitoso
            }
    insertar_db(data, "resolucion_dns")

    prueba_velocidad = prueba_speedtest(hoy, server_name)
    insertar_db(prueba_velocidad, "speedtest")
