from hexa_vue import *
from hexa_modele import *
from actions import *

class Controleur():
    def __init__(self, vue, model):
        self.vue = vue
        self.model = model

    def bouton(self, label):
          
        if label == "Effacer Tout":
            self.vue.grille.reset()
            self.model.reset()

        if label == "Effacer Resultats":
            self.vue.grille.resetResults()

        if label == "Parcours en profondeur":
            parcoursEnProfondeur(self.model)

        if label == "Parcours en largeur":
            parcoursEnLargeur(self.model)

        if label == "Bellman-Ford":
            bellmanFord(self.model)

        if label == "Dijskstra":
            dijkstra(self.model)

        if label == "Aleatoire":
            self.model.random()

        if label == "A star":
            astar(self.model)
            
        if label == "Composantes connexes" :
            composantesConnexes(self.model)


    def onLClick(self, hexCoord):
        couleur = self.vue.palette.choixDeCouleur.get()
        if couleur == "Depart":
            self.model.change_depart(hexCoord)
        elif couleur == "Objectif":
            self.model.change_objectif(hexCoord)
            print self.model.distance_a_vide(self.model.getDepart(), self.model.getObjectif())
        else:
            self.model.hexs[hexCoord].change_couleur(couleur)

if __name__ == '__main__':
    root = Root()
   
    root.mainloop()
