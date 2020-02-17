import sys
import os
import subprocess
from os.path import *
import re
import argparse
import json
import time
from datetime import datetime
import csv


class ContainerRN:
    def __init__(self):
        self.amount=0
        self.initTime=0
        self.finalTime=0
        self.dict={}
        self.jsObj=[] #los json de cada objeto ordenados por tiempo

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
        # se queda con el valor de clasificacion mayor y que sobrepase al threshold
        if valuePrecission == 0.0 and float(listLabels[i][1]) >= threshold or valuePrecission !=0.0 and \
                valuePrecission < float(listLabels[i][1]):
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
    # primero lee la lista de las etiquetas que utiliza ais y las guarda en una lista propia del programa para luego
    # utilizarla como referencia de las etiquetas que se desea utilizar
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

def get_milisec(time_HMS):
    # espera por parametro una variable datime.time de formato H:M:S y devuelve el valor correspondiente en milisegundos
    return (time_HMS.hour*3600 + time_HMS.minute*60 + time_HMS.second)/1000
# end function

def get_timeToDetect(folderData):
    # lee el file que contiene el tiempo final e inicial de la deteccion de yolo y la vuelca a la variable de timeDetAis
    contain=""
    with open(folderData,'r') as fileData:
        # toma la segunda linea que es sin la inicializacion del programa
        contain=list(fileData.readlines())[1]
    # end with
    contain=contain[contain.find(':') + +1 : len(contain)-1]
    #print("\n",contain,"print contain")
    # timeArr tiene dos posiciones: la primera el tiempo final del procesamiento de ais y el segundo, el tiempo inicial
    timeArr=contain.split('-')
    timeFinal=(str(timeArr[0]).encode("utf-8").decode("unicode-escape").encode("latin-1").decode("utf-8")).strip("'").strip()
    timeInit=(str(timeArr[1]).encode("utf-8").decode("unicode-escape").encode("latin-1").decode("utf-8")).strip("'").strip()
    tF=get_milisec(datetime.strptime(timeFinal,'%H:%M:%S').time())
    tI=get_milisec(datetime.strptime(timeInit,'%H:%M:%S').time())
    #print(tF,"-",tI,"timeFinal - timeInit")
    return float(tF - tI)
# end function

def loadAis(arrAis, aisContain, threshold, folderData):
    # recorre el arreglo correspondiente a la salida de ais y vuelca los datos en una instancia de ContainerRN
    # args:
    #   arrAis: arreglo correspondiente a la salida de ais
    #   ais: instancia de la clase ContainerRN
    for pos in range(0,len(arrAis)):
        if pos is 0:
            aisContain.finalTime= float(float(arrAis[pos]) + get_timeToDetect(folderData))
        elif pos is 1:
            aisContain.amount=int(arrAis[pos])
        else:
            # por cada posicion luego de las dos primeras, llama al metodo que completa el diccionario de ais
            readClasificate(arrAis[pos],aisContain, threshold)
        # end if
    # end for
    #print(get_timeToDetect(folderData),"TIME DET AIS EN LOADAIS")
    #print(aisContain.finalTime)
# end function

def runAlgAis(dirRunA,aisContain, threshold, folderData, folderStAis):
    # Ejecuta el script de AIS para detectar y clasificar todos los tb
    # En el script se realiza la iteracion por todas las carpetitas correspondientes a todos los tb detectados
    # El script devuelve un string de la forma "folderImgClasificada.jpg;CAR;0.8|BUS;0.1|TRUCK;0.1"
    # args:
    #    folderTB posee la ubicacion a la carpeta que posee cada carpeta para cada TB, que cada una de ellas contiene 5 archivos
    #    aisContain es una instancia de la clase ContainerRN, que contiene un diccionario con la cantidad de objetos
    #       detectados por cada clasificacion
    # asocia el script de ais para deteccion y clasificacion
    setBatFileAis(dirRunA,folderStAis)
    sub = subprocess.Popen([r''+dirRunA], stdout=subprocess.PIPE, shell=False)
    # calcula tiempo inicial
    print("aca toma el tiempo")
    #aisContain.initTime = time()
    # convierte caracteres de bytes a string de la salida del script de ais - elimina caracteres como 'b' o '\'
    resultPrint=(str(sub.stdout.read()).encode("utf-8").decode("unicode-escape").encode("latin-1").decode("utf-8"))
    resultPrint=resultPrint.replace(r"\r\n","")
    """
    resultPrint="['pickup', 'bus', 'car', 'cyclist', 'human', 'truck', 'van'];\r\n3.602055072784424;21;cyclist_46.22|pickup_34.62|human_6.40|car_5.25|van_4.75|truck_1.73|bus_1.03|;human_97.03|cyclist_2.95|bus_0.02|truck_0.00|van_0.00|pickup_0.00|car_0.00|;truck_54.41|pickup_15.22|bus_12.68|human_11.82|cyclist_4.52|car_0.90|van_0.45|;human_71.68|pickup_21.36|cyclist_6.62|car_0.22|truck_0.06|van_0.03|bus_0.02|;human_57.99|truck_24.39|pickup_8.19|bus_7.55|cyclist_1.55|van_0.20|car_0.12|;human_99.81|cyclist_0.17|truck_0.01|pickup_0.00|car_0.00|bus_0.00|van_0.00|;human_93.01|cyclist_6.83|bus_0.09|pickup_0.03|car_0.02|truck_0.01|van_0.01|;cyclist_95.17|bus_3.26|truck_1.04|human_0.37|pickup_0.11|van_0.03|car_0.02|;human_58.99|bus_26.69|cyclist_7.69|van_3.99|truck_2.27|pickup_0.28|car_0.09|;human_68.59|cyclist_28.10|bus_1.55|truck_1.11|pickup_0.52|car_0.08|van_0.05|;human_99.20|cyclist_0.62|truck_0.15|pickup_0.02|bus_0.01|car_0.00|van_0.00|;human_66.44|cyclist_33.25|truck_0.18|bus_0.09|pickup_0.03|van_0.01|car_0.00|;human_71.07|bus_13.01|van_10.08|cyclist_3.86|pickup_1.20|car_0.52|truck_0.27|;human_70.94|cyclist_14.27|pickup_8.90|truck_5.27|bus_0.28|van_0.23|car_0.10|;human_31.48|truck_22.16|bus_21.64|cyclist_12.64|pickup_6.89|van_3.09|car_2.10|;truck_79.07|human_10.33|bus_4.88|cyclist_4.81|pickup_0.78|car_0.09|van_0.05|;bus_36.80|truck_27.55|human_23.75|cyclist_11.17|van_0.52|car_0.15|pickup_0.05|;truck_78.81|human_10.80|bus_3.20|van_2.77|pickup_2.56|car_1.23|cyclist_0.62|;human_32.92|van_26.99|truck_19.32|cyclist_11.62|bus_7.90|pickup_1.05|car_0.19|;human_71.53|truck_24.49|cyclist_3.78|pickup_0.11|bus_0.10|car_0.00|van_0.00|;bus_61.37|truck_19.98|cyclist_10.96|human_7.57|pickup_0.09|car_0.02|van_0.02|\r\n"
    """
    resultPrint = resultPrint[int(resultPrint.find('[')):int(len(resultPrint))]
    loadLabels(resultPrint)
    # se llama al metodo que procesa los primeros caracteres desde el primer [ hasta el proximo ] para cargar los labels
    # correspondientes a las clasificaciones que se estudiaran
    # se salta todos los caracteres hasta ']'
    resultPrint = resultPrint[int(resultPrint.find(']')) + 1:int(len(resultPrint))]
    # se separa el string por ';' en elementos de un arreglo
    resultArray=resultPrint.split(";")
    resultArray.remove("")
    # Se recorre el resto del string pasado por ais para obtener la clasificacion con su precision de cada objeto
    loadAis(resultArray, aisContain, threshold, folderData)
    readAndSortJsons(folderStAis, aisContain)
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
    # loadDicYOLO lee las carpetitas que contienen los json generados por la salida de la red YOLO
    # y vuelca los datos al diccionario correspondiente al objeto yolo del programita
    # args:
    #   folderYOLO: localizacion de las carpetitas de los json que genera la deteccion y clasificacion de la red yolo
    #   yoloContain: instancia de la clase ContainerRN
    print(folderYOLO)
    for root, dirs, files in os.walk(folderYOLO+'//events//sheets//'):
        #print(files,'files')
        dirs[:] = [d for d in dirs if not d.format('4:d-2:d-2d')]
        for name in files:
            if str(name).endswith('.json'):
                #print(name, "names in loadDicYOLO")
                labelObj=getLabelDicYolo(str(name).split("_")[3], yoloContain)
                value = int(yoloContain.dict.get(labelObj) or 0)
                checkLabel(labelObj,value,yoloContain)
                yoloContain.amount+=1
                #addSort(yoloContain,folderYOLO+name)
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
    ###p=subprocess.Popen(paramYolo)
    setBatFileYolo(dirRunYolo,dirStoreYolo, dirVideoIn)
    p=subprocess.Popen([r''+dirRunYolo])
    # calcula el tiempo inicial
    yoloContain.initTime=time.time()
    p.communicate()
    yoloContain.finalTime = time.time() - yoloContain.initTime
    # llama a la funcion encargada de volcar los datos leidos al diccionario de yolo
    loadDicYOLO(dirStoreYolo, yoloContain)
    # Calcula el tiempo final de ejecucion de la red densa
    print(yoloContain.finalTime)
    readAndSortJsons(dirStoreYolo, yoloContain)
# end function

def printValues(yoloContain, aisContain):
    # Este metodo imprime una tabla de la forma Yolo | AIS | Human
    # Volcando los datos de la cantidad de objetos detectados y clasificados
    # args:
    #   yoloContain: instancia de la clase ContainerRN, correspondiente al contenido de yolo
    #   aisContain: idem anterior, correspondiente al contenido de ais
    print("{1:^36s}".format("|", "____________________________________"))
    print("{4}{0:10s}{4}{4}{2:^10s}{4}{4}{3:^10s}{4}".format(" ", "\n", "YOLO", "AIS", "|"))
    print("{2}{0:^10s}{2}{2}{1:^22s}{2}".format("Etiqueta", "Valor", "|"))
    with open('compareResult.csv', 'w') as csvfile:
        #rowNames = ['Label','YOLO','AIS','Time_YOLO','Time_AIS']
        rowNames = ['Label', 'YOLO', 'AIS']
        writer = csv.DictWriter(csvfile, fieldnames=rowNames)
        writer.writeheader()
        #writer.writerows([{'Time_YOLO': yoloContain.finalTime, 'Time_AIS': aisContain.finalTime}])
        for label in LABELS:
            writer.writerows([{'Label': label, 'YOLO': int(yoloContain.dict.get(label) or 0),
                               'AIS': int(aisContain.dict.get(label) or 0) }])

            valorYolo = int(yoloContain.dict.get(label) or 0)
            valorAis = int(aisContain.dict.get(label) or 0)
            print("{2}{0:^10s}{2}{2}{1:^10d}{2}{2}{3:^10d}{2}".format(label, valorYolo, "|", valorAis))

        # end for
        labelsYolo = set.difference(set(yoloContain.dict.keys()), LABELS)
        # por todas las etiquetas diferentes que posee yolo y no se encuentra en labels, las imprime con su valor
        for labelYolo in labelsYolo:
            writer.writerows([{'Label': labelYolo, 'YOLO': int(yoloContain.dict.get(labelYolo) or 0),
                               'AIS': 0}])

            print("{2}{0:^10s}{2}{2}{1:^10d}{2}{2}{3:^10d}{2}".format(label, yoloContain.dict.get(label), "|", 0))

        # end for

        writer.writerows([{'Label': 'Total_time', 'YOLO': yoloContain.finalTime, 'AIS': aisContain.finalTime}])

        print("{1:^36s}".format("|", "____________________________________"))
        print("{0}{1:^10s}{0}{0}{2:^10d}{0}{0}{3:^10d}{0}".format("|", "Total", yoloContain.amount, aisContain.amount))
        print("{0}{1:^10s}{0}{0}{2:^10f}{0}{0}{3:^10f}{0}".format("|", "Tiempo", yoloContain.finalTime,
                                                                  aisContain.finalTime))

    # end with
    """
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
    """
# end function

####################################################################################################################################
# modifican los batch file que ejecutan los comandos de yolo y ais respectivamente
def setBatFileAis(folderRunBat, folderStore):
    contenido=""
    with open(folderRunBat,'r') as file:
        column=file.read().split(' ')
        for pos in range(1,len(column)):
            if column[pos-1]=='--dir':
                column[pos]='"'+folderStore+'"'
                break
            # end if
        # end for
        contenido=' '.join(column)
    # end with
    with open(folderRunBat,'w') as file:
        file.write(contenido)
    # end with
# end function

def setBatFileYolo(folderRunBat, folderStore, folderVideo):
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
#######################################################################################################################

#######################################################################################################################
# leer los json el directorio que contiene todos y cada uno por vez
def sortJsonList(listJson, atribute):
    """
    initTime=datetime.strptime(jsObj['init'],'%Y-%m-%d %H:%M:%S.%f').time()
    finishTime=datetime.strptime(jsObj['finish'],'%Y-%m-%d %H:%M:%S.%f').time()
    #insertar ordenado en objContain.jsObj() por time
    if objContain.jsObj:
    # si la lista de json no esta vacia
        for obj in objContain.jsObj:
        # recorre toda la lista de objetos json ya ubicados y añade el nuevo de forma ordenada ascendentemente
            initObj=(obj['init'], '%Y-%m-%d %H:%M:%S.%f').time()
            if initTime.__le__(initObj):
                print(initTime, "-", finishTime)
    """
    #for obj in objContain.jsObj:
    # recorrido de todos los json desordenados por fecha
    #    print("Todos desordenados")
    #    print(obj['init'])
    # funcion y metodo de ordenamiento, para ordenar todos los json ubicados en la lista correspondiente a la instancia de ContainerRN segun tiempo de entrada a escena
    def takeInitPos(elem):
        return datetime.strptime(elem[atribute],'%Y-%m-%d %H:%M:%S.%f').time()
    # end function
    listJson.sort(key=takeInitPos)
    print("#################################### Todos ordenados ######################################################")
    for obj in listJson:
    # recorrido de todos los json ordenados por fecha de forma ascendente
        print(obj['init'])
# end function

def readAndAddJson(objContain, folderJson):
    # lee los json ubicados en la direccion de folderJson, los procesa y llama al metodo addSort para guardarlos ordenados en la intancia objContain de ContainerRN
    if str(folderJson).endswith('.json'):
        findedJson=json
        with open(folderJson,'r') as fileJson:
            findedJson=json.loads(fileJson.read())
            # llamado al metodo para que ordene la lista de blobs por el atributo de time de forma ascendente
            #sortJsonList(findedJson['blob'],'time')
            objContain.jsObj.append(findedJson)
        # end with
    # end if
# end function

def readAndSortJsons(dirJsons, objContain):
    for root, dirs, files in os.walk(dirJsons):
        for file in files:
            readAndAddJson(objContain,dirJsons+"\\"+file[0 : int(file.find('_'))]+"\\"+file)
        # end for
    # end for
    sortJsonList(objContain.jsObj, 'init')
# end function
#######################################################################################################################

def main():
    # {etiqueta, cantidad de objetos detectados}
    ###################################################################################################################
    # args del algoritmo de comparacion
    parser = argparse.ArgumentParser()
    # parametro para que el usuario eliga que version de comparacion quiere usar (v1: normal por cantidad de obj
    # ; v2: por hora de obj ; v3: por espacio)
    parser.add_argument('-v', '--version', type=int, choices=[1,2,3])
    parser.add_argument('-dirA', default=os.getcwd() + '//run-ScriptAis-Py.bat', type=str)
    parser.add_argument('-dirStA', default='F://YOLO//Prueba_V1//2018-08-05//', type=str)
    parser.add_argument('-dirY', default=os.getcwd() + '//run-S2-Yolo3-w20.bat', type=str)
    parser.add_argument('-dirStY', default='F://YOLO//TestYoloAis//test_yolo//Yolo_S2w20T7//', type=str)
    parser.add_argument('-video', default='F://YOLO//Prueba_V1//2019-08-05_16-09-46.mp4', type=str)
    parser.add_argument('-timeDetAis', default='F://YOLO//Prueba_V1//datos.txt', type=str)
    parser.add_argument('-um', default=0.85,type=float)
    args = parser.parse_args()
    ###################################################################################################################
    #paramYolo=['D:\YOLO_CL\yoloApps.exe', 'detect', '-M', '5',  YOLO_CONFIG, YOLO_WEIGHTS, '-cnn', '-v',  args.vIn, '-media', args.dirStY,  '-MB', '2100',  '-i', '0',  '-w', '30', '-t', '0',  '-schedule',  '-knn']
    aisContain = ContainerRN()
    yoloContain = ContainerRN()
    #runAlgAis(args.dirA , aisContain, args.um, args.timeDetAis, args.dirStA)
    #runAlgYolo(args.dirY, args.dirStY, yoloContain, args.video)
    readAndSortJsons(args.dirStA, aisContain)
# end main

if __name__ == "__main__":
    main()