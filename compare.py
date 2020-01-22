import sys
import os
import subprocess
import time
from os.path import *
import csv
import re


class ContainerRN:
    def __init__(self):
        self.amount=0
        self.initTime=0
        self.finalTime=0
        self.dict={}

labels=[]

def main():
    # {etiqueta, cantidad de objetos detectados}
    # en un principio los diccionarios estarian inicializados con todas las etiquetas posibles y 0 como valor
    ais = ContainerRN()
    yolo = ContainerRN()
    runAlg1('F://YOLO//ClasificacionAIS//test_images', ais)
    runAlg2(yolo)
    printValues(yolo, ais)

def readClasificate(labelsObj, ais):
    #lee el string pasado por parametro labelsObj pasado de la forma etiqueta1_precission1|etiqueta2_precission2... por cada objeto detectado por el algoritmo de ais, los traduce y huelca al diccionario correspondiente a ais
    listLabels=labelsObj.split("|")
    valuePrecission=0.0
    originalLabel=""
    for i in range(0,len(listLabels)-1,1):
        listLabels[i]=listLabels[i].split("_")
        if( valuePrecission < float(listLabels[i][1]) ):
            valuePrecission=float(listLabels[i][1])
            originalLabel=listLabels[i][0]
    if originalLabel.lower() in ais.dict:
        ais.dict[originalLabel.lower()]+=1
    else:
        ais.dict[originalLabel.lower()]=1

def loadLabels(cad):
    classif = ""
    # procesar la salida del script de ais
    # primero lee la lista de las etiquetas que utiliza ais y las guarda en una lista propia del programa para luego utilizarla como referencia de las etiquetas que se desea utilizar
    for pos in range(0, cad.find(']'), 1):
        if (cad[pos] not in {"[", "'", ",", " "}):
            classif += cad[pos]
        elif classif != "":
            labels.append(classif)
            classif = ""

def loadAis(arrAis, ais):
    for pos in range(0,len(arrAis)):
        cont=arrAis[pos].lstrip("\r\n").rstrip("\r\n")
        if pos is 0:
            ais.finalTime=float(arrAis[pos])
        elif pos is 1:
            ais.amount=int(arrAis[pos])
        else:
            readClasificate(arrAis[pos],ais)
    print(ais.finalTime)

#folderTrackedBlob posee la ubicacion a la carpeta que posee cada carpeta para cada TB, que cada una de ellas contiene 5 archivos
#folderTB='F://YOLO//prueba//'
def runAlg1(folderTB,ais):
    #Ejecuta el script de AIS para detectar y clasificar todos los tb
    #En el script se realiza la iteracion por todas las carpetitas correspondientes a todos los tb detectados
    #El script devuelve un string de la forma "folderImgClasificada.jpg;CAR;0.8|BUS;0.1|TRUCK;0.1"
    ais.initTime=time.time()
    sub = subprocess.Popen([r'F:\YOLO\TestYoloAis\run-ScriptAis-Py.bat'], stdout=subprocess.PIPE, shell=False)
    outAis=sub.stdout.read()
    resultPrint=(str(outAis).encode("utf-8").decode("unicode-escape").encode("latin-1").decode("utf-8"))
    resultPrint = resultPrint[int(resultPrint.find('[')):int(len(resultPrint))]
    #resultPrint="['pickup', 'bus', 'car', 'cyclist', 'human', 'truck', 'van'];\r\n3.602055072784424;21;cyclist_46.22|pickup_34.62|human_6.40|car_5.25|van_4.75|truck_1.73|bus_1.03|;human_97.03|cyclist_2.95|bus_0.02|truck_0.00|van_0.00|pickup_0.00|car_0.00|;truck_54.41|pickup_15.22|bus_12.68|human_11.82|cyclist_4.52|car_0.90|van_0.45|;human_71.68|pickup_21.36|cyclist_6.62|car_0.22|truck_0.06|van_0.03|bus_0.02|;human_57.99|truck_24.39|pickup_8.19|bus_7.55|cyclist_1.55|van_0.20|car_0.12|;human_99.81|cyclist_0.17|truck_0.01|pickup_0.00|car_0.00|bus_0.00|van_0.00|;human_93.01|cyclist_6.83|bus_0.09|pickup_0.03|car_0.02|truck_0.01|van_0.01|;cyclist_95.17|bus_3.26|truck_1.04|human_0.37|pickup_0.11|van_0.03|car_0.02|;human_58.99|bus_26.69|cyclist_7.69|van_3.99|truck_2.27|pickup_0.28|car_0.09|;human_68.59|cyclist_28.10|bus_1.55|truck_1.11|pickup_0.52|car_0.08|van_0.05|;human_99.20|cyclist_0.62|truck_0.15|pickup_0.02|bus_0.01|car_0.00|van_0.00|;human_66.44|cyclist_33.25|truck_0.18|bus_0.09|pickup_0.03|van_0.01|car_0.00|;human_71.07|bus_13.01|van_10.08|cyclist_3.86|pickup_1.20|car_0.52|truck_0.27|;human_70.94|cyclist_14.27|pickup_8.90|truck_5.27|bus_0.28|van_0.23|car_0.10|;human_31.48|truck_22.16|bus_21.64|cyclist_12.64|pickup_6.89|van_3.09|car_2.10|;truck_79.07|human_10.33|bus_4.88|cyclist_4.81|pickup_0.78|car_0.09|van_0.05|;bus_36.80|truck_27.55|human_23.75|cyclist_11.17|van_0.52|car_0.15|pickup_0.05|;truck_78.81|human_10.80|bus_3.20|van_2.77|pickup_2.56|car_1.23|cyclist_0.62|;human_32.92|van_26.99|truck_19.32|cyclist_11.62|bus_7.90|pickup_1.05|car_0.19|;human_71.53|truck_24.49|cyclist_3.78|pickup_0.11|bus_0.10|car_0.00|van_0.00|;bus_61.37|truck_19.98|cyclist_10.96|human_7.57|pickup_0.09|car_0.02|van_0.02|\r\n"
    resultPrint=resultPrint.replace(r"\r\n","")
    print(resultPrint)
    loadLabels(resultPrint)
    resultPrint = resultPrint[int(resultPrint.find(']')) + 1:int(len(resultPrint))]
    resultArray=resultPrint.split(";")
    print(resultArray)
    resultArray.remove("")
    #Se recorre todo el resto del string pasado por ais para obtener la clasificacion con su precision de cada objeto
    loadAis(resultArray, ais)

#Toma la salida de la yolo densa, para eso se pasa el comando con todfos sus parametros
#videoMp4='D://Videos//usina//fanless2//2018-09-02//2018-09-02_15-01-07.mp4'
#backupOutputDensa='d://temp//YoloUsina15-01-07//'
def checkLabel(objectLabel, value, yolo):
    #agrega uno mas a la posicion correspondiente a la etiqueta de yolo de su diccionario
    if objectLabel in labels:
        yolo.dict[objectLabel]=value+1
    elif objectLabel=='motorbike' or objectLabel=='bicycle':
        yolo.dict['cyclist']=value+1
    elif objectLabel=='person':
        yolo.dict['human']=value+1
    elif objectLabel=='dog' or objectLabel=='horse':
        yolo.dict['animal']=value+1
    else:
        yolo.dict[objectLabel]=value+1#podria ser etiquetado como other

def getLabelDicYolo(label, yolo):
    #devuelve la etiqueta correspondiente al diccionario de yolo
    #para que se corresponda con las de ais
    if label in yolo.dict.keys():
        return label
    elif label=='motorbike' or label=='bicycle':
        return 'cyclist'
    elif label=='person':
        return 'human'
    elif label=='dog' or label=='horse':
        return 'animal'
    else:
        return label

def loadDicYOLO(folderYOLO, yolo):
    #loadDicYOLO lee las carpetitas que contienen los json generados por la salida de la red YOLO y huelca los datos al diccionario
    #correspondiente al objeto yolo del programita
    print(folderYOLO)
    for root, dirs, files in os.walk(folderYOLO):
        print(files)
        for lab in files:
            #labArr=str(lab).split("_")
            labelObj=getLabelDicYolo(str(lab).split("_")[1], yolo)
            cant = int(yolo.dict.get(labelObj) or 0)
            checkLabel(labelObj,cant,yolo)
        yolo.amount=len(files)

def runAlg2(yolo):
    #el algoritmo debe ejecutar la red YOLO (densa) y obtener los resultados y completar el diccionario
    #args:
    #p=subprocess.Popen([r'D:\YOLO_CL\run-S2-Yolo3-w20.bat'])#corre el batch file que hizo juan para correr la red
    yolo.initTime=time.time()
    #p.communicate()
    loadDicYOLO("F://YOLO//TestYoloAis//test_yolo//Yolo_S2w20T7//events//sheets//", yolo)
    #Calcula el tiempo final de ejecucion de la red densa
    yolo.finalTime=time.time()-yolo.initTime
    print(yolo.finalTime)

def printValues(yolo, ais):
    #Este metodo imprime una tabla de la forma Yolo | AIS | Human
    #Volcando los datos de la cantidad de objetos detectados y clasificados
    #
    print("{1:^36s}".format("|", "____________________________________"))
    print("{4}{0:10s}{4}{4}{2:^10s}{4}{4}{3:^10s}{4}".format(" ","\n","YOLO","AIS","|"))
    print("{2}{0:^10s}{2}{2}{1:^22s}{2}".format("Etiqueta","Valor","|"))
    for etiqueta in labels:
        #por todos los items dentro del diccionario correspondiente a la red densa, itero por su etiqueta y valor correspondiente
        valorYolo=int(yolo.dict.get(etiqueta) or 0)
        valorAis=int(ais.dict.get(etiqueta) or 0)
        print("{2}{0:^10s}{2}{2}{1:^10d}{2}{2}{3:^10d}{2}".format(etiqueta, valorYolo,"|",valorAis))
    etiquetasYolo=set.difference(set(yolo.dict.keys()),labels)
    for etiqueta in etiquetasYolo:
        print("{2}{0:^10s}{2}{2}{1:^10d}{2}{2}{3:^10d}{2}".format(etiqueta, yolo.dict.get(etiqueta), "|", 0))
    print("{1:^36s}".format("|", "____________________________________"))
    print("{0}{1:^10s}{0}{0}{2:^10d}{0}{0}{3:^10d}{0}".format("|", "Total", yolo.amount, ais.amount))
    print("{0}{1:^10s}{0}{0}{2:^10f}{0}{0}{3:^10f}{0}".format("|", "Tiempo", yolo.finalTime, ais.finalTime))


if __name__ == "__main__":
    main()