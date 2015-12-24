__author__ = 'ruben'

# -*- coding: utf-8 -*-
import urllib2, unicodedata
from bs4 import BeautifulSoup


def analisisDescarga(archivo, conexion):
    html = conexion.read()
    soup = BeautifulSoup(html)
    # obtenemos una lista de String con la condicin de atributos class con valores details y price
    links = soup.find_all("a")
    # la lista alterna valores de nombre de producto y precio
    #   creamos una bandera para diferenciar si es valor o producto
    precio = False
    #print(links)
    # archivo.write('http://www.mejortorrent.com/secciones.php?sec=descargas&ap=contar&tabla=peliculas&id='+ hrefS[2] + '&link_bajar=1\n')
    for tag in links:
        try:
            if ("peli-descargar-torrent" in tag['href']):
                hrefS = tag['href'].replace(".html","")
                hrefS = hrefS.split('-')
                print(hrefS[3])
                titulo = (' '.join(hrefS[4:]))
                archivo.write(titulo + '|')
                archivo.write('http://www.mejortorrent.com/secciones.php?sec=descargas&ap=contar&tabla=peliculas&id='+ hrefS[3] +'&link_bajar=1\n')
        except:
            print('No tag')

# este metodo se conectara con la web y establece un timeout que obliga a reintentar el fallo
# una vez descargada realiza el analisis
def preparar(archivo, web, x):
    print(web)
    conector = urllib2.urlopen(web, timeout=10)  # timeout de 10 segundos
    analisisDescarga(archivo, conector)


# Programa principal
print('Comienza el programa')
archivo = open('mejorTorrent.csv', 'a')

# El CSV separa las columnas por medio de tabuladores
for x in range(1, 50):
    # Ruta de la pagina web
    url = 'http://www.mejortorrent.com/secciones.php?sec=descargas&ap=series&p=' + str(x)
    preparar(archivo, url, x)

archivo.close()
print('Fin del programa')



