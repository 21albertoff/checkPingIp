import json
import time
from datetime import datetime, timedelta
from ping3 import ping

# Función para cargar la configuración desde un archivo JSON
def cargar_configuracion():
    with open("direccionesIPs.json", "r") as archivo_json:
        configuracion = json.load(archivo_json)
    return configuracion

# Diccionario para almacenar los resultados por nombre
resultados = {}

# Diccionario para llevar un registro de la última vez que se mostró el aviso
ultimo_aviso = {}

# Diccionario para contar los fallos consecutivos
fallos_consecutivos = {}

# Cargar configuración desde el archivo JSON
configuracion = cargar_configuracion()
direcciones_ip = configuracion["direcciones_ip"]

# Inicializar diccionarios con la configuración cargada
for nombre, ip in direcciones_ip.items():
    resultados[nombre] = []
    ultimo_aviso[nombre] = None
    fallos_consecutivos[nombre] = 0

# Bucle infinito para monitorear continuamente
while True:
    for nombre, ip in direcciones_ip.items():
        # Realiza el ping
        respuesta = ping(ip)

        # Si el ping es exitoso, añade el resultado a la lista
        if respuesta is not None:
            resultados[nombre].append({"timestamp": time.strftime("%Y-%m-%d %H:%M:%S"), "status": "OK"})

            # Limita la lista a los últimos tres resultados
            resultados[nombre] = resultados[nombre][-3:]

            # Reinicia el contador de fallos consecutivos
            fallos_consecutivos[nombre] = 0
        else:
            # Incrementa el contador de fallos consecutivos
            fallos_consecutivos[nombre] += 1

            # Verifica si ha habido tres fallos consecutivos
            if fallos_consecutivos[nombre] == 3 and (ultimo_aviso[nombre] is None or
                                                     datetime.now() - ultimo_aviso[nombre] >= timedelta(hours=1)):
                print(f"Error en el ping de {nombre} ({ip}) (Fallo consecutivo 3 veces)", flush=True)
                ultimo_aviso[nombre] = datetime.now()

    # Espera 15 segundos antes del próximo ciclo
    time.sleep(15)

    # Guarda los resultados en un archivo JSON
    with open("resultados.json", "w") as archivo_json:
        json.dump(resultados, archivo_json, indent=4)

    print("Resultados guardados en resultados.json")
