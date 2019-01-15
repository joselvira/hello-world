# -*- coding: utf-8 -*-
"""
Created on Fri Oct 09 18:20:40 2018

@author: jose.lopeze

Plantilla para procesar todos los archivos de una carpeta
Cambia comas por puntos o puntos por comas
"""

import numpy as np
import pandas as pd
import time #para cuantificar tiempos de procesado


from matplotlib import pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages #para guardar gráficas en pdf


unidadDisco = r'G:\Mi unidad'
carpetaOriginal = r'\Programacion\Python\Mios\TratamientoDatos'

extensionArchivos = '\*.txt'
separador= '\t'

sepInicial=',' #separador decimal de los archivos originales
sepFinal='.' #separador decimal de los archivos transformados

#los archivos transformados les pone este añadido al final para identificarlos
if sepFinal==',':
    nomSepFin='Comas'
else: 
    nomSepFin='Puntos'
        


#Mete en una lista todos los archivos de la carpeta
import glob
lista = glob.glob(unidadDisco + carpetaOriginal + extensionArchivos)
#si se quiere que capture todos los archivos INCLUSO EN SUBCARPETAS
#lista = glob.glob(unidadDisco + carpetaOriginal +'\*'+ extensionArchivos)


print ("A procesar {0:d} archivos".format(len(lista)))

#Si hace falta crea la carpeta donde se guardarán los archivos procesados
import os
carpetaInput = os.path.dirname(lista[0])
carpetaOutput = os.path.join(carpetaInput, 'CarpetaProcesada')
if not os.path.isdir(carpetaOutput):
    os.mkdir(carpetaOutput)


#################################################################
#Va abriendo archivos uno a uno y los trata
tpoTotal=time.time() #para cuantificar cuánto tarda con cada archivo
ErroresArchivos=[]#guarda los nombres de archivo que no se pueden abrir y su error 
numProcesados=0 #contador de los archivos que va procesando


nomArchivosProcesados=[]

print("\n\nIniciando el procesado de los archivos...\n")
for NombreArchivo in lista[:]:    
    timer = time.time() #inicia el contador de tiempo
    
    
    # =============================================================================
    #%%Lee los datos
    # =============================================================================    
    try: #intenta leer el archivo
        f = open(NombreArchivo, 'r')
    except Exception as err: #Si falla anota un error y continua
        print("\nATENCIÓN, no se ha podido procesar "+ os.path.basename(NombreArchivo), err)          
        ErroresArchivos.append(os.path.basename(NombreArchivo)+" "+ err.message)
        continue
    else:
        print ('Procesando archivo num {0:d} {1:s}'.format(numProcesados+1, os.path.basename(NombreArchivo)))    
    #==============================================================================
       
        
    s= open(NombreArchivo+'_'+nomSepFin+'.txt', 'w')

    for line in f:
        l=line.replace(sepInicial, sepFinal)
        s.writelines(l)
    
    #Finaliza procesado del archivo
    s.close()
    f.close()
    numProcesados+=1
    nomArchivosProcesados.append(os.path.basename(NombreArchivo))
    #print("\nNum {0:d} nombre {1:s}".format(numProcesados, os.path.basename(NombreArchivo)))    
    print("Tiempo de procesado {0:.3f} s \n".format(time.time()-timer))
      
    #==============================================================================

#ya ha terminado de procesar todos los archivos
print("\nProcesados {0:d} de {1:d} archivos en la carpeta".format(numProcesados, len(lista)))
print("Tiempo total {0:.3f} s".format(time.time()-tpoTotal))

#Si no ha podido cargar algún archivo, lo indica
if len(ErroresArchivos)>0:
    print("No se ha podido procesar:")
    for x in range(len(ErroresArchivos)):
        print(ErroresArchivos[x])

#FIN
#################################################################



