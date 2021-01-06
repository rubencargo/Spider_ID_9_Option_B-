#! python3

# Importamos librerías. #
import urllib.request #Libreria necesaria para poder calcular el peso de la pagina#
import requests
import sys

from bs4 import BeautifulSoup

# Creamos nuestras listas (Declaracion de la lista). #
urls = []

if len(sys.argv) ==3:
	# Recibimos los argumentos, en mi caso se refiere a la Url que le paso. #
	target_url = sys.argv[1]
	if target_url[:4] == "http": #Primer if para controlar el primer argumento que sea valido.#
		# Realizamos una conexión al argumento pasado y además, leemos todo el contenido del código fuente que existe en la página. #
		url = requests.get(target_url).content
		#  BeautifulSoup es una libreria que usamos para parsear el HTML (PARSING) #
		soup = BeautifulSoup(url,'html.parser') 
		# Mediante el for y el método de bs4 llamado find_all, recolectamos todas las etiquetas donde existe a. #
		#El line se refiere a cada linea del html es el equivalente al i de un for normal#
		for line in soup.find_all('a'): #Esta funcion te devuelve todas las lineas que tengan un "a"#
			new_line = line.get('href') # Guardamos en una variable la URL de la etiqueta "a"#
			line_etiqueta = line.find(sys.argv[2]) #En esta linea buscamos dentro de la etiqueda "a" el segundo argumento que se ha pasado (En nuestro caso la etiqueta pasada)#
			if line_etiqueta != None: #Esta linea controla el caso de que el argumento que le hayamos pasado, no se encuentre (QUe no tenga imagenes)#
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
		if len(urls)>0:

			#Accedemos a las paginas recogidas inicialmente y comprobamos si son accesibles o no#
			for get_this in urls:
				if get_this[:4] == "http":
					url = get_this
					usock = urllib.request.urlopen(url)
					data = usock.read()
					size = data.__len__() 
					size = size / 1024.0 # Tamaño en KB
					print ('URL:',get_this,'   |   Size: ',size,'Kb')
				else:
					print('URL:',get_this,'  -->  Link can not be accessed')
		else:
			print('No hyperlinks were found containing the tag:', sys.argv[2])
	else:
		print('The first argument is invalid', sys.argv[1])
else:
	print ('You have to pass 2 arguments: Like for example: https://www.marca.com/ img ')