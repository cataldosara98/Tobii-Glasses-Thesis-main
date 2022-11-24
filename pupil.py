#Informazioni:
#Dimensioni medie pupille occhio destro e sinistro combinati
#Dimensioni medie pupilla occhio destro totale
#Dimensioni medie pupilla occhio sinistro totale
#Dimenesione medie occhio destro e sinistro totale
#Dimensione massima occhio sinistro e occhio destro
#Dimensione minima occhio sinistro e occhio destro
#Cacolo Velocità media dilatazione

#Dimensioni medie pupille occhio destro e sinistro combinati
def averageLeftAndRight(diameterLF,diameterRG):
    average = (diameterLF + diameterRG)/2
    return average

#Dimensioni medie pupilla occhio sinistro totale
#Dimensioni medie pupilla occhio destro totale
def averangeTotal(diameterEye):
    return sum(diameterEye)/len(diameterEye)
   
#Dimenesione medie occhio destro e sinistro totale
def averangeLFRGTotal(averageTotalLF,averageTotalLFRG):
    average = (averageTotalLF+averageTotalLFRG)/2
    return average


#Dimensione massima occhio sinistro e occhio destro
#Dimensione minima occhio sinistro e occhio destro
def minmaxLeftAndRight(diameterLF,diameterRG):
    minDiameterLF = min([value for value in diameterLF if value!=0])
    minDiameterRG = min([value for value in diameterRG if value!=0])
    maxDiameterLF = max(diameterLF)
    maxDiameterRG = max(diameterRG)

    return minDiameterLF,minDiameterRG,maxDiameterLF,maxDiameterRG


#Cacolo Velocità media dilatazione
def avgDilatationSpeed(initialDil,finalDil,initialT,finalT):
    return (finalDil-initialDil)/(finalT-initialT)

#Task 1
#Calcolo differenziale a il diametro minimo nella prima parte dell’esposizione e il diametro massimo nella seconda metà
def diffLeftRight(diameterLF, diameterRG) :
    diff = diameterLF - diameterRG
    diff1 = diameterRG - diameterLF
    return max(diff, diff1)

# Massimo diametro pupilla destra e sinistra in intervallo di tempo
def maxDimInt(time, eyeRGdiameter, eyeLFdiameter, t1, t2) :
    mdimRG = 0
    mdimLF = 0
    for x, y, z in zip(time, eyeRGdiameter, eyeLFdiameter):
        if x > t1 and x < t2:
            if (mdimRG < y):
                mdimRG = y
            if (mdimLF < z):
                mdimLF = z
    return mdimRG, mdimLF

#Diametro pupillare destra e sinistra a riposo
def dimRipLFRG(time, eyeRGdiameter, eyeLFdiameter, t1, t2) :
    dRG = 0
    dLF = 0
    for x, y, z in zip(time, eyeRGdiameter, eyeLFdiameter):
        if x > t1 and x < t2:
            dRG = y
            dLF = z
    return dRG, dLF

# Diametro pupillare massimo rilevato durante l'esposizione al singolo stimolo
def dmaxTot(time, eyeRGdiameter, eyeLFdiameter, t1, t2) :
    dmax = 0
    for x, y, z in zip(time, eyeRGdiameter, eyeLFdiameter):
        if x > t1 and x < t2:
            dmax = max(minmaxLeftAndRight(eyeLFdiameter, eyeRGdiameter)[2], minmaxLeftAndRight(eyeLFdiameter, eyeRGdiameter)[3])
    return dmax

# Risposta pupillare: differenza tra dmin e dmax e tempi di risposta
def rispPup(time, eyeRGdiameter, eyeLFdiameter, t1, t2) :
    dif = 0
    for x, y, z in zip(time, eyeRGdiameter, eyeLFdiameter):
        if x > t1 and x < t2:
            dif = diffLeftRight(minmaxLeftAndRight(eyeLFdiameter, eyeRGdiameter)[2], minmaxLeftAndRight(eyeLFdiameter, eyeRGdiameter)[3])
    return dif

# Diametro pipillare medio
def diamAvgPup(time, eyeRGdiameter, eyeLFdiameter, t1, t2) :
    avg = 0
    av = 0
    a = []
    for x, y, z in zip(time, eyeRGdiameter, eyeLFdiameter):
        if x > t1 and x < t2:
            if eyeRGdiameter and eyeLFdiameter is None :
                avg = 0
            else :
                av = (y + z)/2
                a.append(av)
                avg = sum(a)/len(a)
    return avg


