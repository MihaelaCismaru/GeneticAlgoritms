import numpy as np
from numpy import random
import matplotlib.pyplot as plt

def initializare_populatie (marime_populatie) :
    populatie = []
    for i in range (0,marime_populatie) :
        populatie.append( random.randint(0,2,size=gene) )
    return populatie

def calcul_adecvare (populatie) :    
    adecvare = []
    for crom in populatie:
        valoare_totala = 0
        greutate_totala = 0
        for index,each in enumerate(crom):
            if each == 1:
                valoare_totala = valoare_totala + valori[index]
                greutate_totala = greutate_totala + greutati[index]
        if greutate_totala > greutate_maxima :
            valoare_totala = valoare_totala*(-1)
        adecvare.append(valoare_totala)
    
    minim = np.min(adecvare)
    #daca avem valori negative, le aducem pe toate peste 0 adaugand cea mai mica valoare
    if (minim < 0):
        for index,each in enumerate(adecvare):
            adecvare[index] = adecvare[index] + minim*(-1)
    return adecvare

def calcul_adecvare_final (populatie) :    
    adecvare = []
    for crom in populatie:
        valoare_totala = 0
        greutate_totala = 0
        for index,each in enumerate(crom):
            if each == 1:
                valoare_totala = valoare_totala + valori[index]
                greutate_totala = greutate_totala + greutati[index]
        if greutate_totala > greutate_maxima :
            valoare_totala = valoare_totala*(-1)
        adecvare.append(valoare_totala)
    return adecvare

#fitness proportionat
def selectie (populatie, de_ales, marime_populatie) :
    adecvare = calcul_adecvare (populatie)
    index = []
    for i in range (0,marime_populatie) :
        index.append (i)
    sum = np.sum(adecvare)

    probabilitati = []

    for each in adecvare:
        probabilitati.append(each/sum)

    selectati = random.choice(index,p = probabilitati,size=de_ales)
    alesi = []
    for ind in selectati:
        for index,each in enumerate (populatie) :
            if (index == ind) :
                alesi.append(each)
                break
        
    return alesi

#incrucisare binara uniforma
def incrucisare (parinte1, parinte2, gene) :
    masca = random.randint(0,2,size=(gene))

    copil1 = np.array([],dtype=int)
    copil2 = np.array([],dtype=int)

    for i in range (0,gene) :
        if (masca[i] == 0) :
            copil1 = np.append (copil1, parinte2[i])
            copil2 = np.append (copil2, parinte1[i])
        else :
            copil1 = np.append(copil1, parinte1[i])
            copil2 = np.append(copil2,parinte2[i])

    copii = []
    copii.append (copil1)
    copii.append (copil2)
    return copii

#mutatie binara tare
def aplica_mutatii (copii, gene) :
    pm = 0.2
    for cromozom in copii:
        sansa_mutatie = random.rand()
        #nu facem mutatie tuturor copiilor, doar cu probabilitate de 1/5
        if (sansa_mutatie < pm) :
            coeficienti = random.rand(gene)
            for i,crom in enumerate(cromozom) :
                if (coeficienti[i] < pm) :
                    cromozom[i] = 1 - crom
    return copii

def evaluare_populatie (populatie,marime_populatie) :
    suma = 0
    for crom in populatie:
        valoare_totala = 0
        greutate_totala = 0
        for index,each in enumerate(crom):
            if each == 1:
                valoare_totala = valoare_totala + valori[index]
                greutate_totala = greutate_totala + greutati[index]
        if (greutate_totala <= greutate_maxima) :
            suma += valoare_totala
        else :
            suma -= valoare_totala
    return suma/marime_populatie
        
def cel_mai_bun_scor (populatie, marime_populatie) :
    valoare_maxima = 0
    for crom in populatie:
        valoare_totala = 0
        greutate_totala = 0
        for index,each in enumerate(crom):
            if each == 1:
                valoare_totala = valoare_totala + valori[index]
                greutate_totala = greutate_totala + greutati[index]
        if (greutate_totala <= greutate_maxima and valoare_totala > valoare_maxima) :
            valoare_maxima = valoare_totala
    return valoare_maxima

def calcul_convergenta (populatie, marime_populatie) :
    maxim = 0
    cel_mai_intalnit = populatie[0]
    for crom1 in populatie:
        la_fel = 0
        for crom2 in populatie:
            if (crom1 == crom2).all() :
                la_fel = la_fel + 1;

        if (la_fel > maxim) :
            maxim = la_fel
            cel_mai_intalnit = crom1
    convergenta = 0
    for crom in populatie:
        if not(crom == cel_mai_intalnit).all() :
            convergenta = convergenta + 1
    return convergenta
            
de_ales = 60
marime_populatie = 100
gene = 8
numar_pasi = 200
valori = [30,15,60,85,100,10,25,45]
greutati=[5,14,6,8,14,11,4,6]
greutate_maxima = 30

populatie = initializare_populatie(marime_populatie)

solutie = 0
evaluari = []
convergente = []
convergenta = calcul_convergenta (populatie, marime_populatie)
pas = 0
while (convergenta > 3):
    pas = pas + 1
    parinti = selectie (populatie, de_ales, marime_populatie)

    copii = []
    for i in range(0,de_ales,2):
        copii.extend (incrucisare (parinti[i], parinti[i+1], gene))

    copii = aplica_mutatii (copii, gene)

    populatie.extend (copii)

    populatie = selectie (populatie,marime_populatie, marime_populatie+de_ales)
    scor =  cel_mai_bun_scor (populatie, marime_populatie)
    convergenta = calcul_convergenta(populatie, marime_populatie)
    if scor > solutie:
        solutie = scor
    evaluare = evaluare_populatie (populatie,marime_populatie)
    print (evaluare, convergenta )
    evaluari.append (evaluare)
    convergente.append (convergenta)

print (calcul_adecvare_final(populatie))
plt.plot (evaluari)
plt.show()
plt.plot (convergente)
plt.show()
#print ("Solutia problemei este: ")
#print (solutie)
