# Funzione per settare i colori, ha come paramentro un int

import PySimpleGUI as sg


def setColor(color):

    if color == 1:
        c = 'red'
    elif color == 2:
        c = 'blue'
    elif color == 3:
        c = 'yellow'
    elif color == 4:
        c = 'green'
    else:
        c = 'black'
    print("Hai scelto il colore: ",c)

    return c


# Funzione che restituisce i colori di ogni intervallo
def interChoose():
    # L'utente deve inserire il numero di intervalli che vuole creare





    while True:
     n = (sg.popup_get_text("Quanti intervalli vuoi creare ?(max 5): "))
     if n!=str(1) and n!=str(2) and n!=str(3) and n!=str(4) and n!=str(5):
         sg.popup_annoying("Perfavore inserire un valore valido")

     else:
        while True:
           col = []  # Lista di colori

           for i in range(int(n)):
             color =int(sg.popup_get_text('''Seleziona il colore per il %s° intervallo: 
        I colori presenti nell'elenco sono:
                1. Red
                2. Blue
                3. Yellow
                4. Green
                5. Black
        '''  % (i+1)))  # Loop del numero di intervalli per settare il colore ad ogni intervallo

             if color != int(1) and color != int(2) and color != int(3) and color != int(4) and color != int(5):

                   sg.popup_annoying("Perfavore inserire un valore valido")

             else:
                   col.append(setColor(color))
           return col






# Funzione che restituisce i limiti di ogni intervallo, passo per paramentro il numero di intervalli e il tempo massimo del video
def durInter(num,time, scene):

    listInter = []                                  # Lista dei limiti degli intervalli
    listInter.append(time)                          # Aggiungo il primo limite alla lista
    for i in range(num):
        sg.popup_get_text("Scegli tra %s e  %s:" %(listInter[i], scene))

        # Controllo se è l'ultima iterazione
        # Se è l'ultima allora restituisco nella variable help1 il tempo massimo
        # Altrimenti l'utente digita il limite dell' intervallo per ogni i-esimo intervallo
        if i == num-1:
            help1 = scene
        else:
            while(True):
                help1 = float(sg.popup_get_text("Digita: "))
                if help1 >= listInter[i] and help1 <= scene:
                    break
                else:
                    sg.popup_annoying("Numero inserito non valido")
        listInter.append(help1)                       # Aggiungo il numero nella lista

    return listInter