import sys
print(sys.version)
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import math
import random
import operator

################################################################################################
#################################PARTIE I généré un LH##########################################
################################################################################################
#################1) le principe
#pour crée l'hypercube latin je crée une grille de taille DIM, NBpoint
#puis j'éxtrait de maniére aléatoire des DIM-tuples de cette grille pour crée les points du LH
#aprés avoir choisi un DIM-tuples j'enléves ses coordonnées de la grilles
#de cette maniéres je pioches des DIM-tuples qui remplise les conditions d'un LH(c'est des maths la flemme d'éxpliquer trust me i'm an engineer)
#exemple
#[[0,1,2,3,4],[0,1,2,3,4],[0,1,2,3,4]] dim=3 nbpoint=5 deviens
#point choisi[3 3 0]
#grille[[0,1,2,4],[0,1,2,4],[1,2,3,4]]

#point choisi[3 3 0][1 4 2]
#grille[[0,2,4],[0,1,2],[1,3,4]]

#point choisi[3 3 0][1 4 2][4 2 3]
#grille[[0,2],[0,1],[1,4]]
#et ainsi de suite jusqua ce que la grille sois vide.
###############2) les fonctions
#initialisation de la grille
def initgrid(NBpoint,DIM):
    grid=np.zeros((DIM,NBpoint),dtype=float)
    for i in range(0,DIM):
        for j in range(0,NBpoint):
            grid[i,j]=j
    return grid
#choisi un nombre aléatoire dans un tableau
def RandInArray(A):
    a=A[np.random.randint(0, np.size(A))]
    return a
#génére un point aléatoirement a partir de la grille
def GenPoint(grid,DIM):
    res=np.zeros(DIM,dtype=float)
    j=0
    for i in grid:
        res[j]=RandInArray(i)
        j=j+1
    return res
#enléve un point donné dans la grille
def delpointingrid(grid,point):
    j=0
    (a,b)=np.shape(grid)
    res=np.zeros((a,b-1),dtype=float)
    for i in point:
        res[j]=np.delete(grid[j],np.where(grid[j] ==  point[j]))
        j=j+1
    return res
#génére un LH avec le systeme expliquer précement
def getLH(DIM,NBpoint):
    grid = initgrid(NBpoint, DIM)
    LH=np.zeros((NBpoint,DIM),dtype=float)
    for i in range(0,NBpoint):
        p = GenPoint(grid, DIM)
        LH[i]=p
        grid=delpointingrid(grid,p)
    for i in range(0,DIM):
        for j in range(0,NBpoint):
            LH[j,i]=LH[j,i]/NBpoint
    return  LH
################################################################################################
#############################PARTIE II Algorithme génétic#######################################
################################################################################################
#################1) le principe
#https://www.youtube.com/watch?v=1i8muvzZkPw heu c'est mieux que du texte pour expliquer
#################2) les fonctions
#distance euclidienne en N dimmension
def d(x,y,DIM):
    acc=0
    for i in range(0,DIM):
        acc=acc+(x[i]-y[i])*(x[i]-y[i])
    acc=math.sqrt(acc)
    return acc
#critére d'évaluation maximin
def maximin(LH,DIM,NBpoint):
    acc=np.zeros(NBpoint,dtype=float)
    accfinal=np.zeros(NBpoint,dtype=float)
    for i  in range(0,NBpoint):
        for j in range(0,NBpoint):
            a=d(LH[i], LH[j], DIM)
            if a==0:
                acc[j]=999990
            else:
                acc[j]=a#trouver un moyen que cette case sois pas le minimum
        accfinal[i]=min(acc)
    return min(accfinal)
#échange 2 points (genre en 2 D tu échanges leurs colonnes) en N dim c'est trop chiant a visualiser mais tu vois le concept
#en gros tu permutes l'une de leurs variables
def swapVar(LH1,DIM,NBpoint):
    a=np.random.randint(0, NBpoint)
    b=np.random.randint(0, NBpoint)
    c=np.random.randint(0, DIM)
    acc=LH1[a][c]
    LH1[a][c]=LH1[b][c]
    LH1[b][c]=acc
    return LH1
#on permute 'impact%' des colonnes du LH (comme c'est impossible de faire un crossover sur des LH différent
# baaaaah j'ai crossover le LH avec lui méme... en quelque sorte c'est un LH consanguin
def muta(LH1,DIM,NBpoint,Impact):
    for i in range(0,(math.ceil(Impact*NBpoint))):
        LH1=swapVar(LH1,DIM,NBpoint)
    return LH1
#crossover1 et 2 et mutation 1 et 2 sont des tentatives de crossover et mutation foireuse
#le LH perdait ses propriétées et ca fesait de la merde
def crossover1(LH1,LH2,DIM,NBpoint):
    acc=np.zeros((NBpoint,DIM),dtype=int)
    for i in range(0,NBpoint):#il faut optimiser cette boucle (la separer en deux et virer le if
            if LH1[i][0]<NBpoint/2:
                acc[i]=LH1[i]
            if LH1[i][0]>NBpoint/2:
                acc[i]=LH2[i]
    return acc
def mutation(LH1,DIM,NBpoint):
    nbmuta=math.ceil(NBpoint/20)
    acc=np.zeros(DIM)
    for i in range(0,DIM):
        acc[i]=random.randint(0,NBpoint-1)
    for i in range(0,nbmuta):
        LH1[random.randint(0,NBpoint-1)]=acc
    return LH1
def crossover2(LH1,LH2,DIM,NBpoint):
    acc=np.zeros((NBpoint,DIM),dtype=int)
    for i in range(0,NBpoint):#il faut optimiser cette boucle (la separer en deux et virer le if
        if i%2==0:
            acc[i]=LH1[i]
        else:
            acc[i]=LH2[i]
    return acc
def maximinn(LH, DIM, NBpoint):
    acc = 0
    for i in range(0, NBpoint - 2):
        for j in range(i + 1, NBpoint - 1):
            acc = acc + 1 / (d(LH[i], LH[j], DIM) * d(LH[i], LH[j], DIM))
    return 1 / acc

def mutation2(LH1,DIM,NBpoint):
    nbmuta=math.ceil(NBpoint/20)
    acc=np.zeros(DIM)
    for i in range(0,DIM):
        acc[i]=random.randint(0,NBpoint-1)
    for i in range(0,nbmuta):
        LH1[random.randint(0,NBpoint-1)]=acc
    return LH1
#cf la vidéo
def muta3(LH1,LH2,ImpactCross):
    for i in range(0,math.floor(ImpactCross*DIM)):
        LH1[:,random.randint(0,DIM-1)]=LH2[:,random.randint(0,DIM-1)]
    return LH1
#ouai bah plot 2D et 3D sa sert a plot lol mdr et plot ca regroupe les 2 car je suis un flemmard
def plotLH2D(LH,NBpoint):
    for i in LH:
        [a,b]=i
        plt.plot([a],[b],'ro')
        plt.axis([0, NBpoint-1, 0, NBpoint-1])

    return
def plotLH3D(LH,NBpoint):
    fig = plt.figure()
    ax = plt.axes(projection='3d')
    for i in LH:
        [a,b,c]=i
    ax.scatter3D(LH[:,0],LH[:,1],LH[:,2]);

    return
def plot(LH,NBpoint,DIM):
    if DIM == 2:
        plotLH2D(LH, NBpoint)
    else:
        plotLH3D(LH, NBpoint)
#test lalgo genetiques avec plein de valeurs pour voir c'est quoi les paramétres optimaux
#et pour eviter de lancer 30 000 simulation on utilise un LH pour choisir les simulations qu'on va lancer
def testing(LH):
    acc=1
    for i in LH:
        fichier = open("datadim2.txt", "a")
        print("iteration numéro %d" %acc)
        acc=acc+1
        #DIM = math.ceil(i[0]/10)
        DIM=2
        NBpoint = math.ceil(i[1]*1.5)
        NBinitialLH = math.ceil(i[2]*1.5)
        SurvivorRate = i[3]/100
        ImpactCross = i[4]/100
        ImpactMuta = i[5]/1000
        print([DIM, NBpoint, NBinitialLH, SurvivorRate, ImpactCross, ImpactMuta])
        LH=genetic(DIM, NBpoint, NBinitialLH, SurvivorRate, ImpactCross, ImpactMuta)
        goodness=maximin(LH, DIM, NBpoint)
        print(goodness)

        fichier.write("%d" % DIM)
        fichier.write(", ")
        fichier.write("%d" % NBpoint)
        fichier.write(", ")
        fichier.write("%d" % NBinitialLH)
        fichier.write(", ")
        fichier.write("%g" % SurvivorRate )
        fichier.write(", ")
        fichier.write("%g" % ImpactCross)
        fichier.write(", ")
        fichier.write("%g" % ImpactMuta)
        fichier.write("\n")
        fichier.write("%g" % goodness)
        fichier.write("\n")
        fichier.close()
    return 0
def genetic(DIM,NBpoint,NBinitialLH,SurvivorRate,ImpactCross,ImpactMuta):
    LHlist=[]
    FitTab=[]
    #generation NBinitialLH LH et de leurs goodness(leur taux de si ils sont bien) wesh je sais pas comment on appelle sa en francais
    for i in range(0,NBinitialLH):
        LHlist.append(getLH(DIM,NBpoint))
        FitTab.append(maximin(LHlist[-1],DIM,NBpoint))
    #boucle principal
    ite=0
    while len(FitTab)>1:
        #evaluation des survivant
        ite+=1
        for i in range(0, len(LHlist)):
            FitTab[i]=(maximin(LHlist[i], DIM, NBpoint))
        #SEULS LES PLUS FORT RESTERONS on vire le 1-survivorate plus faibles
        #ce if sert a debugger pour eviter qu'un survivor rate trop bas face tout planter sur la derniére itération
        if (math.floor(SurvivorRate*len(FitTab)))==0:
            a=1
        else:
            a=(math.floor(SurvivorRate*len(FitTab)))
        #ici on vire les faibles
        for i in range(0,a):
            idmin = FitTab.index(min(FitTab))
            FitTab.remove(FitTab[idmin])
            del LHlist[idmin]
        idmax = FitTab.index(max(FitTab))
        #crossover tout les hypercubes sauf le méilleur lui on le garde au cas ou
        for i in range(0, len(FitTab)):
            if i != idmax:
                LHlist[i] = muta3(LHlist[i],LHlist[random.randint(0,len(FitTab)-1)], ImpactCross)
        # mutation de tout les hypercubes sauf le méilleur lui on le garde au cas ou
        for i in range(0, len(FitTab)):
            if i != idmax:
                LHlist[i] = muta(LHlist[i], DIM, NBpoint, ImpactMuta)
        tty = FitTab[idmax]
        #plt.axis([0, ite, 0, 1])
        print(tty)
        #plt.scatter(ite, tty)
        #plt.pause(0.00001)
    #plt.show()
    return LHlist[0]

acc=[]
DIM=2#dimension du cube
NBpoint=20#nombre de point dans le cube
NBinitialLH=200 #nombre de LH initial pour algo genetic
SurvivorRate=1-0.99 #% de survivant
ImpactCross=0.3 #% de colonne interchanger durant le cross over
ImpactMuta=0.05 #%de colonnes interchanger durant la mutation
from statistics import mean
acc=[]
acc2=[]
for i in range(0,10):
    LH = genetic(DIM,NBpoint,NBinitialLH,SurvivorRate,ImpactCross,ImpactMuta)
    acc.append(maximin(LH, DIM, NBpoint))
    acc2.append(maximinn(LH, DIM, NBpoint))
    #plot(LH, DIM)
    #plt.show()
    print(max(acc))
    print(mean(acc))
    print(max(acc2))
    print(mean(acc2))
    print("##################")
    #print(LH)