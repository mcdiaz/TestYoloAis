import os
import subprocess
import io
import errno
import csv
import argparse

PATH_RUN_BAT_NEURAL_NET="F://YOLO//TestYoloAis//run-ScriptAis-RN1y2.bat"
PATH_TEST_IMAGES="D://Leo_Test_1//test_images//van//"
LABELS_RN6=list()
LABELS_RN124=list()
#Guardan en diccionario la cantidad de clasificaciones de los labels correspondientes a r1 y a r2
DICT_GT=dict()
DICT_RN6_1RO=dict()
DICT_RN124_1RO=dict()
DICT_RN6_2DO=dict()
DICT_RN124_2DO=dict()
SUBPROCESS_R1=subprocess
SUBPROCESS_R2=subprocess
THRESHOLD_MIN=50.0
THRESHOLD_MAX=10.0
LABEL_TEST='van'
LIST_WRONG_LABEL=list()



def loadLabels(listLabels,RN6,RN124):
    # procesar la salida del script de ais
    # primero lee la lista de las etiquetas que utiliza ais y las guarda en una lista propia del programa para luego
    # utilizarla como referencia de las etiquetas que se desea utilizar
    classif = ""
    for pos in range(0, listLabels.find(']'), 1):
        if (listLabels[pos] not in {"[", "'", ",", " "}):
            classif += listLabels[pos]
        elif classif != "":
            if RN6:
                LABELS_RN6.append(classif)
            elif RN124:
                LABELS_RN124.append(classif)
            classif = ""
        # end if
    # end for
    print(LABELS_RN6)
    print(LABELS_RN124)
# end function

def setBatFileAis(pathRunBat,pathImg,pathRN,pathTestImg,nameRN):
    contenido=""
    with open(pathRunBat,'r') as file:
        column=file.read().split(' ')
        for pos in range(1,len(column)):
            if column[pos-1]=='--im':
                column[pos]='"'+pathImg+'"'
                #break
            # end if
            elif column[pos-1]=='--nameRN':
                column[pos]='"'+nameRN+'"'
                #break
            # end if
            elif column[pos-1]=='--pathRN':
                column[pos]='"'+pathRN+'"'
                #break
            # end if
            elif column[pos-1]=='--pathTestImg':
                column[pos]='"'+pathTestImg+'"'
                print(pathTestImg)
                break
            # end if
        # end for
        contenido=' '.join(column)
    # end with
    with open(pathRunBat,'w') as file:
        file.write(contenido)
    # end with
# end function

def initSubprocess(pathFolderRN,pathRunRN,RN):
    stdin=()
    stdout=()
    if RN.__eq__(1):
        setBatFileAis(PATH_RUN_BAT_NEURAL_NET, "1", pathFolderRN, PATH_TEST_IMAGES,
                      pathRunRN)
        SUBPROCESS_R1 = subprocess.Popen([r'' + PATH_RUN_BAT_NEURAL_NET],shell=True, stdin=subprocess.PIPE,
                                         stdout=subprocess.PIPE)
        stdin = io.TextIOWrapper(
            SUBPROCESS_R1.stdin,
            encoding='utf-8',
            line_buffering=True,  # send data on newline
        )
        stdout = io.TextIOWrapper(
            SUBPROCESS_R1.stdout,
            encoding='utf-8',
        )
    elif RN.__eq__(2):
        setBatFileAis(PATH_RUN_BAT_NEURAL_NET, "2", pathFolderRN, PATH_TEST_IMAGES,
                      pathRunRN)
        SUBPROCESS_R2 = subprocess.Popen([r'' + PATH_RUN_BAT_NEURAL_NET], shell=True, stdin=subprocess.PIPE,
                                         stdout=subprocess.PIPE)
        stdin = io.TextIOWrapper(
            SUBPROCESS_R2.stdin,
            encoding='utf-8',
            line_buffering=True,  # send data on newline
        )
        stdout = io.TextIOWrapper(
            SUBPROCESS_R2.stdout,
            encoding='utf-8',
        )
    return stdin,stdout
# end function

def classifyImage(folderImage, classify, rn124):
    arrayClassify=classify.strip().replace(";","").split("|")
    label_1ro=str()
    label_2do=str()
    preciss_1ro=float()
    preciss_2do=float()
    if arrayClassify.__sizeof__().__ge__(1):
        firstPos = arrayClassify[0].split("_")
        label_1ro = firstPos[0]
        preciss_1ro = float(firstPos[1])
        if preciss_1ro.__le__(THRESHOLD_MIN) and arrayClassify.__sizeof__().__ge__(2):#si el primero es menor a 50
            secondPos = arrayClassify[1].split("_")
            label_2do= secondPos[0]
            preciss_2do = float(secondPos[1])
        if rn124:
            arrclass = folderImage.split("//")
            root=list(arrclass).pop(list(arrclass).__len__()-2) #root se vuelve el anteultimo elemento del arreglo que contiene
            #los elementos del path del folder, entonces se vuelve la etiqueta original
            if root.__ne__(label_1ro):
               LIST_WRONG_LABEL.append([folderImage,label_1ro,preciss_1ro])
    return label_1ro,label_2do
# end function

def loadDicc(classify, classRN):
    print(classify)
    if classRN.__eq__('GT'):
        # print(classify.split("\\"))
        arrclass = classify.split("\\")
        label = arrclass.pop()
        print(label)
        DICT_GT[LABEL_TEST] = (DICT_GT.get(LABEL_TEST) or 0) + 1
    else:
        label_1ro,label_2do=classify
        if label_1ro:
            if classRN.startswith("RN6000"):
                DICT_RN6_1RO[label_1ro]=(DICT_RN6_1RO.get(label_1ro) or 0)+1
            elif classRN.startswith("RN124000"):
                DICT_RN124_1RO[label_1ro] = (DICT_RN124_1RO.get(label_1ro) or 0) + 1
            #end if
        if label_2do:
            if classRN.startswith("RN6000"):
                DICT_RN6_2DO[label_2do]=(DICT_RN6_2DO.get(label_2do) or 0)+1
            elif classRN.startswith("RN124000"):
                DICT_RN124_2DO[label_2do] = (DICT_RN124_2DO.get(label_2do) or 0) + 1
            #end if

#end function

def classifyFolder(stdin,stdout,ClassRN,GT,RN6,RN124):
    # aca itera por las carpetas del gt en d\leo test 1\ y con cada path de cada img de cada carpeta, invoca a
    # runNeuralNet 1 y 2 y va dando las salidas en una tablita de formato csv
    #Antes de iterar por directorios y files, me aseguro que esté posicionada en la linea proxima a que la herramienta ais "lea la url",
    out = ""
    while out.__ne__("waiting\n"):
        out=str(stdout.readline())
        print(out)
        if out.startswith("[") and RN6:
            print("loadLabels")
            loadLabels(out,RN6,False)
        elif out.startswith("[") and RN124:
            print("loadLabels")
            loadLabels(out,False,RN124)
        # end if
    #end while
    # recorre todos los directorios y files que se encuentren en una ruta especifica
    print("Hola, tendria que comparar rns")
    for root, dirs, files in os.walk(PATH_TEST_IMAGES):
        # saltea el primer directorio, que es el directorio que estoy recorriendo
        if out.__eq__("waiting\n"):
        #if root != PATH_TEST_IMAGES and out.__eq__("waiting\n"): #forma de chequear con todos los labels
            # recorre todos los archivos contenidos en files
            for name in files:
                # encuentra una imagen"
                #if str(name).endswith(".jpg") or str(name).endswith(".jpeg"):
                folderImage=root + name
                print(folderImage)
                line = '{}\n'.format(folderImage)#es importante que este definido el formato del salto de linea, porque eso tambien genera que la herramienta no lo tome como url de imagen, porque no terminaria en .jpg o .jpeg
                stdin.write(line)
                stdin.flush()
                #wrAndReadRN(sub1.stdout.readline())
                output = stdout.readline()
                print(output.rstrip())
                if output.rstrip().__ne__(";ERROR"):#Si surgio algun error de la herramienta de clasificacion, no lo procesa
                    if RN124:
                       loadDicc(root,GT)#metodo que carga el diccionario correspondiente al GT de acuerdo al nombre que figura en el path pasado por parametro
                    loadDicc(classifyImage(folderImage,output,RN124),ClassRN)#se le manda el folder(que de ahi se podria verificar la clasificacion real)
                waiting = stdout.readline()  # waiting que espera la proxima escritura, "lo descarto"
                # end if
            # end for
        # end if
    # end for
    line = '{}\n'.format("close") #Le avisa al proceso hijo que no va a recibir mas
    stdin.write(line)
# end function

def generateResults():
    with open(LABEL_TEST+'_v2.0NO_resultRNs.csv', 'w') as csvfile:
        #rowNames = ['Label','YOLO','AIS','Time_YOLO','Time_AIS']
        rowNames = ['Label', 'GT', 'RN6000-Mayor50', 'RN6000-Menor50', 'RN124000-Mayor50', 'RN124000-Menor50']
        csv.register_dialect('delimiter',delimiter=';',lineterminator='\n')
        writer = csv.DictWriter(csvfile, fieldnames=rowNames, dialect='delimiter')
        writer.writeheader()
        #writer.writerows([{'Time_YOLO': yoloContain.finalTime, 'Time_AIS': aisContain.finalTime}])
        for label in LABELS_RN124:
            writer.writerows([{'Label': label, 'GT': int(DICT_GT.get(label) or 0),
                               'RN6000-Mayor50': int(DICT_RN6_1RO.get(label) or 0),
                               'RN6000-Menor50': int(DICT_RN6_2DO.get(label) or 0),
                               'RN124000-Mayor50': int(DICT_RN124_1RO.get(label) or 0),
                             'RN124000-Menor50':int(DICT_RN124_2DO.get(label) or 0)}])
            #valorYolo = int(yoloContain.dict.get(label) or 0)
            #valorAis = int(aisContain.dict.get(label) or 0)
            #print("{2}{0:^10s}{2}{2}{1:^10d}{2}{2}{3:^10d}{2}".format(label, valorYolo, "|", valorAis))
        for pos in LIST_WRONG_LABEL:
            writer.writerows([{'Label': pos[0], 'GT': pos[1],
                               'RN6000-Mayor50': pos[2]}])
        #writer.writerows([{'Label': 'Total_time', 'YOLO': yoloContain.finalTime, 'AIS': aisContain.finalTime}])
        #print("{1:^36s}".format("|", "____________________________________"))
        #print("{0}{1:^10s}{0}{0}{2:^10d}{0}{0}{3:^10d}{0}".format("|", "Total", yoloContain.amount, aisContain.amount))
        #print("{0}{1:^10s}{0}{0}{2:^10f}{0}{0}{3:^10f}{0}".format("|", "Tiempo", yoloContain.finalTime,
        #                                                          aisContain.finalTime))
    # end with
# end function

def main():
    #Primero para inicializar R1 y agregarlo al diccionario correspondiente
    stdin1,stdout1=initSubprocess("D://Leo_Test_1//60000//","retrained_graph.pb",1)
    classifyFolder(stdin1,stdout1,'RN6000','',True,False)
    stdin2,stdout2=initSubprocess("D://Leo_Test_1//124000//", "retrained_graph_v1.pb",2)
    classifyFolder(stdin2,stdout2,'RN124000','GT',False,True)
    generateResults()
    print("Hola, soy el main")
# end main

if __name__ == "__main__":
    main()