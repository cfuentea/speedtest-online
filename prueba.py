import speedtest, socket, subprocess
from datetime import datetime
from ping3 import ping, verbose_ping

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

if __name__ == "__main__":
    host = "8.8.8.8"
    dominio = "www.google.com"

    latencia = mide_latencia(host)
    if latencia:
        print(f"Latencia hacia {host}: {latencia} ms")
    else:
        print(f"No se pudo medir la latencia hacia {host}")

    perdidos = verifica_intermitencia(host)
    if perdidos is not None:
        print(f"Paquetes perdidos hacia {host}: {perdidos}")
    else:
        print(f"No se pudo verificar intermitencia hacia {host}")

    dns_exitoso = prueba_resolucion_dns(dominio)
    if dns_exitoso:
        print(f"Resolución DNS para {dominio} fue exitosa.")
    else:
        print(f"Resolución DNS para {dominio} falló.")

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
    'ping_ms': ping
}
    
print(result)
