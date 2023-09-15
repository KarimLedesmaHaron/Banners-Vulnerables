# ===================================================
# banners_vulnerables
# Autor: "K" kharon.it@gmail.com
# Fecha: 14 de Septiembre 2023 / Córdoba - Argentina
#
# pip install -r requirements.txt
#
# ===================================================
logo = """
						┳┓            ┏┓    ┓ ┓ •    
						┣┫┏┓┏┓┏┓┏┓┏┓  ┃┓┏┓┏┓┣┓┣┓┓┏┓┏┓
						┻┛┗┻┛┗┛┗┗ ┛   ┗┛┛ ┗┻┗┛┗┛┗┛┗┗┫
													┛
                                        Creado por "K"
    """
print(logo)

import socket
from tqdm import tqdm
import os

def banner_grabbing(ip_url, puerto, banners_vulnerables, archivo_reporte):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip_url, puerto))
        s.settimeout(1)
        banner = s.recv(1024).decode('utf-8')
        for banner_vulnerable in banners_vulnerables:
            if banner.strip() in banner_vulnerable.strip():
                with open(archivo_reporte, "a") as reporte:
                    reporte.write(f"¡Tenemos un ganador! {banner}\n")
                    reporte.write(f"IP/URL: {ip_url}\n")
                    reporte.write(f"Puerto: {puerto}\n\n")
        s.close()
    except:
        pass

if __name__ == "__main__":
    archivo_ip_url = "ip_url.txt"
    archivo_puertos = "puertos.txt"
    archivo_reporte = "reporte.txt"  # Informe
    carpeta_banners = "banners"  # Banners

    with open(archivo_ip_url, "r") as archivo_ip_url:
        ips_urls = archivo_ip_url.read().splitlines()

    with open(archivo_puertos, "r") as archivo_puertos:
        puertos = [int(puerto) for puerto in archivo_puertos.read().splitlines()]

    # Toma la lista de archivos de banners desde la carpeta "banners"
    archivos_de_banners = os.listdir(carpeta_banners)

    # Crear un diccionario que mapea números a archivos de banners
    banners_por_tipo = {i + 1: os.path.join(carpeta_banners, archivo) for i, archivo in enumerate(archivos_de_banners)}

    # Menú interactivo
    print("Selecciona el tipo de búsqueda de banners:")
    for key, value in banners_por_tipo.items():
        print(f"{key}) {os.path.basename(value).replace('_banners.txt', '').title()}")

    tipo_busqueda = int(input("Ingresa el número correspondiente al tipo de búsqueda: "))

    # Obtener el archivo de banners correspondiente al tipo seleccionado
    archivo_banners_vulnerables = banners_por_tipo.get(tipo_busqueda)

    # Verificar si se seleccionó un tipo válido
    if archivo_banners_vulnerables is None:
        print("Tipo de búsqueda no válido.")
    else:
        with open(archivo_banners_vulnerables, "r") as archivo_banners_vulnerables:
            banners_vulnerables = archivo_banners_vulnerables.read().splitlines()

        # Calcula el total de iteraciones para la barra de progreso
        total_iteraciones = len(ips_urls) * len(puertos)
        barra_progreso = tqdm(total=total_iteraciones, desc="Progreso", unit="iter")

        # Abre el archivo de informe para escribir en él
        with open(archivo_reporte, "w") as reporte:
            for ip_url in ips_urls:
                for puerto in puertos:
                    try:
                        banner_grabbing(ip_url, puerto, banners_vulnerables, archivo_reporte)
                        barra_progreso.update(1)  # Actualiza la barra de progreso
                    except ValueError:
                        reporte.write(f"El puerto '{puerto}' en '{ip_url}' no es un número válido.\n")

        barra_progreso.close()  # Cierra la barra de progreso al finalizar
        print("Informe generado con éxito en el archivo 'reporte.txt'")
