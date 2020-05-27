#Este programa resolveria el problema del trackeo por el algoritmo de Substraccion de fondo; buscando y "matcheando" los
#TB que pertenezcan realmente al mismo objeto en el video original.

import os
import subprocess
import time
from datetime import datetime
import json
import csv

RANGE_TIME=0.05 #rango de tiempo que se comparan los tb adyacentes en linea de tiempo ordenados
PATH_JSON="D://CARO//Colon_Montevideo//testObjetos.json"
PATH_TBS_FOLDER="D://CARO//Colon_Montevideo//TBlobs//"
DICT_MATCH=dict() #resultado con los paths de imagen de recortes que matchean como resultado, de la forma {nameFolder,
# caracteristicas }
LIST_JSON=list() #lista que va a contener todos los json que se encuentren registrados en el csv, ordenados ascendentemente
# por el atributo init de cada tb

# leer los json del directorio que contiene todos y agregarlos cada uno por vez
def sortJsonList(listJson, atribute):
    #ordena ascendentemente a todos los json segun tiempo de inicio al video
    #print(listJson)
    modAtribute=""
    def takeInitPos(elem):
        print(elem[atribute])
        if elem[atribute].__contains__("."):
            modAtribute=elem[atribute]
        else:
            modAtribute="{0}{1}{2}".format(elem[atribute],".",str(0))
        print(modAtribute)
        return datetime.strptime(modAtribute,'%Y-%m-%d %H:%M:%S.%f').time()
    # end internal function
    listJson.sort(key=takeInitPos)
    #print("#################################### Todos ordenados ######################################################")
# end function

def readAndAddJson(objData):
    #Aca por cada objeto json que se envia, se deberia parsear los atributos de color,shape y snapshot_data
    ######
    # llamado al metodo para que ordene la lista de blobs por el atributo de time de forma ascendente
    #findedJson=json.load('color','shape','snapshot') #parsea el json que contiene los atributos del TB
    color=json.loads(objData['color'])#parsea la lista de colors a objeto json
    shape = json.loads(objData['shape'])  # parsea la lista de shapes a objeto json
    snapshot = json.loads(objData['snapshot_data'])  # parsea la lista de snapshots a objeto json
    objData['color']=color
    objData['shape'] = shape
    objData['snapshot'] = snapshot
    LIST_JSON.append(objData)#agrega el objeto json encontrada al final
# end function

def readAndSortJsons(dirJsons):
    with open(dirJsons,'r') as fileJson:
        allJsons=json.loads(fileJson.read()) #lee toddo lo contenido en fileJson y lo parsea a un objeto json, guardandolo
        #en allJsons
        #por cada objeto que se encuentra en data, se lo envia a readAndAddJson
        for pos in allJsons['data']:
            readAndAddJson(pos)
        # end for
    # end with
    sortJsonList(LIST_JSON, 'init')
    print(LIST_JSON)

# end function

def main():
    print('holi')
    readAndSortJsons(PATH_JSON)

if __name__ == '__main__':
    main()