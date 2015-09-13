__author__ = 'ruben'


# -*- coding: utf-8 -*-
import urllib2, unicodedata
from bs4 import BeautifulSoup


def analisisDescarga(archivo, conexion):
    html = conexion.read()
    soup = BeautifulSoup(html)
    # obtenemos una lista de String con la condicin de atributos class con valores details y price
    links = soup.find_all(True, {'class': ['nombre']})
    # la lista alterna valores de nombre de producto y precio
    #   creamos una bandera para diferenciar si es valor o producto
    precio = False
    for tag in links:
        print("--")
        for linea in tag:
            linea = linea.strip();
            print('linea: ' + linea)
            href = str(tag['href'])
            # adaptamos unicode a utf-8
            normalizado = unicodedata.normalize('NFKD', linea).encode('ascii', 'ignore')
            archivo.write(normalizado + '|')
            # Obtenemos la URL de Descarga
            hrefS = href.split('/')
            print('href: ' + hrefS[2])
            archivo.write('http://www.elitetorrent.net/get-torrent/'+ hrefS[2] + '\n')

# este metodo se conectara con la web y establece un timeout que obliga a reintentar el fallo
# una vez descargada realiza el analisis
def preparar(archivo, web, x):
    try:
        print(web)
        conector = urllib2.urlopen(web, timeout=10)  # timeout de 10 segundos
        analisisDescarga(archivo, conector)
    except:
        print("Tiempo de espera agotado, volviendo a intentar")
        preparar(archivo, web, x)

# Programa principal
print('Comienza el programa')
archivo = open('peliculasTorrent.csv', 'a')

# El CSV separa las columnas por medio de tabuladores
for x in range(1, 7):
    # Ruta de la pagina web
    url = 'http://www.elitetorrent.net/categoria/17/peliculas-microhd/pag:' + str(x)
    preparar(archivo, url, x)

archivo.close()
print('Fin del programa')


