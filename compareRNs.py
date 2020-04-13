import os
import subprocess
import io
import errno
import csv
import argparse

PATH_RUN_BAT_NEURAL_NET="F://YOLO//TestYoloAis//run-ScriptAis-RN1y2.bat"
PATH_TEST_IMAGES="D:\\CARO\\Leo_Test_1\\test_images\\"
LABELS=list()
#Guardan en diccionario la cantidad de clasificaciones de los labels correspondientes a r1 y a r2
DICT_GT=dict()
DICT_RN6=dict()
DICT_RN124=dict()
SUBPROCESS_R1=subprocess
SUBPROCESS_R2=subprocess
THRESHOLD_MIN=15.0
THRESHOLD_MAX=35.0

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
    print(LABELS)
# end function

def setBatFileAis(pathRunBat,pathImg,pathRN,pathTestImg,nameRN):
    contenido=""
    with open(pathRunBat,'r') as file:
        column=file.read().split(' ')
        for pos in range(1,len(column)):
            if column[pos-1]=='--im':
                column[pos]='"'+pathImg+'"'
                break
            # end if
            if column[pos-1]=='--nameRN':
                column[pos]='"'+nameRN+'"'
                break
            # end if
            if column[pos-1]=='--pathRN':
                column[pos]='"'+pathRN+'//"'
                break
            # end if
            if column[pos-1]=='--pathTestImg':
                column[pos]='"'+pathTestImg+'//"'
                break
            # end if
        # end for
        contenido=' '.join(column)
    # end with
    with open(pathRunBat,'w') as file:
        file.write(contenido)
    # end with
# end function

def runNeuralNet(path_img,pathRN,pathTestImg,nameRN):
    setBatFileAis(PATH_RUN_BAT_NEURAL_NET,path_img,pathRN,pathTestImg,nameRN)
    sub1 = subprocess.Popen([r''+PATH_RUN_BAT_NEURAL_NET],stdin=subprocess.PIPE,stdout=subprocess.PIPE, shell=False)
    return sub1
# end function

def wrAndReadRN(outputRN):
    #sub.stdin.write(path_img)
    resultPrint = (str(outputRN).encode("utf-8").decode("unicode-escape").encode("latin-1").decode("utf-8"))
    resultPrint = resultPrint.replace(r"\r\n", "")
    resultPrint = resultPrint[int(resultPrint.find('[')):int(len(resultPrint))]
    print(resultPrint)
    #if LABELS_R1.clear():
    #    loadLabels(resultPrint,LABELS_R1)
    #resultArray = resultPrint[int(resultPrint.find(']')) + 1:int(len(resultPrint))].split(";").remove("")
#end function
"""
def runNeuralNet2(path_img,pathRN,pathTestImg,nameRN):
    setBatFileAis(PATH_RUN_BAT_NEURAL_NET, path_img,pathRN,pathTestImg,nameRN)
    sub = subprocess.Popen([r''+PATH_RUN_BAT_NEURAL_NET],stdout=subprocess.PIPE, shell=False)
    resultPrint = (str(sub.stdout.read()).encode("utf-8").decode("unicode-escape").encode("latin-1").decode("utf-8"))
    resultPrint = resultPrint.replace(r"\r\n", "")
    resultPrint = resultPrint[int(resultPrint.find('[')):int(len(resultPrint))]
    print(resultPrint)
    if LABELS_R2.clear():
        loadLabels(resultPrint,LABELS_R2)
    #resultArray = resultPrint[int(resultPrint.find(']')) + 1:int(len(resultPrint))].split(";").remove("")
#end function
"""
def initSubprocess(pathFolderRN,pathRunRN,RN):
    setBatFileAis(PATH_RUN_BAT_NEURAL_NET, "1", pathFolderRN, PATH_TEST_IMAGES,
                  pathRunRN)
    stdin=()
    stdout=()
    if RN.__eq__(1):
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
    else:
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

def classifyImage(folderImage, classify, classRN):
    arrayClassify=classify.strip().replace(";","").split("|")
    label=""
    preciss=0.0
    if arrayClassify.__sizeof__().__ge__(1):
        firstPos = arrayClassify[0].split("_")
        label = firstPos[0]
        preciss = float(firstPos[1])
    print(arrayClassify)

    """
    #para comparar la precission de los labels
    if arrayClassify.__sizeof__().__ge__(2):
        firstPos=arrayClassify[0].split("_")
        secondPos=arrayClassify[1].split("_")
        firstLabel=firstPos[0]
        firstPress=float(firstPos[1])
        secondLabel=secondPos[0]
        secondPress=float(secondPos[1])
        if float(abs(firstPress-100.0)).__le__(THRESHOLD_MIN):
            
    """
    """
    #Recorre todas las posicciones de arrayClassify, para luego comparar
    for pos in arrayClassify:
        if pos.__ne__(''):
            arrLabel=pos.split("_")
            if label.__eq__("") or label.__ne__("") and arrLabel[1].__ge__(porc):
                porc=arrLabel[1]
                label=arrLabel[0]
            # end if
        # end if
    # end for
    """
    return label
# end function

def loadDicc(classify, classRN):
    if classRN.startswith("RN6000"):
        DICT_RN6[classify]=(DICT_RN6.get(classify) or 0)+1
    elif classRN.startswith("RN124000"):
        DICT_RN124[classify] = (DICT_RN124.get(classify) or 0) + 1
    else:
        #print(classify.split("\\"))
        arrclass=classify.split("\\")
        label=arrclass.pop()
        print(label)
        DICT_GT[label]=(DICT_GT.get(label) or 0) + 1
    #end if

#end function

def classifyFolder(stdin,stdout,ClassRN,GT):
    # aca itera por las carpetas del gt en d\leo test 1\ y con cada path de cada img de cada carpeta, invoca a
    # runNeuralNet 1 y 2 y va dando las salidas en una tablita de formato csv
    #Antes de iterar por directorios y files, me aseguro que esté posicionada en la linea proxima a que la herramienta ais "lea la url",
    out = ""
    while out.__ne__("waiting\n"):
        out=str(stdout.readline())
        print(out)
        if out.startswith("[") and LABELS.__eq__(False) :
            print("loadLabels")
            loadLabels(out)
        # end if
    #end while
    # recorre todos los directorios y files que se encuentren en una ruta especifica
    print("Hola, tendria que comparar rns")
    for root, dirs, files in os.walk(PATH_TEST_IMAGES):
        # saltea el primer directorio, que es el directorio que estoy recorriendo
        if root != PATH_TEST_IMAGES and out.__eq__("waiting\n"):
            # recorre todos los archivos contenidos en files
            for name in files:
                # encuentra una imagen"
                if str(name).endswith(".jpg") or str(name).endswith(".jpeg"):
                    folderImage=root + "\\" + name
                    print(folderImage)
                    line = '{}\n'.format(folderImage)#es importante que este definido el formato del salto de linea, porque eso tambien genera que la herramienta no lo tome como url de imagen, porque no terminaria en .jpg o .jpeg
                    stdin.write(line)
                    stdin.flush()
                    #wrAndReadRN(sub1.stdout.readline())
                    output = stdout.readline()
                    print(output.rstrip())
                    if GT.__ne__(''):
                        loadDicc(root,GT)#metodo que carga el diccionario correspondiente al GT de acuerdo al nombre que figura en el path pasado por parametro
                    loadDicc(classifyImage(folderImage,output,ClassRN),ClassRN)#se le manda el folder(que de ahi se podria verificar la clasificacion real)
                    waiting = stdout.readline()  # waiting que espera la proxima escritura, "lo descarto"
                # end if
            # end for
        # end if
    # end for
    line = '{}\n'.format("close") #Le avisa al proceso hijo que no va a recibir mas
    stdin.write(line)
# end function

def generateResults():
    with open('resultRNs.csv', 'w') as csvfile:
        #rowNames = ['Label','YOLO','AIS','Time_YOLO','Time_AIS']
        rowNames = ['Label', 'GT', 'RN6000', 'RN124000']
        writer = csv.DictWriter(csvfile, fieldnames=rowNames)
        writer.writeheader()
        #writer.writerows([{'Time_YOLO': yoloContain.finalTime, 'Time_AIS': aisContain.finalTime}])
        for label in LABELS:
            writer.writerows([{'Label': label, 'GT': int(DICT_GT.get(label) or 0),
                               'RN6000': int(DICT_RN6.get(label) or 0),
                               'RN124000': int(DICT_RN124.get(label) or 0)}])
            #valorYolo = int(yoloContain.dict.get(label) or 0)
            #valorAis = int(aisContain.dict.get(label) or 0)
            #print("{2}{0:^10s}{2}{2}{1:^10d}{2}{2}{3:^10d}{2}".format(label, valorYolo, "|", valorAis))
        #writer.writerows([{'Label': 'Total_time', 'YOLO': yoloContain.finalTime, 'AIS': aisContain.finalTime}])
        #print("{1:^36s}".format("|", "____________________________________"))
        #print("{0}{1:^10s}{0}{0}{2:^10d}{0}{0}{3:^10d}{0}".format("|", "Total", yoloContain.amount, aisContain.amount))
        #print("{0}{1:^10s}{0}{0}{2:^10f}{0}{0}{3:^10f}{0}".format("|", "Tiempo", yoloContain.finalTime,
        #                                                          aisContain.finalTime))
    # end with
# end function

def main():
    #Primero para inicializar R1 y agregarlo al diccionario correspondiente
    stdin1,stdout1=initSubprocess("D://CARO//Leo_Test_1//60000//","retrained_graph.pb",1)
    classifyFolder(stdin1,stdout1,'RN6000','GT')
    stdin2,stdout2=initSubprocess("D://CARO//Leo_Test_1//124000//", "retrained_graph_v1.pb",2)
    classifyFolder(stdin2,stdout2,'RN124000','')
    generateResults()
    print("Hola, soy el main")
# end main

if __name__ == "__main__":
    main()