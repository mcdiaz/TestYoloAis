#Este programa resolveria el problema del trackeo por el algoritmo de Substraccion de fondo; buscando y "matcheando" los
#TB que pertenezcan realmente al mismo objeto en el video original.

import os
import subprocess
import time
from datetime import datetime
import json
import csv

RANGE_TIME=0.05 #rango de tiempo que se comparan los tb adyacentes en linea de tiempo ordenados
PATH_JSON="D:\\CARO\\Colon_Montevideo\\testObjetos.json"
PATH_TBS_FOLDER="D:\\CARO\\Colon_Montevideo\\TBlobs\\"
DICT_MATCH=dict() #resultado con los paths de imagen de recortes que matchean como resultado, de la forma {nameFolder,
# caracteristicas }
LIST_JSON=list() #lista que va a contener todos los json que se encuentren registrados en el csv, ordenados ascendentemente
# por el atributo init de cada tb

# leer los json del directorio que contiene todos y agregarlos cada uno por vez
def sortJsonList(listJson, atribute):
    #ordena ascendentemente a todos los json segun tiempo de inicio al video
    #print(listJson)
    def takeInitPos(elem):
        return datetime.strptime(elem[atribute],'%Y-%m-%d %H:%M:%S.%f').time()
    # end function
    listJson.sort(key=takeInitPos)
    #print("#################################### Todos ordenados ######################################################")
# end function

def readAndAddJson(findedJson):
    #Aca por cada objeto json que se envia, se deberia parsear los atributos de color,shape y snapshot_data
    ######
    #    findedJson=json.loads(fileJson.read())#parsea el json que contiene los atributos del TB
        # llamado al metodo para que ordene la lista de blobs por el atributo de time de forma ascendente
        blobs=json.loads(findedJson['blobs'])#parsea la lista de blobs a objeto json
        sortJsonList(blobs,'time')#Ordena todos los blobs del TB identificado dentro del json y los ordena por 'time'
        findedJson['blobs']=blobs
        LIST_JSON.append(findedJson)#agrega el objeto json encontrada al final
    # end function

def readAndSortJsons(dirJsons):
    with open(dirJsons,'r') as fileJson:
        allJsons=json.loads(fileJson.read()) #lee toddo lo contenido en fileJson y lo parsea a un objeto json, guardandolo
        #en allJsons
        data=json.loads(allJsons['data']) #transforma el atributo de allJsons, llamado 'data', en un objeto json
        for json in data:
            readAndAddJson(json)
        # end for
    # end with
    sortJsonList(LIST_JSON, 'init')
# end function

def main():
    print('holi')
    readAndSortJsons(PATH_TBS_FOLDER)

if __name__ == '__main()__':
    main()