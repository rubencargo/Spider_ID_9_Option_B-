#! python3

# Importamos librerías. #
import requests
import sys

from bs4 import BeautifulSoup

# Creamos nuestras listas. #
urls = []
urls2 = []

# Recibimos los argumentos. #
target_url = sys.argv[1]

# Realizamos una conexión al argumento pasado y además, leemos todo el contenido del código fuente que existe en la página. #
url = requests.get(target_url).content
# Usamos nuestra librería de bs4 para posteriormente recatar lo que deseamos. #
soup = BeautifulSoup(url,'html.parser')
# Mediante el for y el método de bs4 llamado find_all, recolectamos todas las etiquetas donde existe a href. #
for line in soup.find_all('a'):
	new_line = line.get('href')
	line_etiqueta = line.find(sys.argv[2])
	if line_etiqueta != None: 
		try:
			# Si existe en alguna línea del código fuente el http, lo almacenamos en nuestra lista llamada urls. #
			if new_line[:4] == "http":
				urls.append(str(new_line))
			# Si no existe, intentamos combinar nuestro argumento(url de la página) + lo que encontramos. #
			elif new_line[:1] == "/":
				try:
					comb_line = target_url+new_line
					urls.append(str(comb_line))
				except:
					pass
			else:
				#Enlaces fallidos como por ejemplo: javascript:void(0), lo añadimos para luego mostrar que en la ejecucion falla#
				urls.append(str(new_line))
		except:
			pass
	else:
		pass
#Accedemos a las paginas recogidas inicialmente y comprobamos si son accesibles o no#
for get_this in urls:
	if get_this[:4] == "http":
		print('URL:',get_this)
	elif get_this[:1] == "/":
		print('URL:',get_this)
	else:
		print('No se puede acceder al enlace', get_this)
