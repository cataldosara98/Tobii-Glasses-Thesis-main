import cv2
import pandas as pd
import tkinter as tk
import keyboard
import PySimpleGUI as sg
import ctypes
from readDataGaze import *
ctypes.windll.shcore.SetProcessDpiAwareness(2)
def chooseScanpath(pathGaze, pathVideo):
    while True:

        #choose = input("Digita l'opzione scelta: ")
        choose = sg.popup_get_text('''Quale Scanpath vuoi creare e visualizzare?
        1. Scanpath Real-Time
        2. Scanpath finale
        ''', )
        if choose == str(1):
            path = pathVideo
            generateScanpath(path, pathGaze)
        elif choose == str(2):
            sg.popup_no_buttons("CREAZIONE SCANPATH IN CORSO...", auto_close=True)
            generateFrame(pathVideo)
        elif choose == choose != str(1) and choose != str(2) :
          sg.popup('''Avviso: 
         - Il numero scelto non è non valido ;
         - Uscita dalla funzione  ''')
        break
def generateScanpath(path, pathGaze):
    readData(pathGaze)
    # dati del grafico fixation
    csv_file = 'out/fixation.csv'
    # Salvo in un dataFrame il file letto
    dataFrame = pd.read_csv(csv_file)
    # Salvo in un array i valori dei campi che dovrò utilizzare
    data = dataFrame.iloc[:, [0, 1, 2, 3, 4]].values
    numFix = [element for element in data[:, 0]]
    start = [element for element in data[:, 1]]
    dur = [element for element in data[:, 2]]
    posX = [element for element in data[:, 3]]
    posY = [element for element in data[:, 4]]
    posXPix = []
    posYPix = []
    times = []
    Xtemp = []
    Ytemp = []
    d_temp=[]
    lista_flag=[]
    flag = False#Utile per interrompere il video

    #lista di 1000 numeri utilizzata per numerare le fissazioni
    lista = []
    for i in range(10000):
        lista.append(i)

    #Formatto i Tempi
    for s, d in zip(start, dur):
        times.append(float("{:.1f}".format(s + d)))  # Secondi

    #Acquisisco la grandezza del display
    root = tk.Tk()#Libreria tkinter 
    displayWidth = root.winfo_screenwidth()
    displayHeight = root.winfo_screenheight()



    #root.mainloop()

    #Formatto x,y per avere le coordinate in pixel
    for x, y in zip(posX, posY):
        posXPix.append(round(x * displayWidth))
        posYPix.append(round(y * displayHeight))


    vid_filename = path #Il video utilizzato, specificato nel main

    cap = cv2.VideoCapture(vid_filename)
    count = 1
    fps = int(cap.get(cv2.CAP_PROP_FPS)) #Salvo il numero di fps del video

    i = 0
    k = 0
    while cap.isOpened():
        ret, frame = cap.read()

        if ret is False:
            break  # Break loop nel caso in cui ret è falso (lo diventa nell'ultimo frame)

        '''
        for i,(x, y, t, d) in enumerate(zip(posXPix, posYPix, start, dur)):
            if abs(count - (t+d) * fps) <= 1: #Per sincronizzare il tempo in cui si è verificata la fissazione con il frame
                # Disegno i cerchi
                cv2.circle(frame, (int(x), int(y)), 10, (255, 0, 0), -1)

                #Posiziono l'elemento scansionato in una lista temporanea utile a ridisegnare i cerchi precedenti
                Xtemp.append(x)
                Ytemp.append(y)
                for a, b, i in zip(Xtemp, Ytemp, range(len(Xtemp) - 1)):
                    #Ridisegno i cerchi precedenti
                    cv2.circle(frame, (int(a), int(b)), 10, (255, 0, 0), -1)

                    # Creazione saccadi
                    # Creazione frecce che uniscono saccadi di inizio e fine
                    cv2.line(frame, (Xtemp[i], Ytemp[i]), (Xtemp[i + 1], Ytemp[i + 1]), (238, 238, 238), 2)
                    # cv2.putText(frame, str(i), (posXPix[i], posYPix[i]), cv2.FONT_HERSHEY_DUPLEX, 0.8, (0, 255, 0), 2, cv2.LINE_AA)
        '''

        for x, y, t, d, l in zip(posXPix, posYPix, start, dur, lista):
            if abs(count - (t + d) * fps) <= 1:# Per sincronizzare il tempo in cui si è verificata la fissazione con il frame
                d=d*6                  #moltiplico dur per 6 in modo da aumentare la dimensione del cerchio
                if d < 1:              #se la durata è minore di 1
                    d=1                #arrotondamela ad 1
                # Disegno i cerchi
                cv2.circle(frame, (int(x), int(y)), int(d), (255,3,224), -1) #disegno il cerchio ed il relativo testo
                cv2.putText(img=frame,
                            text=str(l),
                            org=(int(x), int(y)),
                            fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                            fontScale=1,
                            color=(3, 7, 255) ,
                            thickness=1,
                            lineType=cv2.LINE_AA)


                # Posiziono gli elementi scansionati in precedenza (nel primo for) in una lista temporanea utile a ridisegnare i cerchi precedenti
                Xtemp.append(x)
                Ytemp.append(y)
                d_temp.append(d)
                lista_flag.append(l)

                for a, b, i, d_t, l_f in zip(Xtemp, Ytemp, range(len(Xtemp)-1),d_temp, lista_flag):
                    # Ridisegno i cerchi precedenti
                    cv2.circle(frame, (int(a), int(b)), int(d_t), (255,3,224), -1)
                    cv2.putText(img=frame,
                                 text=str(l_f),
                                 org=(int(a), int(b)),
                                 fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                                 fontScale=1,
                                 color=	(3, 7, 255),
                                 thickness=1,
                                 lineType=cv2.LINE_AA)

                    # Creazione saccadi
                    # Creazione frecce che uniscono saccadi di inizio e fine
                    cv2.line(frame, (Xtemp[i], Ytemp[i]), (Xtemp[i + 1], Ytemp[i + 1]), (238, 238, 238), 2)
                    # cv2.putText(frame, str(i), (posXPix[i], posYPix[i]), cv2.FONT_HERSHEY_DUPLEX, 0.8, (0, 255, 0), 2, cv2.LINE_AA)

                cv2.namedWindow('Scanpath') #nomino la finestra Scanpath, utile per la chiusura
                cv2.imshow('Scanpath', frame)
                cv2.waitKey(1000)

                #Comando per bloccare l'esecuzione dei cicli e la creazione dello scanpath sul video
                if keyboard.is_pressed('q'):
                    print('Video interrotto.')
                    flag = True#Setto il flag a true
                    break
            if flag == True:#Ci entro solo se è stato premuto il tasto q, faccio terminare i cicli
               break
        count += 1

    cap.release()
    if flag == True:  # Ci entro solo se è stato premuto il tasto q, chiudo il video
        cv2.destroyWindow('Scanpath')

def generateFrame(path):
    # dati del grafico fixation
    csv_file = 'out/fixation.csv'
    # Salvo in un dataFrame il file letto
    dataFrame = pd.read_csv(csv_file)
    # Salvo in un array i valori dei campi che dovrò utilizzare
    data = dataFrame.iloc[:, [0, 1, 2, 3, 4]].values
    numFix = [element for element in data[:, 0]]
    start = [element for element in data[:, 1]]
    dur = [element for element in data[:, 2]]
    posX = [element for element in data[:, 3]]
    posY = [element for element in data[:, 4]]
    posXPix = []
    posYPix = []
    times = []
    Xtemp = []
    Ytemp = []
    d_temp = []
    lista_flag = []
    flag = False  # Utile per interrompere il video

    # lista di 1000 numeri utilizzata per numerare le fissazioni
    lista = []
    for i in range(10000):
        lista.append(i)

    # Formatto i Tempi
    for s, d in zip(start, dur):
        times.append(float("{:.1f}".format(s + d)))  # Secondi

    # Acquisisco la grandezza del display
    root = tk.Tk()  # Libreria tkinter
    displayWidth = root.winfo_screenwidth()
    displayHeight = root.winfo_screenheight()

    #root.mainloop()

    # Formatto x,y per avere le coordinate in pixel
    for x, y in zip(posX, posY):
        posXPix.append(round(x * displayWidth))
        posYPix.append(round(y * displayHeight))

    vid_filename = path  # Il video utilizzato, specificato nel main

    cap = cv2.VideoCapture(vid_filename)
    count = 1
    fps = int(cap.get(cv2.CAP_PROP_FPS))  # Salvo il numero di fps del video
    totale = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    while cap.isOpened():
        ret, frame = cap.read()



        if ret is False:
            break  # Break loop nel caso in cui ret è falso (lo diventa nell'ultimo frame)

        for x, y, t, d, l in zip(posXPix, posYPix, start, dur, lista):
            if abs(count - (t + d) * fps) <= 1:  # Per sincronizzare il tempo in cui si è verificata la fissazione con il frame
                d = d * 5
                if d < 1:
                    d = 1
                # Disegno i cerchi
                cv2.circle(frame, (int(x), int(y)), int(d), (138, 11, 92), -1)
                cv2.putText(img=frame,
                            text=str(l),
                            org=(int(x), int(y)),
                            fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                            fontScale=1,
                            color=(0, 0, 255),
                            thickness=1,
                            lineType=cv2.LINE_AA)

                # Posiziono l'elemento scansionato in una lista temporanea utile a ridisegnare i cerchi precedenti

                Xtemp.append(x)
                Ytemp.append(y)
                d_temp.append(d)
                lista_flag.append(l)

                for a, b, i, d_t, l_f in zip(Xtemp, Ytemp, range(len(Xtemp) - 1), d_temp, lista_flag):
                    # Ridisegno i cerchi precedenti
                    cv2.circle(frame, (int(a), int(b)), int(d_t), (138, 11, 92), -1)
                    cv2.putText(img=frame,
                                text=str(l_f),
                                org=(int(a), int(b)),
                                fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                                fontScale=1,
                                color=(0, 0, 255),
                                thickness=1,
                                lineType=cv2.LINE_AA)

                    # Creazione saccadi
                    # Creazione frecce che uniscono saccadi di inizio e fine
                    cv2.line(frame, (Xtemp[i], Ytemp[i]), (Xtemp[i + 1], Ytemp[i + 1]), (238, 238, 238), 2)
                    # cv2.putText(frame, str(i), (posXPix[i], posYPix[i]), cv2.FONT_HERSHEY_DUPLEX, 0.8, (0, 255, 0), 2, cv2.LINE_AA)

                cv2.imshow('Scanpath', frame )
                #cv2.imwrite(frame )

                # Comando per bloccare l'esecuzione dei cicli e la creazione dello scanpath sul video
                if keyboard.is_pressed('q'):
                    print('Video interrotto.')
                    flag = True  # Setto il flag a true
                    break
            if flag == True:  # Ci entro solo se è stato premuto il tasto q, faccio terminare i cicli
                break
        count += 1

    cap.release()
    if flag == True:  # Ci entro solo se è stato premuto il tasto q, chiudo il video
        cv2.destroyAllWindows()

        