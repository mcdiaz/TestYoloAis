#Este programa resolveria el problema del trackeo por el algoritmo de Substraccion de fondo; buscando y "matcheando" los
#TB que pertenezcan realmente al mismo objeto en el video original.

import os
import subprocess
import time
from datetime import datetime
import json
import csv

#TIME_INIT_VIDEO=datetime(0,0,0,0)
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
    def takeInitPos(elem):
        return datetime.strptime(elem[atribute],'%Y-%m-%d %H:%M:%S.%f').time()
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
    if not objData['init'].__contains__("."):#si no tienen milisegundos, se los "setea en 0"
        objData['init'] = "{0}{1}{2}".format(objData['init'], ".", str(0))
    if not objData['finish'].__contains__("."):#si no tienen milisegundos, se los "setea en 0"
        objData['finish'] = "{0}{1}{2}".format(objData['finish'], ".", str(0))
    LIST_JSON.append(objData)#agrega el objeto json encontrada al final
# end function

def readAndSortJsons(dirJsons):
    #Toma del archivo json pasado por parametro, el atributo "data" que es un tipo lista/arreglo y lo recorre
    #por cada "elemento" dentro de data, los manda a parsear, ya que son objetos tipo json y sus atributos se tienen
    #que pasar de string a json o hacer modificaciones correspondientes que se encarga la funcion readAndAddJson
    #que meramente coloca cada objeto json encontrado en data (ya modificado y todos) y los agrega de LIST_JSON
    #acá se la termina de ordenar ascendentemente por tiempo de inicio a escena.
    with open(dirJsons,'r') as fileJson:
        allJsons=json.loads(fileJson.read()) #lee toddo lo contenido en fileJson y lo parsea a un objeto json, guardandolo
        #en allJsons
        #por cada objeto que se encuentra en data, se lo envia a readAndAddJson
        for pos in allJsons['data']:
            readAndAddJson(pos)
        # end for
    # end with
    sortJsonList(LIST_JSON, 'init')#lista de tblobs tomados como objetos JSON, ordenados por el tiempo de inicio a escena
    #if LIST_JSON:
     #   TIME_INIT_VIDEO=LIST_JSON(0)['init']
    #print(LIST_JSON)
# end function

def totalTime(tblob):
    return tblob['init']
# end function

def foundedTimeMacth(tblob):
    for anotherTblob in (x for x in LIST_JSON if x['init'] in (tblob['init']-RANGE_TIME,tblob['init'],tblob['finish']+RANGE_TIME)):
        print(tblob," match con ",anotherTblob)

# end function

def matchingTblobs():
    for tblob in LIST_JSON:
        foundedTimeMacth(tblob)



def main():
    print('holi')
    readAndSortJsons(PATH_JSON)#llama al metodo que lee todos los objetos json encontrados en el archivo .json y los
    #agrega a LIST_JSON ordenados ascendentemente por tiempo de inicio a escena
    matchingTblobs()

if __name__ == '__main__':
    main()