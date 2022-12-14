import csv as cs
import gzip
import json
import pandas as pd
import matplotlib
import PySimpleGUI as sg
import os
from fixatDetection import *
from fixColor import *
from pupil import *
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

#Funzione per stampare il file pupil.csv sulla console
def readFilePupil(): 
    csv_file = 'out/pupil.csv'
    data = pd.read_csv(csv_file)
    print(data)
    csv_file2 = 'out/pupilsStatistics.csv'
    data2 = pd.read_csv(csv_file2)
    print(data2)

#***********************************************************************************#
#Funzione per stampare il file fixation.csv sulla console
def readFileFixation():
    csv_file = 'out/fixation.csv'
    data = pd.read_csv(csv_file)
    print(data)
#***********************************************************************************#

# Funzione utilizzata per leggere i dati del file gazedata.gz e scrivere un nuovo file .csv
def readData(pathGaze):
    # Confronto il nome del video

    with gzip.open(pathGaze) as f1:

        # Liste vuote
        positionX = []
        positionY = []
        positionZ = []
        time = []
        eyeLFdiameter = []
        eyeRGdiameter = []
        averageLFRG = []
       

        # Loop per leggere ogni riga nel file
        for data in f1:

            # Assegno  le righe al dictionary dicto
            d = json.loads(data)

            # Salvo nelle variabili i campi che servono dal dictionary
            timestamp = d.get('timestamp')
            gaze2d = d.get('data', {}).get('gaze2d')
            gaze3d = d.get('data', {}).get('gaze3d')
            eyeleftdiameter = d.get('data', {}).get('eyeleft', {}).get('pupildiameter')
            eyerightdiameter = d.get('data', {}).get('eyeright', {}).get('pupildiameter')
        
            time.append(timestamp)  # lista timestamp

            # Controllo se icampi sono vuoti
            # Se lo sono assegno alle liste il valore 0
            # Altrimenti assegno i valori delle variabili
            
            if eyeleftdiameter is None:
                eyeLFdiameter.append(0)  # lista eyelfdiameter
            else:
                eyeLFdiameter.append(eyeleftdiameter)  # lista eyelfdiameter

            if eyerightdiameter is None:
                eyeRGdiameter.append(0)  # lista eyergdiameter
            else:
                eyeRGdiameter.append(eyerightdiameter)  # lista eyergdiameter
            
            if gaze3d == None:
                positionX.append(0)
                positionY.append(0)
                positionZ.append(0)
            else:
                positionX.append(gaze2d[0])  # lista coordinata x
                positionY.append(gaze2d[1])  # lista coordinata y
                positionZ.append(gaze3d[2])  # lista coordinata z


        # for per iterare su ciascun diametro di ogni istante
        for diamLF,diamRG in zip(eyeLFdiameter,eyeRGdiameter):
            averageLFRG.append(averageLeftAndRight(diamLF,diamRG))#Calcolo media per ogni istante
        
        print("Numero timestamp    Sinistro     Destro      Avg ",(len(time),len(eyeLFdiameter),len(eyeLFdiameter),len(averageLFRG)))
        minAndMaxDiameter = minmaxLeftAndRight(eyeLFdiameter,eyeRGdiameter)#Chiamata a funzione per il cacolo del minimo e massimo
        avgDilatationSpeedLF = avgDilatationSpeed(eyeLFdiameter[0],eyeLFdiameter[len(eyeLFdiameter)-1],time[0],time[len(time)-1])#Calcolo velocit?? dilatazione media occhio sinistro
        avgDilatationSpeedRG = avgDilatationSpeed(eyeRGdiameter[0],eyeRGdiameter[len(eyeRGdiameter)-1],time[0],time[len(time)-1])#Calcolo velocit?? dilatazione media occhio destro
 
        # fields ?? una lista avente i nomi dei campi del nuovo file csv
        fields = ['Timestamp','EyeLeftDiameter','EyeRightDiameter','AverageLeftAndRight']

        # Creazione e apertura del file di nome pupil.csv
        with open('out/pupil.csv', 'w', newline="") as cvsPupil:

            # w ?? una dictionary con i campi della lista fields
            w = cs.DictWriter(cvsPupil, fieldnames=fields, delimiter=',')
            w.writeheader()

            # Loop per inserire i valori delle liste nei campi del dictionary
            for stime,diamLF,diamRG, average in zip(time,eyeLFdiameter,eyeRGdiameter, averageLFRG):
               raw = {'Timestamp':stime, 'EyeLeftDiameter': diamLF, 'EyeRightDiameter': diamRG, 'AverageLeftAndRight':average}
               w.writerow(raw)

        #Task 1
        diff = diffLeftRight(maxDimInt(time, eyeRGdiameter, eyeLFdiameter, 22, 27)[1], maxDimInt(time, eyeRGdiameter, eyeLFdiameter, 22, 27)[0])
        diff1 = diffLeftRight(maxDimInt(time, eyeRGdiameter, eyeLFdiameter, 27, 32)[1], maxDimInt(time, eyeRGdiameter, eyeLFdiameter, 27, 32)[0])
        diff2 = diffLeftRight(maxDimInt(time, eyeRGdiameter, eyeLFdiameter, 32, 37)[1], maxDimInt(time, eyeRGdiameter, eyeLFdiameter, 32, 37)[0])
        diff3 = diffLeftRight(maxDimInt(time, eyeRGdiameter, eyeLFdiameter, 37, 42)[1], maxDimInt(time, eyeRGdiameter, eyeLFdiameter, 37, 42)[0])

        # fields1 ?? una lista avente i nomi dei campi del nuovo file csv
        fields1 = ['Img', 'MaxEyeLeftDiameter', 'MaxEyeRightDiameter', 'Differential']

        # Creazione e apertura del file di nome task1.csv
        with open('out/task1.csv', 'w', newline="") as csvTask1:

            # w1 ?? una dictionary con i campi della lista fields
            w1 = cs.DictWriter(csvTask1, fieldnames=fields1, delimiter=',')
            w1.writeheader()

            # Inserisco i valori nei campi del dictionary
            w1.writerow({'Img': "T1_01",'MaxEyeLeftDiameter': maxDimInt(time, eyeRGdiameter, eyeLFdiameter, 22, 27)[1], 'MaxEyeRightDiameter': maxDimInt(time, eyeRGdiameter, eyeLFdiameter, 22, 27)[0], 'Differential': diff})
            w1.writerow({'Img': "T1_02",'MaxEyeLeftDiameter': maxDimInt(time, eyeRGdiameter, eyeLFdiameter, 27, 32)[1], 'MaxEyeRightDiameter': maxDimInt(time, eyeRGdiameter, eyeLFdiameter, 27, 32)[0], 'Differential': diff1})
            w1.writerow({'Img': "T1_03",'MaxEyeLeftDiameter': maxDimInt(time, eyeRGdiameter, eyeLFdiameter, 32, 37)[1], 'MaxEyeRightDiameter': maxDimInt(time, eyeRGdiameter, eyeLFdiameter, 32, 37)[0], 'Differential': diff2})
            w1.writerow({'Img': "T1_04",'MaxEyeLeftDiameter': maxDimInt(time, eyeRGdiameter, eyeLFdiameter, 37, 42)[1], 'MaxEyeRightDiameter': maxDimInt(time, eyeRGdiameter, eyeLFdiameter, 37, 42)[0], 'Differential': diff3})

        # Task 2

        diff = diffLeftRight(maxDimInt(time, eyeRGdiameter, eyeLFdiameter, 42, 46)[1], maxDimInt(time, eyeRGdiameter, eyeLFdiameter, 42, 46)[0])
        diff1 = diffLeftRight(maxDimInt(time, eyeRGdiameter, eyeLFdiameter, 46, 50)[1], maxDimInt(time, eyeRGdiameter, eyeLFdiameter, 46, 50)[0])
        diff2 = diffLeftRight(maxDimInt(time, eyeRGdiameter, eyeLFdiameter, 50, 54)[1], maxDimInt(time, eyeRGdiameter, eyeLFdiameter, 50, 54)[0])
        diff3 = diffLeftRight(maxDimInt(time, eyeRGdiameter, eyeLFdiameter, 54, 58)[1], maxDimInt(time, eyeRGdiameter, eyeLFdiameter, 54, 58)[0])

        # Creazione e apertura del file di nome task2.csv
        with open('out/task2.csv', 'w', newline="") as csvTask2:

            # w2 ?? una dictionary con i campi della lista fields
            w2 = cs.DictWriter(csvTask2, fieldnames=fields1, delimiter=',')
            w2.writeheader()

            # Inserisco i valori nei campi del dictionary
            w2.writerow({'Img': "T2_01", 'MaxEyeLeftDiameter': maxDimInt(time, eyeRGdiameter, eyeLFdiameter, 42, 46)[1], 'MaxEyeRightDiameter': maxDimInt(time, eyeRGdiameter, eyeLFdiameter, 42, 46)[0], 'Differential': diff})
            w2.writerow({'Img': "T2_02", 'MaxEyeLeftDiameter': maxDimInt(time, eyeRGdiameter, eyeLFdiameter, 46, 50)[1], 'MaxEyeRightDiameter': maxDimInt(time, eyeRGdiameter, eyeLFdiameter, 46, 50)[0], 'Differential': diff1})
            w2.writerow({'Img': "T2_03", 'MaxEyeLeftDiameter': maxDimInt(time, eyeRGdiameter, eyeLFdiameter, 50, 54)[1], 'MaxEyeRightDiameter': maxDimInt(time, eyeRGdiameter, eyeLFdiameter, 50, 54)[0], 'Differential': diff2})
            w2.writerow({'Img': "T2_04", 'MaxEyeLeftDiameter': maxDimInt(time, eyeRGdiameter, eyeLFdiameter, 54, 58)[1], 'MaxEyeRightDiameter': maxDimInt(time, eyeRGdiameter, eyeLFdiameter, 54, 58)[0],'Differential': diff3})

        #Task 3

        # fields2 ?? una lista avente i nomi dei campi del nuovo file csv
        fields2 = ['Img', 'DiamRipRG', 'DiamRipLF', 'DiamMaxRG', 'DiamMaxLF', 'DiffMinMax', 'DiamAvg']

        # Creazione e apertura del file di nome task3.csv
        with open('out/task3.csv', 'w', newline="") as csvTask3:
            # w3 ?? una dictionary con i campi della lista fields
            w3 = cs.DictWriter(csvTask3, fieldnames=fields2, delimiter=',')
            w3.writeheader()

            # Inserisco i valori nei campi del dictionary
            w3.writerow({'Img': "T3_01", 'DiamRipRG': dimRipLFRG(time, eyeRGdiameter, eyeLFdiameter, 54, 56)[0], 'DiamRipLF': dimRipLFRG(time, eyeRGdiameter, eyeLFdiameter, 54, 56)[1], 'DiamMaxRG': maxDimInt(time, eyeRGdiameter, eyeLFdiameter, 56, 60)[0], 'DiamMaxLF': maxDimInt(time, eyeRGdiameter, eyeLFdiameter, 56, 60)[1], 'DiffMinMax': rispPup(time, eyeRGdiameter, eyeLFdiameter, 56, 60), 'DiamAvg': diamAvgPup(time, eyeRGdiameter, eyeLFdiameter, 56, 60)})
            w3.writerow({'Img': "T3_02", 'DiamRipRG': dimRipLFRG(time, eyeRGdiameter, eyeLFdiameter, 60, 62)[0], 'DiamRipLF': dimRipLFRG(time, eyeRGdiameter, eyeLFdiameter, 60, 62)[1], 'DiamMaxRG': maxDimInt(time, eyeRGdiameter, eyeLFdiameter, 62, 66)[0], 'DiamMaxLF': maxDimInt(time, eyeRGdiameter, eyeLFdiameter, 62, 66)[1], 'DiffMinMax': rispPup(time, eyeRGdiameter, eyeLFdiameter, 62, 66), 'DiamAvg': diamAvgPup(time, eyeRGdiameter, eyeLFdiameter, 62, 66)})
            w3.writerow({'Img': "T3_03", 'DiamRipRG': dimRipLFRG(time, eyeRGdiameter, eyeLFdiameter, 66, 68)[0], 'DiamRipLF': dimRipLFRG(time, eyeRGdiameter, eyeLFdiameter, 66, 68)[1], 'DiamMaxRG': maxDimInt(time, eyeRGdiameter, eyeLFdiameter, 68, 72)[0], 'DiamMaxLF': maxDimInt(time, eyeRGdiameter, eyeLFdiameter, 68, 72)[1], 'DiffMinMax': rispPup(time, eyeRGdiameter, eyeLFdiameter, 68, 72), 'DiamAvg': diamAvgPup(time, eyeRGdiameter, eyeLFdiameter, 68, 72)})
            w3.writerow({'Img': "T3_04", 'DiamRipRG': dimRipLFRG(time, eyeRGdiameter, eyeLFdiameter, 72, 74)[0], 'DiamRipLF': dimRipLFRG(time, eyeRGdiameter, eyeLFdiameter, 72, 74)[1], 'DiamMaxRG': maxDimInt(time, eyeRGdiameter, eyeLFdiameter, 76, 80)[0], 'DiamMaxLF': maxDimInt(time, eyeRGdiameter, eyeLFdiameter, 76, 80)[1], 'DiffMinMax': rispPup(time, eyeRGdiameter, eyeLFdiameter, 76, 80), 'DiamAvg': diamAvgPup(time, eyeRGdiameter, eyeLFdiameter, 76, 80)})

        #Task4
            csv_file1 = 'out/fixation.csv'
            data = pd.read_csv(csv_file1)
            d = data.iloc[:, [0, 1, 2, 3, 4]].values
            numFix = [element for element in d[:, 0]]
            start = [element for element in d[:, 1]]
            dur = [element for element in d[:, 2]]
            # fields3 ?? una lista avente i nomi dei campi del nuovo file csv
            fields3 = ['FirstImg', 'SacFix', 'PupRea']

            # Creazione e apertura del file di nome task3.csv
            with open('out/task4.csv', 'w', newline="") as csvTask4:
                # w4 ?? una dictionary con i campi della lista fields
                w4 = cs.DictWriter(csvTask4, fieldnames=fields3, delimiter=',')
                w4.writeheader()

                # Inserisco i valori nei campi del dictionary
                w4.writerow({'FirstImg': firstImg(time, positionX, 300), 'SacFix': sacFix(start, numFix, dur, 300, 304)})
                w4.writerow({'FirstImg': firstImg(time, positionX, 84), 'SacFix': sacFix(start, numFix, dur, 304, 308)})
                w4.writerow({'FirstImg': firstImg(time, positionX, 90), 'SacFix': sacFix(start, numFix, dur, 308, 312)})
                w4.writerow({'FirstImg': firstImg(time, positionX, 100), 'SacFix': sacFix(start, numFix, dur, 312, 316)})

        # Apertura del file di nome pupil.csv in modalit?? append
        with open('out/pupilsStatistics.csv', 'w', newline="") as csvPupilStat:

            # fieldnames ?? una lista avente i nomi dei campi per l'append
            fieldnames = ['TotalAverageLeft','TotalAverageRight','TotalAverageLFandRG','MinDiameterLeft','MinDiameterRight','MaxDiameterLeft','MaxDiameterRight','AvgDilatationSpeedLeft','AvgDilatationSpeedRight']

            # writer ?? una dictionary con i campi della lista fieldnames
            writer = cs.DictWriter(csvPupilStat, fieldnames=fieldnames)
            writer.writeheader()
            
            # Inserisco i valori nei campi del dictionary
            writer.writerow({'TotalAverageLeft': averangeTotal(eyeLFdiameter),'TotalAverageRight': averangeTotal(eyeRGdiameter), 
            'TotalAverageLFandRG':averangeLFRGTotal(averangeTotal(eyeLFdiameter),averangeTotal(eyeRGdiameter)),'MinDiameterLeft':minAndMaxDiameter[0],
            'MinDiameterRight':minAndMaxDiameter[1],'MaxDiameterLeft':minAndMaxDiameter[2],'MaxDiameterRight':minAndMaxDiameter[3],
            'AvgDilatationSpeedLeft':avgDilatationSpeedLF,'AvgDilatationSpeedRight':avgDilatationSpeedRG})

        readFilePupil()
        csvPupilStat.close()  # Chiusura del file
        csvTask1.close()
        csvTask2.close()
        csvTask3.close()
        csvTask4.close() # Chiusura del file

        #*********************************************************************************************************#
        #Richiamo la fnuzione fixation per computare le fissazioni
        Efix1 = fixation(positionX, positionY, positionZ, time)
        res1 = [i[0] for i in Efix1]    #restituisce il numero d fissazioni
        res2 = [i[1] for i in Efix1]    #restituisce il tempo iniziale
        res3 = [i[2] for i in Efix1]    #restituisce la durata
        res4 = [i[3] for i in Efix1]    #restituisce la posizione x
        res5 = [i[4] for i in Efix1]    #restituisce la posizione y
        res6 = [i[5] for i in Efix1]    #restituise la posizione z

        #fields ?? una lista avente i nomi dei campi del nuovo file csv
        fields = ['numeroFissazioni', 'startTime', 'duration', 'position_x', 'position_y', 'position_z']

        #creazione e d apertura del file fixation.csv
        with open('out/fixation.csv', 'w', newline="") as csvFix:

            #w ?? una dictionary con i campi della lista fields
            w = cs.DictWriter(csvFix, fieldnames=fields)
            w.writeheader()

            #loop per inserirre i valori delle liste nei campi del dictionary
            for n, s, du, x , y, z in zip(res1, res2, res3, res4, res5, res6):
                raw = {'numeroFissazioni': n, 'startTime': s, 'duration': du, 'position_x': x, 'position_y': y, 'position_z': z}
                w.writerow(raw)

        readFileFixation()
        csvFix.close
        #**********************************************************************************************************#


# Funzione per creare e visualizzare il grafico delle fissazioni
def graficFix(nImg, scene):

    print("All'utente verranno mostrate %d immagini" % nImg)
    # dati del grafico fixation
    csv_file = 'out/fixation.csv'
    # Salvo in un dataFrame il file letto
    dataFrame = pd.read_csv(csv_file)
    # Salvo in un array i valori dei campi che dovr?? utilizzare
    data = dataFrame.iloc[:, [1, 2, 3,]].values #4, 5
    s = 1
    time = [element for element in data[:, 0]]
    z1 = [element for element in data[: ,2]] #4
    time2 = []
    smin = 0
    w=0

    z1.sort()  # Ordino le coordinate z
    # Loop per trovare il minimo e massimo delle coordinate z
    for i in z1:
        maxZ = i
        minZ = z1[0]
    choose = sg.popup_get_text('''Selezionare l'opzione da eseguire: 
                                1. Settare intervalli uguali
                                2. Settare intervalli misti
                                3. Unico intervallo con gradazione dei colori  '''
                            )

    while(True):
        if choose != str(1) and choose != str(2) and choose != str(3):
            sg.popup('''Avviso: 
                                - Numero inserito non valido
                                - Parola inserita non valida
                                - Uscita dalla funzione  ''')

            break
        else:
            break


    if choose == str(1) or choose == str(2):
        n = interChoose()
    print("All'utente verranno mostrate %d immagini" % nImg)
    # Loop per il numero delle immagini
    # Per ogni immagine prendo i valori x, y, z, dur e time dal tempo di inizio al tempo di fine di quell'immagine
    for z in range(0,(nImg)):
        print("Immagine n. %s " % str(z+1))
        img = mpimg.imread('image/img'+str(z)+'.png')
        # Utilizzati per moltiplicare gli elementi x e y per la dimensione dell immagine
        width = img.shape[1]
        height = img.shape[0]

        for t in time:
            if t <= scene[s]:
                time2.append(t)

        x = [element * width for element in data[smin:len(time2), 0]]       # x contiene gli elementi della colonna 2 di data dal tempo minimo al tempo massimo
        y = [element * height for element in data[smin:len(time2),1]]       # y contiene gli elementi della colonna 3 di data dal tempo minimo al tempo massimo
        z = [element for element in data[smin:len(time2),2]]                # z contiene gli elementi della colonna 4 di data dal tempo minimo al tempo massimo
        dur = [element for element in data[smin:len(time2),0]]              # dur contiene gli elementi della colonna 1 di data dal tempo minimo al tempo massimo
        time3 = [element for element in data[smin:len(time2),0]]            # dur contiene gli elementi della colonna 0 di data dal tempo minimo al tempo massimo

        # Utilizzato per restituire il tempo massimo del video
        
        #Confronto la scelta
        if choose == str(1) or choose == str(2):
            if choose == str(1):
                #n = interChoose()    # Restituisco il numero di intervalli selezionati
                col = []              # Creo una lista e aggiungo il valore 0

                col.append(scene[s-1])
                div = (scene[s]-scene[s-1])/len(n)  # Divido il tempo massimo per n intervalli per trovare la grandezza fissa
                div1 = div + scene[s-1]
                
                # Loop per il numero di intervalli
                for i in range(len(n)):
                    col.append(div1)                        # Aggiungo la grandezza fissa dell'intervallo nella lista
                    div1 = scene[s-1] + ((div) * (i+2))     # Sommo la grandezza fissa per se stessa
                bounds = col                                # Assegno la lista col ad una nuova lista

            elif choose == str(2):
                #n = interChoose()                                       # Restituisce il numero di intervalli selezionati
                bounds = durInter(len(n), scene[s-1], scene[s])         # Restituisce un array avente i limiti degli intervalli

            cmap = matplotlib.colors.ListedColormap(n)                  # Restituisce la lista dei colori

            norm = matplotlib.colors.BoundaryNorm(bounds, len(n))       # Resistuisce i limiti degli intervalli
            fig, ax = plt.subplots(num='Immagine %d' %s,figsize=(11, 6))
            ax.autoscale(enable=True)
            ax.imshow(img, aspect='auto')

            # Visualizzo i cerchi per ogni valore x e y, con cambio di colore in base al tempo,
            # alla lista dei colori scelti dall'utente, i limiti degli intervalli e la durata di ogni fissazione
            scatter = plt.scatter(x, y, c=time3, cmap=cmap, norm=norm, linewidths=dur)

            # Modifica della barra di colori
            cbar = plt.colorbar(scatter, spacing="proportional")
            cbar.set_label('Durata della scena (s)', rotation=270, labelpad=10)

            # Dettagli del grafico
            ax.set_aspect('equal')
            plt.xlim([0, width])
            plt.ylim([height, 0])
            plt.xlabel('Posizione X')
            plt.ylabel('Posizione Y')

            # Loop per la legenda del grafico che segna la dimensione e durata delle fissazioni
            for dur in [1.5, 3, 5]:
                plt.scatter([], [], c='k', alpha=0.3, s=dur * 50, label=str(dur) + 's')

            plt.legend(scatterpoints=1, labelspacing=1, title='Durata delle fissazioni')
            plt.axis('off')
            plt.title('Visualizzazione delle fissazioni')

            fig.set_size_inches(11, 6)
            w += 1
            fig.savefig('grafic/fixation' + str(w) + '.jpg')
            plt.show()
            s += 1
            diff = len(time2) - smin
            smin = smin + diff              #smin sar?? il nuovo tempo iniziale utile per restituirmi i dati che mi serviranno

            # Svuoto le liste
            time3.clear()
            x.clear()
            y.clear()
            time2.clear()


        elif choose == str(3):

            #z.sort()
            # Dettagli del grafico
            fig, ax = plt.subplots(num='Immagine %s' %str(w+1),figsize=(11, 6))
            ax.autoscale(enable=True)
            # img = mpimg.imread('image/img' + str(charV) + '0' + str(q) + '.png')
            ax.imshow(img, aspect='auto')

            plt.scatter(x, y, c=z,vmin = minZ, vmax = maxZ, linewidths=dur)
            ax.set_aspect('equal')
            plt.xlim([0, width])
            plt.ylim([height, 0])
            plt.xlabel('Posizione X')
            plt.ylabel('Posizione Y')
            for dur in [1.5, 3, 5]:
                plt.scatter([], [], c='k', alpha=0.3, s=dur * 50, label=str(dur) + 's')

            plt.legend(scatterpoints=1, labelspacing=1, title='Durata delle fissazioni')
            plt.colorbar(label='Valore Z in millimetri\n ( Distanza tra la camera e il punto fissato )')  # Visualizzazione della barra di colori
            plt.clim(minZ, maxZ)  # Setta il minimo e massimo valore della barra di colori
            plt.axis('off')
            plt.title('Visualizzazione delle fissazioni\n  ( Gradazione del colore )')
            w += 1
            fig.savefig('grafic/fixation' + str(w) + '.jpg')
            plt.show()
            s += 1

            diff = len(time2) - smin
            smin = smin + diff
            time3.clear()
            x.clear()
            y.clear()
            time2.clear()


