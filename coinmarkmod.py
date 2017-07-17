import time
import os.path
import datetime

def CrearFicheros(ficheroMonedas,ficheroVolumenes):

	#comprueba si el fichero monedas existe
	if os.path.exists(ficheroMonedas):
		try:
			fo = open(ficheroMonedas,"w")#deja el documento vacio
			print("fichero Monedas vaciado")
			fo.write("Moneda;Ranking;Volumen;Porcentaje1h;Porcentaje1d;FechaActualizacion;FechaGuardado\n")#cabecera fichero monedas
			fo.close()
		except OSError as err:
				print("error al abrir archivo:" + str(err))
	else:#sino existe monedas lo crea
		try:
			fo = open(ficheroMonedas,"w")
			fo.write("Moneda;Ranking;Volumen;Porcentaje1h;Porcentaje1d;FechaActualizacion;FechaGuardado\n")#cabecera fichero monedas
			print("fichero Monedas creado")
			fo.close()
		except OSError as err:
			print(str(err))

	if os.path.exists(ficheroVolumenes):#comprueba si existe el fichero volumen
		try:

			fechaModificacionUnix = os.path.getmtime(ficheroVolumenes)#devuelve el tiempo en tiempo UNIX
			fechaModificacion = datetime.datetime.fromtimestamp(fechaModificacionUnix)#convierte a formato fecha
			fechaActual = datetime.datetime.now()#fecha actual
				
			if (fechaActual - fechaModificacion) > datetime.timedelta(hours = 23,minutes = 59):#si el tiempo desde que se ha actualizado el fichero ha sido mayor que 24 horas
				fo = open(ficheroVolumenes,"a")#abre el fichero y coloca el puntero al final sin sobreescribir
				fo.write("\n")#crea un salto de linea
				fo.close()
				return True
			else:
				return False
				
		except OSError as err:
			print(str(err))
	else:#sino existe crea fichero volumen
		try:
			fo = open(ficheroVolumenes,"w")
			fo.write("Moneda;Volumen;FechaActualizacion;FechaGuardado\n")#cabecera fichero volumenes
			#print("fichero Volumenes creado")
			fo.close()
			return True
		except OSError as err:
			print(str(err))

def ActualizarVolumen(ficheroVolumenes,moneda,volumen,ultimaActualizacion):
	try:
		fo = open(ficheroVolumenes , "a")
		
		fo.write('"' + moneda + '"' + ";"+ '"' + str(volumen) + '"' + ";" + '"' + ultimaActualizacion + '"' + ";" + '"' +
		str(datetime.datetime.now()) + '"' + "\n")
		fo.close()
		#print("Se han actualizado el historial de volumenes en el archivo")
	except OSError as err:
		print(str(err))

def EscribirMonedas(ficheroMonedas,moneda,ranking,volumen,porcentaje1h,porcentaje1d,ultimaActualizacion):
	try:

		#print("moneda to the moooooooooooon")
		fo = open(ficheroMonedas,"a")
		fo.write( '"' + moneda + '"' + ";"  + '"' + ranking + '"' + ";" + '"' + volumen + '"' + ";" + '"' + str(porcentaje1h) + '"' +
		";" + '"' + str(porcentaje1d) + '"' + ";" + '"' + ultimaActualizacion + '"' + ";" + '"' + str(datetime.datetime.now()) + '"' + "\n")
		fo.close()
	except OSError as err:
		print(str(err))