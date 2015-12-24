cd /home/ruben/temp/GetTorrent
echo "Comienzo de la descarga..." >> log.log
date >> log.log
python getEliteTorrent.py
python sendMail.py
cat pelis.txt pelisBBDD.txt >> pelis2.txt
cat pelis2.txt | sort | uniq > pelisBBDD.txt
echo " - Numero de registros" >> log.log
cat pelisBBDD.txt |wc -l >> log.log
rm -Rf pelis2.txt
rm -Rf pelis.txt





