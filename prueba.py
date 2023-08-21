import speedtest, socket, subprocess, os
from dotenv import load_dotenv
from datetime import datetime
from ping3 import ping, verbose_ping
from pymongo import MongoClient

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


def insertar_db(data, coleccion):
    client = MongoClient(mongo_uri)
    db = client.Cluster0
    collection = db[coleccion]
    collection.insert_one(data)
    client.close()

if __name__ == "__main__":
    host = "8.8.8.8"
    dominio = "www.google.com"

    latencia = mide_latencia(host)
    data = {
            'nodo': server_name, 
            'date': datetime.today().strftime('%Y-%m-%d %H:%M:%S'), 
            'host': host, 
            'latencia': latencia 
            }
    insertar_db(data, "latencias")

    perdidos = verifica_intermitencia(host)
    if perdidos is not None:
        data = {
                'nodo': server_name, 
                'date': datetime.today().strftime('%Y-%m-%d %H:%M:%S'), 
                'host': host, 
                'paquetes_perdidos': perdidos
                }
        insertar_db(data, "intermitencias")

    dns_exitoso = prueba_resolucion_dns(dominio)
    data = {
            'nodo': server_name, 
            'date': datetime.today().strftime('%Y-%m-%d %H:%M:%S'), 
            'dominio': dominio, 
            'resolucion_exitosa': dns_exitoso
            }
    insertar_db(data, "resolucion_dns")

    # Ejecutar la prueba de velocidad
    speed = speedtest.Speedtest(secure=True)
    speed.get_best_server()
    download_speed = speed.download() / (10**6)  # Convertir de bits a Mbps
    upload_speed = speed.upload() / (10**6)  # Convertir de bits a Mbps
    ping = speed.results.ping
    
    result = {
            'date': datetime.today().strftime('%Y-%m-%d %H:%M:%S'),
            'download_speed_mbps': download_speed,
            'upload_speed_mbps': upload_speed,
            'ping_ms': ping,
            'nodo': server_name
            }
    insertar_db(result, "speedtest")
