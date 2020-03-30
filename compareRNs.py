import os
import subprocess
import io
import errno
import csv
import argparse

PATH_RUN_BAT_NEURAL_NET="F://YOLO//TestYoloAis//run-ScriptAis-RN1y2.bat"
LABELS_R1=[]
LABELS_R2=[]

def loadLabels(listLabels,labels):
    # procesar la salida del script de ais
    # primero lee la lista de las etiquetas que utiliza ais y las guarda en una lista propia del programa para luego
    # utilizarla como referencia de las etiquetas que se desea utilizar
    classif = ""
    for pos in range(0, listLabels.find(']'), 1):
        if (listLabels[pos] not in {"[", "'", ",", " "}):
            classif += listLabels[pos]
        elif classif != "":
            labels.append(classif)
            classif = ""
        # end if
    # end for
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
def compare(folder):
    # aca itera por las carpetas del gt en d\leo test 1\ y con cada path de cada img de cada carpeta, invoca a
    # runNeuralNet 1 y 2 y va dando las salidas en una tablita de formato csv
    result = ""
    #sub=runNeuralNet("", "D://CARO//Leo_Test_1//60000//", "retrained_graph.pb", "D://CARO//Leo_Test_1//test_images//")
    setBatFileAis(PATH_RUN_BAT_NEURAL_NET, "D://CARO//Leo_Test_1//test_images//animal//0_fa2b4f86-6908-493e-92f3-a187717a9283.jpg", "D://CARO//Leo_Test_1//60000//", "D:\\CARO\\Leo_Test_1\\test_images\\", "retrained_graph.pb")
    sub1 = subprocess.Popen([r'' + PATH_RUN_BAT_NEURAL_NET], stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=False)
    stdin = io.TextIOWrapper(
        sub1.stdin,
        encoding='utf-8',
        line_buffering=True,  # send data on newline
    )
    # recorre todos los directorios y files que se encuentren en una ruta especifica
    print("Hola, tendria que comparar rns")
    for root, dirs, files in os.walk(folder):
        # saltea el primer directorio, que es el directorio que estoy recorriendo
        out=str(sub1.stdout.readline().decode("utf-8"))
        if root != folder and out.__eq__("waiting\r\n"):
            # recorre todos los archivos contenidos en files
            for name in files:
                # encuentra una imagen"
                if str(name).endswith(".jpg") or str(name).endswith(".jpeg"):
                    folderImage=root + "\\" + name
                    print(folderImage)
                    stdin.write('"'+folderImage+'"')
                    stdin.flush()
                    #wrAndReadRN(sub1.stdout.readline())
                    output = sub1.stdout.readlines().decode('utf-8')
                    print(output.rstrip())
                    #sub1.stdout.flush()
                    #runNeuralNet(folderImage,pathRN,"retrained_graph.pb","D://CARO//Leo_Test_1//test_images//")
                    #runNeuralNet2(folderImage,"D://CARO//Leo_Test_1//1240000//","retrained_graph_v1.pb","D://CARO//Leo_Test_1//test_images//")
                # end if
            # end for
            sub1.stdin.write("close")
            remainder = sub1.communicate()[0].decode('utf-8')
            print(remainder)
        # end if
    # end for
# end function

def main():
    compare("D:\\CARO\\Leo_Test_1\\test_images\\")
    print("Hola, soy el main")
# end main

if __name__ == "__main__":
    main()