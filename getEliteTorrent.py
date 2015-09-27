__author__ = 'ruben'


# -*- coding: utf-8 -*-
import urllib2, unicodedata
from bs4 import BeautifulSoup
import MySQLdb
import sys

def analisisDescarga(conexion):
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
            linea = linea.strip().replace('(DVDRip)','');
            print('linea: ' + linea)
            href = str(tag['href'])
            # adaptamos unicode a utf-8
            normalizado = unicodedata.normalize('NFKD', linea).encode('ascii', 'ignore')
            # Obtenemos la URL de Descarga
            hrefS = href.split('/')
            urlDest = 'http://www.elitetorrent.net/get-torrent/' + hrefS[2]
            print('href: ' + urlDest)
            insertPeli(urlDest,linea)

# este metodo se conectara con la web y establece un timeout que obliga a reintentar el fallo
# una vez descargada realiza el analisis
def preparar(web, x):
    try:
        print(web)
        conector = urllib2.urlopen(web, timeout=10)  # timeout de 10 segundos
        analisisDescarga(conector)
    except:
        print("Tiempo de espera agotado, volviendo a intentar")
        preparar(web, x)


# create table pelis (url VARCHAR(500),title VARCHAR(500),description VARCHAR(5000),fecha VARCHAR(12),type INTEGER,language INTEGER, PRIMARY KEY (url))
# type: 0 - DivX, 1 - BlueRay Rip, 2 - DVD RIP
# language: 0 - Spanish
def insertPeli(url,title):
    try:
        x = conn.cursor()
        x.execute (" INSERT INTO pelis VALUES (%s,%s,'','',2,0) ", (url,title))
    except:
        print "Unexpected error:", sys.exc_info()[0]


# Programa principal
print('Comienza el programa')
conn = MySQLdb.connect(host= "localhost",user="root",passwd="root",db="DB")

# El CSV separa las columnas por medio de tabuladores
# http://www.elitetorrent.net/categoria/2/peliculas/pag:
# http://www.elitetorrent.net/categoria/13/peliculas-hdrip/pag:
# http://www.elitetorrent.net/categoria/17/peliculas-microhd/pag:
# http://www.elitetorrent.net/categoria/4/series/pag:
for x in range(1, 280):
    # Ruta de la pagina web
    print "\n----> Tratando ------> %s\n" %(str(x))
    url = 'http://www.elitetorrent.net/categoria/4/series/pag:' + str(x)
    preparar(url, x)
    conn.commit()

print('Fin del programa')
conn.close()

