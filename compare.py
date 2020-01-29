import sys
import os
import subprocess
import time
from os.path import *
import re
import argparse


class ContainerRN:
    def __init__(self):
        self.amount=0
        self.initTime=0
        self.finalTime=0
        self.dict={}

LABELS=[]
YOLO_CONFIG='D:/YOLO_CL/cfg/yolov3.cfg'
YOLO_WEIGHTS='D:/YOLO_CL/cfg/yolov3.weights'

def readClasificate(objLabels, aisContain, threshold):
    # lee el string pasado por parametro objLabels pasado de la forma etiqueta1_precission1|etiqueta2_precission2...
    # por cada objeto detectado por el algoritmo de ais, los traduce y vuelca- al diccionario correspondiente a ais
    # args:
    #   objLabels: clasificaciones de un mismo objeto
    #   aisContain: instancia de la clase ContainerRN
    #   threshold: precission mas deseable
    listLabels=objLabels.split("|")
    valuePrecission=0.0
    theBestLabel=""
    for i in range(0,len(listLabels)-1,1):
        listLabels[i]=listLabels[i].split("_")
        # se queda con el valor de clasificacion mayor
        if valuePrecission == 0.0 and float(listLabels[i][1]) >= threshold or valuePrecission !=0.0 and valuePrecission < float(listLabels[i][1]) :
            valuePrecission = float(listLabels[i][1])
            theBestLabel = listLabels[i][0]
        # end if
    # end for
    # setea 1/suma 1 a la posicion accedida por el nombre de la etiqueta
    if theBestLabel.lower() in aisContain.dict:
        aisContain.dict[theBestLabel.lower()]+=1
    else:
        aisContain.dict[theBestLabel.lower()]=1
    # end if
# end function

def loadLabels(listLabels):
    # procesar la salida del script de ais
    # primero lee la lista de las etiquetas que utiliza ais y las guarda en una lista propia del programa para luego utilizarla como referencia de las etiquetas que se desea utilizar
    classif = ""
    for pos in range(0, listLabels.find(']'), 1):
        if (listLabels[pos] not in {"[", "'", ",", " "}):
            classif += listLabels[pos]
        elif classif != "":
            LABELS.append(classif)
            classif = ""
        # end if
    # end for
# end function

def loadAis(arrAis, aisContain, threshold, timeDetectAis):
    # recorre el arreglo correspondiente a la salida de ais y vuelca los datos en una instancia de ContainerRN
    # args:
    #   arrAis: arreglo correspondiente a la salida de ais
    #   ais: instancia de la clase ContainerRN
    for pos in range(0,len(arrAis)):
        if pos is 0:
            aisContain.finalTime= float(float(arrAis[pos]) + timeDetectAis)
        elif pos is 1:
            aisContain.amount=int(arrAis[pos])
        else:
            # por cada posicion luego de las dos primeras, llama al metodo que completa el diccionario de ais
            readClasificate(arrAis[pos],aisContain, threshold)
        # end if
    # end for
    print(timeDetectAis,"TIME DET AIS EN LOADAIS")
    print(aisContain.finalTime)
# end function

def runAlgAis(folderTB,aisContain, threshold, timeDetectAis, folderStAis):
    # Ejecuta el script de AIS para detectar y clasificar todos los tb
    # En el script se realiza la iteracion por todas las carpetitas correspondientes a todos los tb detectados
    # El script devuelve un string de la forma "folderImgClasificada.jpg;CAR;0.8|BUS;0.1|TRUCK;0.1"
    # args:
    #    folderTB posee la ubicacion a la carpeta que posee cada carpeta para cada TB, que cada una de ellas contiene 5 archivos
    #    aisContain es una instancia de la clase ContainerRN, que contiene un diccionario con la cantidad de objetos detectados por cada clasificacion
    # asocia el script de ais para deteccion y clasificacion
    setBatFileAis(folderTB,folderStAis)
    sub = subprocess.Popen([r''+folderTB], stdout=subprocess.PIPE, shell=False)
    # calcula tiempo inicial
    print("aca toma el tiempo")
    aisContain.initTime = time.time()
    # convierte caracteres de bytes a string de la salida del script de ais - elimina caracteres como 'b' o '\'
    resultPrint=(str(sub.stdout.read()).encode("utf-8").decode("unicode-escape").encode("latin-1").decode("utf-8"))
    #resultPrint="['pickup', 'bus', 'car', 'cyclist', 'human', 'truck', 'van'];\r\n3.602055072784424;21;cyclist_46.22|pickup_34.62|human_6.40|car_5.25|van_4.75|truck_1.73|bus_1.03|;human_97.03|cyclist_2.95|bus_0.02|truck_0.00|van_0.00|pickup_0.00|car_0.00|;truck_54.41|pickup_15.22|bus_12.68|human_11.82|cyclist_4.52|car_0.90|van_0.45|;human_71.68|pickup_21.36|cyclist_6.62|car_0.22|truck_0.06|van_0.03|bus_0.02|;human_57.99|truck_24.39|pickup_8.19|bus_7.55|cyclist_1.55|van_0.20|car_0.12|;human_99.81|cyclist_0.17|truck_0.01|pickup_0.00|car_0.00|bus_0.00|van_0.00|;human_93.01|cyclist_6.83|bus_0.09|pickup_0.03|car_0.02|truck_0.01|van_0.01|;cyclist_95.17|bus_3.26|truck_1.04|human_0.37|pickup_0.11|van_0.03|car_0.02|;human_58.99|bus_26.69|cyclist_7.69|van_3.99|truck_2.27|pickup_0.28|car_0.09|;human_68.59|cyclist_28.10|bus_1.55|truck_1.11|pickup_0.52|car_0.08|van_0.05|;human_99.20|cyclist_0.62|truck_0.15|pickup_0.02|bus_0.01|car_0.00|van_0.00|;human_66.44|cyclist_33.25|truck_0.18|bus_0.09|pickup_0.03|van_0.01|car_0.00|;human_71.07|bus_13.01|van_10.08|cyclist_3.86|pickup_1.20|car_0.52|truck_0.27|;human_70.94|cyclist_14.27|pickup_8.90|truck_5.27|bus_0.28|van_0.23|car_0.10|;human_31.48|truck_22.16|bus_21.64|cyclist_12.64|pickup_6.89|van_3.09|car_2.10|;truck_79.07|human_10.33|bus_4.88|cyclist_4.81|pickup_0.78|car_0.09|van_0.05|;bus_36.80|truck_27.55|human_23.75|cyclist_11.17|van_0.52|car_0.15|pickup_0.05|;truck_78.81|human_10.80|bus_3.20|van_2.77|pickup_2.56|car_1.23|cyclist_0.62|;human_32.92|van_26.99|truck_19.32|cyclist_11.62|bus_7.90|pickup_1.05|car_0.19|;human_71.53|truck_24.49|cyclist_3.78|pickup_0.11|bus_0.10|car_0.00|van_0.00|;bus_61.37|truck_19.98|cyclist_10.96|human_7.57|pickup_0.09|car_0.02|van_0.02|\r\n"
    resultPrint = resultPrint[int(resultPrint.find('[')):int(len(resultPrint))]
    print(resultPrint,"Antes de reemplazar los saltos")
    resultPrint=resultPrint.replace(r"\r\n","")
    print(resultPrint,"resultPrint1")
    # se llama al metodo que procesa los primeros caracteres desde el primer [ hasta el proximo ] para cargar los labels correspondientes a las clasificaciones que se estudiaran
    loadLabels(resultPrint)
    # se salta todos los caracteres hasta ']'
    print(resultPrint,"resultPrint2")
    resultPrint = resultPrint[int(resultPrint.find(']')) + 1:int(len(resultPrint))]
    # se separa el string por ';' en elementos de un arreglo
    print(resultPrint,"resultPrint3")
    resultArray=resultPrint.split(";")
    resultArray.remove("")
    print(resultArray,"este es resultArray")
    # Se recorre el resto del string pasado por ais para obtener la clasificacion con su precision de cada objeto
    loadAis(resultArray, aisContain, threshold, timeDetectAis)
# end function

def checkLabel(objectLabel, value, yoloContain):
    # agrega uno mas a la posicion correspondiente a la etiqueta que es key de yolo de su diccionario
    # args:
    #   objectLabel: etiqueta correspondiente a la clasificacion del objeto que detecto yolo
    #   value: valor anterior asociado a la etiqueta de yolo
    #   yoloContain: instancia de la clase ContainerRN
    # si la etiqueta se encuentra en la lista de etiquetas utilizadas tambien por ais
    if objectLabel in LABELS:
        yoloContain.dict[objectLabel]=value+1
    # si no se encuentra en la lista de etiquetas, entonces puede nombrarse distinto
    elif objectLabel=='motorbike' or objectLabel=='bicycle':
        yoloContain.dict['cyclist']=value+1
    elif objectLabel=='person':
        yoloContain.dict['human']=value+1
    elif objectLabel=='dog' or objectLabel=='horse':
        yoloContain.dict['animal']=value+1
    # es una clasificacion propia de yolo
    else:
        yoloContain.dict[objectLabel]=value+1
    # end if
# end function

def getLabelDicYolo(label, yoloContain):
    # devuelve la etiqueta correspondiente al diccionario de yolo
    # para que se corresponda con las de ais
    # args:
    #   label: etiqueta correspondiente a la clasificacion de yolo
    #   yoloContain: instancia de la clase ContainerRN
    if label in yoloContain.dict.keys():
        return label
    elif label=='motorbike' or label=='bicycle':
        return 'cyclist'
    elif label=='person':
        return 'human'
    elif label=='dog' or label=='horse':
        return 'animal'
    else:
        return label
    # end if
# end function

def loadDicYOLO(folderYOLO, yoloContain):
    # loadDicYOLO lee las carpetitas que contienen los json generados por la salida de la red YOLO y vuelca los datos al diccionario
    # correspondiente al objeto yolo del programita
    # args:
    #   folderYOLO: localizacion de las carpetitas de los json que genera la deteccion y clasificacion de la red yolo
    #   yoloContain: instancia de la clase ContainerRN
    print(folderYOLO)
    for root, dirs, files in os.walk(folderYOLO):
        print(files)
        for name in files:
            print(name,"names in loadDicYOLO")
            if str(name).endswith('.json'):
                labelObj=getLabelDicYolo(str(name).split("_")[1], yoloContain)
                value = int(yoloContain.dict.get(labelObj) or 0)
                checkLabel(labelObj,value,yoloContain)
                yoloContain.amount+=1
            # end if
        # end for
    print(yoloContain.amount,"cant filessss")
    # end for
# end function

def runAlgYolo(dirRunYolo, dirStoreYolo,yoloContain, dirVideoIn):
    # ejecuta el script que testea la red YOLO (densa) y con los resultados, completa el diccionario
    # args:
    #   dirRunYolo: direccion donde se encuentra el batch file que corre el script de yolo
    #   dirStoreYolo: direccion de donde se guardaran las carpetitas de todos los objetos json, correspondientes a cada tb
    #   yoloContain: instancia de la clase ContainerRN
    # corre el batch file que hizo juan para correr la red
    #p=subprocess.Popen(paramYolo)
    setBatFileYolo(dirRunYolo,dirStoreYolo, dirVideoIn)
    p=subprocess.Popen([r''+dirRunYolo])
    # calcula el tiempo inicial
    yoloContain.initTime=time.time()
    p.communicate()
    # llama a la funcion encargada de volcar los datos leidos al diccionario de yolo
    loadDicYOLO(dirStoreYolo, yoloContain)
    # Calcula el tiempo final de ejecucion de la red densa
    yoloContain.finalTime=time.time()-yoloContain.initTime
    print(yoloContain.finalTime)
# end function

def printValues(yoloContain, aisContain):
    # Este metodo imprime una tabla de la forma Yolo | AIS | Human
    # Volcando los datos de la cantidad de objetos detectados y clasificados
    # args:
    #   yoloContain: instancia de la clase ContainerRN, correspondiente al contenido de yolo
    #   aisContain: idem anterior, correspondiente al contenido de ais
    print("{1:^36s}".format("|", "____________________________________"))
    print("{4}{0:10s}{4}{4}{2:^10s}{4}{4}{3:^10s}{4}".format(" ","\n","YOLO","AIS","|"))
    print("{2}{0:^10s}{2}{2}{1:^22s}{2}".format("Etiqueta","Valor","|"))
    # por todos los items dentro de la lista de labels, extraigo el valor que guarda cada diccionario, correspondiente a esa key
    for etiqueta in LABELS:
        valorYolo=int(yoloContain.dict.get(etiqueta) or 0)
        valorAis=int(aisContain.dict.get(etiqueta) or 0)
        print("{2}{0:^10s}{2}{2}{1:^10d}{2}{2}{3:^10d}{2}".format(etiqueta, valorYolo,"|",valorAis))
    # end for
    etiquetasYolo=set.difference(set(yoloContain.dict.keys()),LABELS)
    # por todas las etiquetas diferentes que posee yolo y no se encuentra en labels, las imprime con su valor
    for etiqueta in etiquetasYolo:
        print("{2}{0:^10s}{2}{2}{1:^10d}{2}{2}{3:^10d}{2}".format(etiqueta, yoloContain.dict.get(etiqueta), "|", 0))
    # end for
    print("{1:^36s}".format("|", "____________________________________"))
    print("{0}{1:^10s}{0}{0}{2:^10d}{0}{0}{3:^10d}{0}".format("|", "Total", yoloContain.amount, aisContain.amount))
    print("{0}{1:^10s}{0}{0}{2:^10f}{0}{0}{3:^10f}{0}".format("|", "Tiempo", yoloContain.finalTime, aisContain.finalTime))
# end function

def setBatFileAis(folderRunBat, folderStore):
    contenido=""
    with open(folderRunBat,'r') as file:
        column=file.read().split(' ')
        for pos in range(1,len(column)):
            if column[pos-1]=='--dir':
                column[pos]=folderStore
                break
            # end if
        # end for
        contenido=' '.join(column)
    # end with
    with open(folderRunBat,'w') as file:
        file.write(contenido)
    # end with
# end function

def setBatFileYolo(folderRunBat, folderVideo, folderStore):
    contenido = ""
    with open(folderRunBat, 'r') as file:
        column = file.read().split()
        for pos in range(1, len(column)):
            if column[pos - 1] == '-v':
                column[pos] = folderVideo
            elif column[pos - 1] == '-media':
                column[pos] = folderStore
            # end if
        # end for
        contenido = ' '.join(column)
    # end with
    with open(folderRunBat, 'w') as file:
        file.write(contenido)
    # end with
# end function

def main():
    # {etiqueta, cantidad de objetos detectados}
    #################################################################################################################################
    # args del algoritmo de comparacion
    parser = argparse.ArgumentParser()
    # parametro para que el usuario eliga que version de comparacion quiere usar (v1: normal por cantidad de obj ; v2: por hora de obj ; v3: por espacio)
    parser.add_argument('-v', '--version', type=int, choices=[1,2,3])
    parser.add_argument('-dirA', default=os.getcwd() + '//run-ScriptAis-Py.bat', type=str)
    parser.add_argument('-dirStA', default=os.getcwd() + '//test_images', type=str)
    parser.add_argument('-dirY', default=os.getcwd() + '//run-S2-Yolo3-w20.bat', type=str)
    parser.add_argument('-dirStY', default=os.getcwd() + '//test_yolo//Yolo_S2w20T7//events//sheets//', type=str)
    parser.add_argument('-vIn', default=os.getcwd() + '//video.mp4', type=str)
    parser.add_argument('timeDetectAis', type=float)
    parser.add_argument('-um', default=0.85,type=float)
    args = parser.parse_args()
    ##################################################################################################################################
    #paramYolo=['D:\YOLO_CL\yoloApps.exe', 'detect', '-M', '5',  YOLO_CONFIG, YOLO_WEIGHTS, '-cnn', '-v',  args.vIn, '-media', args.dirStY,  '-MB', '2100',  '-i', '0',  '-w', '30', '-t', '0',  '-schedule',  '-knn']
    aisContain = ContainerRN()
    yoloContain = ContainerRN()
    runAlgAis(args.dirA , aisContain, args.um, args.timeDetectAis, args.dirStA)
    runAlgYolo(args.dirY, args.dirStY, yoloContain, args.vIn)
    printValues(yoloContain, aisContain)
# end main

if __name__ == "__main__":
    main()