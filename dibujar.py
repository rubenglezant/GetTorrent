__author__ = 'ruben'

from bs4 import BeautifulSoup
import requests

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
    else:
        print "Status Code %d" %statusCode

# PRINCIPAL
# Llega hasta 1090 de 10 en 10
for x in range(1, 109):
    # Ruta de la pagina web
    url = 'http://www.estrenotorrent.com/tags/dvd%3Arip?start=' + str(x*10)
    getPage(url)
