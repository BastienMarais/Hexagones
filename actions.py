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

def tracerChemin(modele,pred):
    """trace le plus court chemin"""
    courant = modele.getObjectif()
    while courant in pred :
        precedent = pred[courant]
        modele.addFleche(precedent,courant, "Red")
        courant = precedent
            
    modele.observateur.update()
    

def parcoursEnLargeur(modele):
    """effectue un parcours en largeur du sommet de depart 
    affiche les prédécesseurs par des flèches grises et le chemin jusqu'à
    l'objectif en rouge"""
    
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
                
        # on trace en rouge 
        tracerChemin(modele,pred)
            
    
def composantesConnexes(modele):
    """Trouve les composantes connexes"""
    num_composantes = {}
    liste_sommets = modele.getListeSommets()
    compteur_comp = 0
    
    for x in liste_sommets :
        # si x n'a pas de numéro, lancer un parcours...
        if not x in num_composantes :
            attente = deque([x])
            num_composantes[x] = compteur_comp
            modele.addTexte(x,compteur_comp)
            while attente:
                courant = attente.pop()
                for vois in modele.getVoisins(courant):
                    if not vois in num_composantes:
                        attente.append(vois)
                        num_composantes[vois] = compteur_comp
                        modele.addTexte(voisin,compteur_comp)
   
        compteur_comp += 1
        modele.observateur.update()
    
    


def parcoursEnProfondeur(modele):
    """effectue un parcours en profondeur du sommet de depart 
    affiche les prédécesseurs par des flèches grises et le chemin jusqu'à
    l'objectif en rouge"""
    
    print "Parcours en profondeur ON"
    
    pred = {}
    connu = deque()
    for x in modele.getListeSommets() :
        if not connu[x] :
            PP_etape(x,connu,pred)
    
def PP_etape(x,connu,pred):
    connu[x] = True
    for v in model.getVoisins(x):
        if not connu[v] :
            pred[v] = x 
            # méthodes graphiques
            modele.addFleche(x,v,"Gray")
            modele.observateur.update()
            
            PP_etape(v, connu,pred)
        


def bellmanFord(modele):
    print "Algo de Bellman Ford ON"


def dijkstra(modele): 
    print "Algo Dijkstra ON"


def astar(modele): 
    print "Algo A* ON"

