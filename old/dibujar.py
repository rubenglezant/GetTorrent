__author__ = 'ruben'

from bs4 import BeautifulSoup
import requests
import MySQLdb
import sys

def getURLTorrentSalto(url):
    # Realizamos la peticion a la web
    req = requests.get(url)

    # Comprobamos que la peticion nos devuelve un Status Code = 200
    statusCode = req.status_code
    if statusCode == 200:

        # Pasamos el contenido HTML de la web a un objeto BeautifulSoup()
        html = BeautifulSoup(req.text)

        # Obtenemos todos los divs donde estan las entradas
        entradas = html.find_all('script',{'type':'text/javascript'})

        # Recorremos todas las entradas para extraer el titulo, autor y fecha
        for i,entrada in enumerate(entradas):
            # Con el metodo "getText()" no nos devuelve el HTML
            titulo = entrada.getText()
            href = "download"
            if ("get_torrent.php?id" in titulo):
                index = titulo.find("get_torrent.php?id")
                # Imprimo el Titulo, Autor y Fecha de las entradas
                data = "http://www.estrenotorrent.com/get_torrent.php?id="
                data = data + titulo[index+19:index+79];
                return data
    else:
        print "Status Code %d" %statusCode

def getURLTorrent(url):
    # Realizamos la peticion a la web
    req = requests.get(url)

    # Comprobamos que la peticion nos devuelve un Status Code = 200
    statusCode = req.status_code
    if statusCode == 200:

        # Pasamos el contenido HTML de la web a un objeto BeautifulSoup()
        html = BeautifulSoup(req.text)

        # Obtenemos todos los divs donde estan las entradas
        entradas = html.find_all('a',{'rel':'nofollow'})

        # Recorremos todas las entradas para extraer el titulo, autor y fecha
        for i,entrada in enumerate(entradas):
            # Con el metodo "getText()" no nos devuelve el HTML
            titulo = entrada.getText()
            href = entrada['href']
            if ("download" in href):
                return getURLTorrentSalto("http://www.estrenotorrent.com" + href)
    else:
        print "Status Code %d" %statusCode


def getPage(url):
    # Realizamos la peticion a la web
    req = requests.get(url)

    # Comprobamos que la peticion nos devuelve un Status Code = 200
    statusCode = req.status_code
    if statusCode == 200:

        # Pasamos el contenido HTML de la web a un objeto BeautifulSoup()
        html = BeautifulSoup(req.text)

        # Obtenemos todos los divs donde estan las entradas
        entradasAlto = html.find_all('div',{'class':'info'})

        for itemAlto in enumerate(entradasAlto):
            entrada = itemAlto[1].find('div').find('a')
            # Recorremos todas las entradas para extraer el titulo, autor y fecha
            # Con el metodo "getText()" no nos devuelve el HTML
            titulo = entrada.getText()
            href = getURLTorrent("http://www.estrenotorrent.com"+entrada['href'])
            fecha = itemAlto[1].find('div',{'class':'createdate'}).getText()
            descripcion = itemAlto[1].find('div',{'class':'text'}).getText().replace('\t','').replace('\r','').replace('\n','')
            print "%s|%s|%s|%s" %(titulo,href,fecha,descripcion)
            insertPeli(href,titulo,descripcion,fecha,0,0);
    else:
        print "Status Code %d" %statusCode

# create table pelis (url VARCHAR(500),title VARCHAR(500),description VARCHAR(5000),fecha VARCHAR(12),type INTEGER,language INTEGER, PRIMARY KEY (url))
# type: 0 - DivX
# language: 0 - Spanish
def insertPeli(url,title,desc,fecha,type,lang):
    try:
        x = conn.cursor()
        x.execute (" INSERT INTO pelis VALUES (%s,%s,%s,%s,0,0) ", (url,title,desc,fecha))
    except:
        print "Unexpected error:", sys.exc_info()[0]

# PRINCIPAL
# Llega hasta 1090 de 10 en 10
conn = MySQLdb.connect(host= "localhost",user="root",passwd="root",db="DB")

for x in range(56, 109):
    # Ruta de la pagina web
    url = 'http://www.estrenotorrent.com/tags/dvd%3Arip?start=' + str(x*10)
    getPage(url)
    conn.commit()

conn.close()
