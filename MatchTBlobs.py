#Este programa resolveria el problema del trackeo por el algoritmo de Substraccion de fondo; buscando y "matcheando" los
#TB que pertenezcan realmente al mismo objeto en el video original.

import os
import subprocess
import time
from datetime import datetime, timedelta, time
import json
import csv

#TIME_INIT_VIDEO=datetime(0,0,0,0)
RANGE_TIME={'init':time(),'final':time()} #rango de tiempo que se comparan los tb adyacentes en linea de tiempo ordenados
COMPARE_MIN_TIME=100005 #strptime('0:0:0.5', '%H:%M:%S.%f').time() #minimo rango de tiempo a comparar: 5 microseg
PATH_JSON="D://CARO//Colon_Montevideo//testObjetos.json"
PATH_TBS_FOLDER="D://CARO//Colon_Montevideo//TBlobs//"
DICT_MATCH=dict() #resultado con los paths de imagen de recortes que matchean como resultado, de la forma {nameFolder,
# caracteristicas }
LIST_JSON=list() #lista que va a contener todos los json que se encuentren registrados en el csv, ordenados ascendentemente
TIME_INIT_VIDEO=time()
# por el atributo init de cada tb

# leer los json del directorio que contiene todos y agregarlos cada uno por vez
def sortJsonList(listJson, atribute):
    #ordena ascendentemente a todos los json segun tiempo de inicio al video
    #print(listJson)
    def takeInitPos(elem):
        return elem[atribute]
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
    #end if
    if not objData['finish'].__contains__("."):#si no tienen milisegundos, se los "setea en 0"
        objData['finish'] = "{0}{1}{2}".format(objData['finish'], ".", str(0))
    #end if
    #se agrega los tiempos de inicio y fin ya seteados en formato "time"
    objData['init']=datetime.strptime(objData['init'], '%Y-%m-%d %H:%M:%S.%f').time()
    objData['finish']=datetime.strptime(objData['finish'], '%Y-%m-%d %H:%M:%S.%f').time()
    LIST_JSON.append(objData)#agrega el objeto json, con todos sus atributos "parseados" encontrada al final
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
    if LIST_JSON:
        TIME_INIT_VIDEO=LIST_JSON[0]['init']
        RANGE_TIME['init']=TIME_INIT_VIDEO
        RANGE_TIME['final']=datetime.strptime(str(TIME_INIT_VIDEO.hour)+':'+str(TIME_INIT_VIDEO.minute)+':'+str(TIME_INIT_VIDEO.second)+'.'+str((TIME_INIT_VIDEO.microsecond + COMPARE_MIN_TIME))
                                              , '%H:%M:%S.%f').time()
     # END IF
    #print(LIST_JSON)
# end function

def totalTime(tblob):
    #devuelve el tiempo total que estuvo en escena en microseconds
    return dif_in_microseconds(tblob['init'],tblob['finish'])
# end function

def foundedTimeMacth(tblob):
    print('holi')
# end function

def dif_in_microseconds(time1,time2):
    #obtiene la diferencia en microsegundos de dos tiempos pasados por parametro
    h1, m1, s1, ms1 = time1.hour, time1.minute, time1.second, time1.microsecond
    h2, m2, s2, ms2 = time2.hour, time2.minute, time2.second, time2.microsecond
    t1_secs = s1 + 60 * (m1 + 60 * h1)
    t2_secs = s2 + 60 * (m2 + 60 * h2)
    t1_mcrs = ms1 + 1000000 * t1_secs
    t2_mcrs = ms2 + 1000000 * t2_secs
    print(t2_mcrs,t2_secs,t1_mcrs,t1_secs)
    print("Diferencia en segundos:",t2_secs - t1_secs) #diferencia en segundos
    print("Diferencia en micros:",t1_mcrs - t2_mcrs)
    print(h1,m1,s1,ms1,time1)
# end function

def matchingTblobs():
    dif_in_microseconds(LIST_JSON[0]['init'],LIST_JSON[1]['init'])
# end function

def main():
    print('holi')
    readAndSortJsons(PATH_JSON)#llama al metodo que lee todos los objetos json encontrados en el archivo .json y los agrega a LIST_JSON ordenados ascendentemente por tiempo de inicio a escena
    if LIST_JSON:#si se cargo correctamente LIST_JSON, entonces pasa a los chequeos del path que se pasó
        matchingTblobs()
    else:
        print("Ocurrió algún error no contemplado en el path que se pasó")
    # end if
# end main

if __name__ == '__main__':
    main()