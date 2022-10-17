import gzip
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from dbscan import *
from aoi import *
import PySimpleGUI as sg


# Funzione usata per scegliere il tipo di grafico che si vuole andare a creare e visualizzare
def chooseGraph(char,scene):
    while True:

        #choose = input("Digita l'opzione scelta: ")
        choose = sg.popup_get_text('''Quale grafico vuoi creare e visualizzare?
        1. Grafico a barre per la media dell'occhio sinistro e destro nel tempo
        2. Grafico a barre per la media dell'occhio sinistro e destro per ogni scena
        3. Grafico a barre per il numero di fissazioni nel tempo
        4. Grafico a barre per il numero di aree di interesse nel tempo
        5. Grafico a barre per l' AOI dominante nel tempo
        ''', 'Creazione grafici a barre')
        if choose == str(1):
            rangeMin,rangeMax = openGazeData(char,1)
            barGraphAvgLFandRG(rangeMin,rangeMax)
        elif choose == str(2):
            durScene = openGazeData(char,2)
            barGraphEachScene(durScene)
        elif choose == str(3):
            print("Numero di fissazioni nel tempo")
            inter, listTime = openGazeData(char,3)
            barGraphFix(inter,listTime)
        elif choose == str(4):
            print("Numero di aree di interesse nel tempo")
            inter, listTime = openGazeData(char,3)
            barGraphAoi(inter,listTime)
        elif choose == str(5):
            print("Aoi dominante nel tempo")
            timePoint = readAoiDbscan2(scene)
            inter, listTime = openGazeData(char,4)
            barGraphAoiDominant(listTime, timePoint)
        elif choose == "":
            break
        else:
            print("Numero o parola inserita non valida. ")
    


# Funzione creata per leggere i valori del file gazedata del video corrispondente
# Restituisce l'intervallo di tempo
def openGazeData(char,choose):

    with gzip.open('dataGaze/gazedata'+str(char)+'.gz') as f1:
        time = []
        for data in f1:
            d = json.loads(data)
            timestamp = d.get('timestamp')
            time.append(timestamp)
        

        if(choose == 1):
            msg = "Scegli un intervallo di tempo tra " + str(time[0]) + " e " + str(time[len(time)-1])
            rangeMin = float(sg.popup_get_text(message=msg + " \nInserisci l'intervallo di tempo inferiore" ,title="Media dell'occhio sinistro e destro nel tempo"))
            rangeMax = float(sg.popup_get_text("Inserisci l'intervallo di tempo superiore","Media dell'occhio sinistro e destro nel tempo"))
            
            print(rangeMin,rangeMax)
            return rangeMin,rangeMax
        elif(choose == 2):
            msg = "Scegli la durata di ogni scena:"
            dur = float(sg.popup_get_text(message=msg + "\nInserisci la durata della scena" ,title="Media dell'occhio sinistro e destro per ogni scena"))
            print(dur)
            return dur
        elif(choose == 3) or (choose == 4) or (choose == 5):
            # L'utente deve scegliere quanti intervalli temporali vuole
            listTime = []
            listTime.append(0)
            inter = []
            num = int((sg.popup_get_text(message="Inserisci il numero di intervalli" ,title="Numero di fissazioni nel tempo")))
            print(num)
            for i in range(num):
                for j in time:
                    maxTime = round(j, 1)
                msg = "Scegli tra " + str(listTime[i-1]) + " e " + str(maxTime)
                
                if i == num - 1:
                    helpTime = maxTime
                else:
                    helpTime = float((sg.popup_get_text(message=msg + "\nInserisci" ,title="Numero di fissazioni nel tempo")))
                numTime = (str(listTime[i]) + '-' + str(helpTime))
                listTime.append(helpTime)
                inter.append(numTime)
            return inter, listTime



# Funzione che restituisce il grafico della media dell'occhio sinistro e destro combinati all'interno di un intervallo di tempo specificato
def barGraphAvgLFandRG(rangeMin,rangeMax):
    dataFrame = pd.read_csv('out/pupil.csv')             # Lettura del file .csv e salvataggio del dataframe
    data = dataFrame.iloc[:, [0,3]].values                 # Prendo i valori che mi serviranno dal dataframe
    fig, ax = plt.subplots(num='Media tra occhio destro e sinistro', figsize=(12, 8))                 # Creo una figura con dimensione 1.200 e 800

    print("I range sono %f e %f" %(rangeMin,rangeMax))

    rangeSelected = []#Lista con i timestamp nel range scelto
    rangeTempSelected = [element for element in data[:, 0]]#Lista temporanea di tutti i timestamp
    index = []#Indice del range
    averageTemp = [element for element in data[:, 1]]#Lista temporanea di tutte le medie
    average = []#Lista con le medie all'interno del range

    #Loop per trovarmi i valori del range scelto e per salvare i loro indici 
    for element,elemAvg in zip(rangeTempSelected,averageTemp):
        if(rangeMin<=element<=rangeMax):
            rangeSelected.append(element)
            index.append(rangeTempSelected.index(element))
            average.append(elemAvg)# Lista con i valori medi nel range selezionato 
 
    numBar = np.arange(len(average))
    # Genera Le barre
    bar_plot = plt.bar(numBar,average,width=0.5) 
    
    # Ruota le label dell'asse x di 90 gradi
    plt.xticks([r for r in numBar], np.round(rangeSelected,2), rotation=90) 
    
    
    # Funzione per generare le label sulle bar
    def autolabel(rects):
        for idx,rect in enumerate(bar_plot):
            height = rect.get_height()
            ax.text(rect.get_x() + rect.get_width()/2., 0.5*height,
                    round(average[idx], 4),
                    ha='center', va='bottom', rotation=90)
    autolabel(bar_plot)

    # Dettagli del grafico
    plt.subplots_adjust(bottom= 0.2, top = 0.98)# Regola i margini
    plt.ylabel('Media occhio DX e SX',fontweight='bold', fontsize=15)
    plt.xlabel('Intervallo',fontweight='bold', fontsize=15)
    fig.savefig('grafic/graficAverageLeftAndRight.png')
    plt.grid()

    event, values = sg.Window('Dettagli grafico', [[sg.Image(filename='grafic/graficAverageLeftAndRight.png')]]).read(close=True)
  
    plt.show()
    

# Funzione che restituisce il grafico della media dell'occhio sinistro e destro combinati per ogni scena di durata scelta
def barGraphEachScene(durScene):
    dataFrame = pd.read_csv('out/pupil.csv')             # Lettura del file .csv e salvataggio del dataframe
    data = dataFrame.iloc[:, [0,3]].values                 # Prendo i valori che mi serviranno dal dataframe

    times = [element for element in data[:, 0]]#Lista dei timestamp
    avgLFRG = [element for element in data[:, 1]]#Lista delle medie
    listTimeScene = []
    listTimeSceneTemp = []
    listAvgScene = []
    listAvgSceneTemp = []
    durSceneTemp=durScene

    for time,avg in zip(times,avgLFRG):
        if(time<=durSceneTemp):
            listTimeSceneTemp.append(time)
            listAvgSceneTemp.append(avg)
            
        else:
            durSceneTemp += durScene
            listAvgScene.append(sum(listAvgSceneTemp)/len(listAvgSceneTemp))
            listAvgSceneTemp.clear()
            listTimeScene.append(listTimeSceneTemp[len(listTimeSceneTemp)-1])
            listAvgSceneTemp.clear()   
    
    print(listAvgScene)

    fig, ax = plt.subplots(num='Media tra occhio destro e sinistro', figsize=(12, 8))# Creo una figura con dimensione 1.200 e 800

    numBar = np.arange(len(listAvgScene))
    # Genera Le barre
    bar_plot = plt.bar(numBar,listAvgScene,width=0.5)
    print("numbar %s" %numBar)
    # Ruota le label dell'asse x di 90 gradi
    plt.xticks([r for r in numBar],np.round(listTimeScene,2), rotation=90)
    
    
    # Funzione per generare le label sulle bar
    def autolabel(rects):
        for idx,rect in enumerate(bar_plot):
            height = rect.get_height()
            ax.text(rect.get_x() + rect.get_width()/2., 0.5*height,
                    round(listAvgScene[idx],4),
                    ha='center', va='bottom', rotation=90)
    autolabel(bar_plot)

    # Dettagli del grafico
    plt.subplots_adjust(bottom= 0.2, top = 0.98)# Regola i margini
    plt.ylabel('Media occhio DX e SX',fontweight='bold', fontsize=15)
    plt.xlabel('Intervallo',fontweight='bold', fontsize=15)
    fig.savefig('grafic/graficAverageLeftAndRight.png')
    plt.grid()

    event, values = sg.Window('Dettagli grafico', [[sg.Image(filename='grafic/graficAverageLeftAndRight.png')]]).read(close=True)
    plt.show()


# Funzione che restituisce il grafico del numero delle fissazioni
# Parametri: inter = numero di intervalli di tempo; listTime = lista dei valori degli intervalli
def barGraphFix(inter,listTime):
    dataFrame = pd.read_csv('out/fixation.csv')                 # Dataframe del file .csv
    data = dataFrame.iloc[:, [0, 1, 3, 4]].values               # Prendo i valori che mi serviranno
    times = [element for element in data[:, 1]]
    time2 = []
    smin = 0
    numF = []

    # Loop per la dimensione della lista 'listTime'
    # Utilizzata per restituire una lista avente il numero di fissazioni per ogni intervallo
    for i in range(1, len(listTime)):
        for x in times:
            if x <= listTime[i]:
                time2.append(x)
                numFix = [int(element) for element in data[smin:len(time2), 1]]
        diff = len(time2) - smin
        smin = smin + diff
        numF.append(len(numFix))
        numFix.clear()
        time2.clear()

    # Dettagli del grafico
    fig, ax = plt.subplots(num='Conteggio Fissazioni',figsize=(12, 8))
    plt.bar(inter, numF, width=0.3)
    # Annotazioni per ogni barra che restituisce il numero di fissazioni
    for i in range(len(inter)):
        plt.annotate(numF[i], (-0.05 + i, numF[i]))
    plt.ylim([0, len(times)])
    plt.ylabel('Numero di Fissazioni',fontweight='bold', fontsize=15)
    plt.xlabel('Intervalli (s)',fontweight='bold', fontsize=15)
    plt.title('Grafico Numero di Fissazioni')
    fig.savefig('grafic/graficNumFissazioni.png')

    event, values = sg.Window('Dettagli grafico', [[sg.Image(filename='grafic/graficNumFissazioni.png')]]).read(close=True)
    plt.show()

# Funzione che restituisce il grafico del numero di Aoi.
# Parametri: inter = numero di intervalli; listTime = lista dei valori temporali per ogni intervallo
def barGraphAoi(inter,listTime):
    df = pd.read_csv('out/fixation.csv')                                # Salvo in un dataframe il file .csv
    X = df.iloc[:, [1, 3, 4]].values                                    # Valori del dataframe che mi serviranno
    times = [element for element in X[:, 0]]
    db = DBscan(NOISE=0, UNASSIGNED=0, core=-1, edge=-2)                # Istanza del dbscan
    time2 = []
    smin = 0
    numC = []

    # Loop per la dimensione della lista
    # Trovo i valori x e y per ogni intervallo e eseguo il dbscan su questi valori
    # Mi restituisce una lista con il numero di aoi trovati per ogni intervallo
    for i in range(1, len(listTime)):
        for x in times:
            if x <= listTime[i]:
                time2.append(x)
                numCluX = [element for element in X[smin:len(time2), 1]]
                numCluY = [element for element in X[smin:len(time2), 2]]
        result = np.array([numCluX, numCluY])
        result2 = result.transpose()
        cluster, pl = db.fit(result2)
        numC.append(cluster)
        diff = len(time2) - smin
        smin = smin + diff
        numCluX.clear()
        numCluY.clear()
        time2.clear()

    # Dettagli del grafico
    fig, ax = plt.subplots(num='Conteggio Aoi',figsize=(12, 8))
    plt.bar(inter, numC, width=0.3)
    # Annotazione del numero di aoi per ogni intervallo
    for i in range(len(inter)):
        plt.annotate(numC[i], (-0.05 + i, numC[i]))
    plt.ylim([0, 5])
    plt.ylabel('Numero di Aree di Interesse',fontweight='bold', fontsize=15)
    plt.xlabel('Intervalli (s)',fontweight='bold', fontsize=15)
    plt.title('Grafico Aree di interesse')
    fig.savefig('grafic/graficAoi.png')

    event, values = sg.Window('Dettagli grafico', [[sg.Image(filename='grafic/graficAoi.png')]]).read(close=True)
    plt.show()

# Funzione che mi restituisce un grafico con gli aoi dominanti per ogni intervallo
# Parametri: inter = numero di intervalli; listTime = lista avente i valori del tempo per ogni intervallo
def barGraphAoiDominant(listTime, timePoint):

    listTime2 = [val for val in listTime]
    listTime2.pop(0)
    count = 0
    count2 = 0
    numClust = []
    help1 = []
    for x in range(len(listTime) - 1):
        for i in range(len(timePoint)):
            for j in range(len(timePoint[i])):

                if timePoint[i][j] >= listTime[x] and timePoint[i][j] <= listTime[x + 1]:

                    count += 1
            if count != 0:
                numClust.append(count)
                count2 += 1
            count = 0

        help1.append(count2)
        count2 = 0

    help2 = []
    count3 = 0
    for x in range(len(help1)):
        help2.append([])
        for y in range(help1[x]):
            help2[x].append(numClust[count3])
            count3 += 1

    fig, ax = plt.subplots(num='Aoi Dominante', figsize=(12, 8))
    br1 = 0.1
    br2 = -0.92
    mapcolor = ['red', 'blue', 'green', 'yellow', 'black', 'orange', 'indigo', 'magenta', 'pink', 'grey', 'lime',
                'violet', 'cyan', 'fuchsia']
    count = 0
    maxCount = 0
    for i in range(len(help1)):
        if help1[i] >= 1:
            for j in range(help1[i]):
                br = [br2]
                plt.bar(br, help2[i][j], color=mapcolor[j], width=br1)
                plt.annotate(help2[i][j], (-0.05 + br2, help2[i][j]))
                count += 1
                if j < (help1[i]) - 1:
                    br2 += 0.1
                else:
                    br2 = 0
                    br2 = (1 * i) + 0.2

            if maxCount < count:
                maxCount = count
        else:
            br2 = (1 * (i + 1)) + 0.2
        count = 0
        # Altri dettagli del grafico
        plt.xlabel('Intervalli (s)', fontweight='bold', fontsize=15)
        plt.ylabel('Numero di fissazioni', fontweight='bold', fontsize=15)
        plt.xlim([-1, len(listTime)])
        plt.xticks([r + br1 for r in range(len(listTime2))], [listTime2[x] for x in range(len(listTime2))])  # CORRETTO

    for i in range(maxCount):
        plt.plot(i, label='cluster' + str(i + 1), c=mapcolor[i])
    plt.grid(axis='y')
    plt.legend()
    plt.title('Grafico Aoi Dominante\n(Dbscan)')
    fig.savefig('grafic/graficAOIDominante.png')

    event, values = sg.Window('Dettagli grafico', [[sg.Image(filename='grafic/graficAOIDominante.png')]]).read(close=True)
    plt.show()

