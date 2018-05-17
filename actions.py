#coding: utf-8
"""
    Les actions que vous écrirez prennent en paramètre un modele. 
    Les objets manipulés sont :
        - les sommets (visuellement, les cases hexagonales). 
             (Les sommets sont des objets 'Hex' mais 
             vous n'avez pas besoin de les manipuler directement,
             seulement de les passer en paramètre.)

        - les flèches 
            (même remarque que pour les sommets 
            ce sont en fait des entiers qui representent des objets manipulés
            par la bibliothèque graphique Tkinter)
    
    Les methodes de l'objet modele utilisables sont les suivantes :

    ### METHODES LIEES AU MODELE THEORIQUE #########################

    modele.getListeSommets():
        renvoie la liste des sommets du modele. 
        Rq : modele.getListeSommets(True) renvoie la liste de tous les
        sommets même noirs

    modele.getDepart():
        renvoie le sommet de départ

    modele.getObjectif(self):
        renvoie le sommet objectif

    modele.getVoisins(self, sommet):
        renvoie la liste des sommets voisins d'un sommet donné.
        Rq : modele.getVoisins(True) renvoie la liste de tous les
        voisins même noirs

    modele.longueur(sommet1, sommet2):
        renvoie la longueur de l'arete entre ces deux sommets
        configurable en changeant les valeurs dans hexa_modele

    ### METHODES GRAPHIQUES #########################
    
    modele.addFleche(sommet1, sommet2, couleur): 
        ajoute une fleche du sommet 1 au sommet 2, de la couleur donnée,
        et renvoie un indentifiant (un entier) qui permet de la supprimer plus tard
        couleurs : "Black", "Red", etc.

    modele.delFleche(ref):
        supprimer la fleche dont l'identifiant est ref

    modele.addTexte(sommet, texte):
        ajoute un texte sur le sommet donne. Renvoie un identifiant pour 
        pouvoir le supprimer.
        
    modele.deltexte(ref):
        suppprime le texte dont l'identifiant est ref.

"""



from hexa_modele import *
from collections import deque
import random
import time
import priorite
import sys

sys.setrecursionlimit(666666) # augmente la pile

"""
#############################################################
#                        Utilitaire                         #
#############################################################
"""

def tracerChemin(modele,pred):
    """ trace le plus court chemin """
    
    courant = modele.getObjectif()
    while courant in pred :
        precedent = pred[courant]
        modele.addFleche(precedent,courant, "Red")
        courant = precedent
            
    modele.observateur.update()

def relacher_arc(modele,dist,pred,fleches,texte,v1,v2):
    """ Relache l'arc (v1,v2) et indique s'il y changement ou non """
    
    if dist[v1] + modele.longueur(v1,v2) < dist[v2] :
        dist[v2] = dist[v1] + modele.longueur(v1,v2)
        pred[v2] = v1
        if v2 in fleches :
            modele.delFleche(fleches[v2])
            modele.deltexte(texte[v2])
        fleches[v2] = modele.addFleche(v1,v2,"Gray")
        texte[v2] = modele.addTexte(v2,dist[v2])
        modele.observateur.update()
        return True 
    return False 
    
        
    
"""
#############################################################
#         Recherche de composantes connexes                 #
#############################################################
"""

def composantesConnexes(modele):
    """ Trouve les composantes connexes """
    
    num_composantes = {}
    liste_sommets = modele.getListeSommets()
    compteur_comp = 1
    
    for x in liste_sommets :
        # si x n'a pas de numéro, lancer un parcours...
        if x not in num_composantes :
            attente = deque([x])
            num_composantes[x] = compteur_comp
            modele.addTexte(x,compteur_comp)
            while attente:
                courant = attente.pop()
                for vois in modele.getVoisins(courant):
                    if not vois in num_composantes:
                        attente.append(vois)
                        num_composantes[vois] = compteur_comp
                        modele.addTexte(vois,compteur_comp)
   
            compteur_comp += 1
            modele.observateur.update()
    

"""
#############################################################
#                  Parcours en largeur                      #
#############################################################
"""

def parcoursEnLargeur(modele):
    """ effectue un parcours en largeur du sommet de depart 
    affiche les prédécesseurs par des flèches grises et le chemin jusqu'à
    l'objectif en rouge """
    
    print "Parcours en largeur ON"
    distance = {}
    distance[modele.getDepart()] = 0

    pred = {}
    attente = deque()
    attente.append(modele.getDepart())

    while attente:
        courant = attente.popleft()
        liste_vois = modele.getVoisins(courant)
        random.shuffle(liste_vois)
        
        for voisin in liste_vois:
            if not voisin in distance: # encore inconnu
                distance[voisin] = distance[courant] + 1
                pred[voisin] = courant
                attente.append(voisin)
                
                # méthodes graphiques
                modele.addFleche(courant,voisin,"Gray")
                modele.addTexte(voisin,distance[voisin])
                modele.observateur.update()
                time.sleep(0.01)
                
        # on trace en rouge 
        tracerChemin(modele,pred)
            
    
    

"""
#############################################################
#                  Parcours en profondeur                   #
#############################################################
"""

def parcoursEnProfondeur(modele):
    """ effectue un parcours en profondeur du sommet de depart 
    affiche les prédécesseurs par des flèches grises et le chemin jusqu'à
    l'objectif en rouge """
    
    print "Parcours en profondeur ON"
    
    pred = {}
    connu = {}
    liste_sommets = modele.getListeSommets()
    liste_sommets.remove(modele.getDepart())
    PP_etape(modele,modele.getDepart(),connu,pred)
    for x in liste_sommets :
        if x not in connu :
            PP_etape(modele, x,connu,pred)
    tracerChemin(modele,pred)
    
def PP_etape(modele, x,connu,pred):
    connu[x] = True
    voisins = modele.getVoisins(x)
    random.shuffle(voisins)
    for v in voisins:
        if v not in connu :
            pred[v] = x
            # méthodes graphiques
            modele.addFleche(x,v,"Gray")
            modele.observateur.update()
            time.sleep(0.01)
            PP_etape(modele, v, connu,pred)
        

"""
#############################################################
#              Parcours de Bellman-Ford                     #
#############################################################
"""

def bellmanFord(modele):
    """ Algo de Bellman-Ford , utile si graphe valué, dans le cas d'absence 
    de circuit  """
    
    print "Parcours Bellman-Ford ON"
    
    # intialisation
    fleches = {}
    texte = {}
    n = len(modele.getListeSommets())
    dist = {}
    
    for v in modele.getListeSommets():
        dist[v] = float("inf")
        
    dist[modele.getDepart()] = 0
    
    pred = {}
    
    for i in range(n-1):
        changement = False 
        # relache chaque sommet
        for v1 in modele.getListeSommets():
            for v2 in modele.getVoisins(v1):
                if relacher_arc(modele,dist,pred,fleches,texte,v1,v2):
                    changement = True
        if changement == False :
            tracerChemin(modele,pred)
            return
               
    


"""
#############################################################
#                Parcours de Dijkstra                       #
#############################################################
"""

def dijkstra(modele): 
    print "Algo Dijkstra ON"


"""
#############################################################
#                    Parcours avec A*                       #
#############################################################
"""
def astar(modele): 
    print "Algo A* ON"

