__author__ = 'ruben'

import smtplib
import time

s = ""
with open('pelis.txt') as f:
	for line in f:
		sSplit = line.split("|");
		s += sSplit[0] + "\n";
		s += "   " + sSplit[1] + "\n";

fecha = (time.strftime("%d/%m/%y"))

fromaddr = 'pcillo2mar@gmail.com'
toaddrs  = 'YYYYYYYY,pcillo2mar@gmail.com'
msg = "\r\n".join([
  "From: "+fromaddr,
  "To: "+toaddrs,
  "Subject: Pelis Nuevas - "+fecha,
  "",
  s
  ])
username = 'pcillo2mar@gmail.com'
password = 'XXXXXXXX'
server = smtplib.SMTP('smtp.gmail.com:587')
server.ehlo()
server.starttls()
server.login(username,password)
server.sendmail(fromaddr, toaddrs, msg)
server.quit()
