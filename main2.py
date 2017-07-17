import urllib.request
import json
import time
import os.path
import datetime
import coinmarkmod
from pygame import mixer

ficheroMonedas = "./monedas.csv"#ubicacion fichero monedas
ficheroVolumenes = "./volumenes.csv" #ubicacion fichero volumenes

while True:

	volumenActualizado = False

	#reproduce audio cada vez que el programa se ejecuta
	try:
		mixer.init()
		s = mixer.Sound("metal-gear-snake-eater.wav")#solo admite audios en formato .wav u .ogg
		s.set_volume(0.5)
		s.play()
		time.sleep(11)
		s.stop()
	except:
		print("No se ha podido reproducir audio")

	try:
	#descarga datos pagina en formato HTML
		paginaRaw = urllib.request.urlopen("https://api.coinmarketcap.com/v1/ticker/")

	except urllib.error.HTTPError as err:
		print("Error al descargar la pagina: " + str(err))
		time.sleep(300)
	except:
	    print("Error inesperado")
	    time.sleep(300)
	else:
		#almacena la informacion de la pagina decodificando el html usando el estandar utf-8
		pagina = paginaRaw.read().decode("utf-8")

		#el objeto del json es un array, por lo que python lo traduce en una lista si hacemos la conversion a objeto de python

		listaDecoded = json.loads(pagina)
		
		#crea los dos ficheros y devuelve true si han pasado 24 horas desde la ultima modificacion para actualizar el fichero volumenes
		volumenActualizado = coinmarkmod.CrearFicheros(ficheroMonedas,ficheroVolumenes)

		#cada moneda de la lista es un diccionario almacenado en un indice de este listado, recorremos listado y el mapa en cada posicion
		#print("he llegado al inicio de iterar")
		for i in range(0,len(listaDecoded)):
			#print("estoy iterando lista")
			for clave,valor in listaDecoded[i].items():
				#la lista de monedas tiene valores nulos y None que ocasiona que el programa falle por eso las filas con esos valores se convierten en comas
				if valor != "null" and valor != None:
					#print("estoy iterando mapa")
					if clave == "id":
						moneda = str(valor)
					if clave == "24h_volume_usd":
						volumen = str(valor)
					if clave == "percent_change_1h":
						porcentaje1h = float(valor)
					if clave == "percent_change_24h":
						porcentaje1d = float(valor)
					if clave == "last_updated":
						ultimaActualizacion = str(valor)
					if clave == "rank":
						rank = str(valor)
				else:
					if clave == "id":
						moneda = ","
					if clave == "24h_volume_usd":
						volumen = ","
					if clave == "percent_change_1h":
						porcentaje1h = ","
					if clave == "percent_change_24h":
						porcentaje1d = ","
					if clave == "last_updated":
						ultimaActualizacion = ","
					if clave == "rank":
						rank = ","
			#print("Me he quedado  aqui")
			if volumenActualizado:#si ha pasado mas de 24 horas actualiza el listado de volumenes
				#print("actualizar Volumen")
				coinmarkmod.ActualizarVolumen(ficheroVolumenes,moneda,volumen,ultimaActualizacion)

			if porcentaje1h != "," and porcentaje1d != ",":#si los porcentajes no estan vacios

				if porcentaje1h > 5.0 and porcentaje1d > 20.0:#si la moneda tiene un porcentaje apto se escribe en el fichero de monedas
					#print("actualizar monedas")
					coinmarkmod.EscribirMonedas(ficheroMonedas,moneda,rank,volumen,porcentaje1h,porcentaje1d,ultimaActualizacion)
			
		#fin bucle for
		time.sleep(3600)#espera 1 hora antes de siguiente interacción del bucle si la ejecucion del programa ha sido correcta
	
	
