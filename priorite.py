#coding: utf-8

class File_Priorite:
    def __init__(self, liste = []):
        self.tab = [None]
        self.indices = {}
        for cle, valeur in liste:
            self.ajouter(cle, valeur)

    def _echanger(self, i1, i2):
        assert len(self.tab) == len(self.indices) + 1
        self.tab[i1], self.tab[i2] = self.tab[i2], self.tab[i1]
        self.indices[ self.tab[i1][0] ] = i1
        self.indices[ self.tab[i2][0] ] = i2

    def _ajouter_feuille(self,cle, valeur):
        self.tab.append((cle,valeur))
        self.indices[cle] = len(self.tab) - 1
 

    def ajouter(self,cle, valeur):
        if cle in self:
            raise Exception("clé déjà présente dans la file")

        self._ajouter_feuille(cle, valeur)
        i = self.indices[cle]

        while i>1 and self.tab[i/2][1] > self.tab[i][1] :
            self._echanger(i, i/2)
            i = i/2


    def diminuer_valeur(self, cle, nouvelle_val):
        assert len(self.tab) == len(self.indices) + 1
        i = self.indices[cle]
        self.tab[i] = (cle, nouvelle_val)
        while i>1 and self.tab[i/2][1] > self.tab[i][1]:
            self._echanger(i, i/2)
            i = i/2

    def extraire_min(self):
        assert len(self.tab) == len(self.indices) + 1
        if len(self.tab) <=1:
            raise Exception("La file de priorités est vide")
        result = self.tab[1]
 
 
        self.indices.pop(result[0])
        if len(self.tab) == 2:
            self.tab.pop()
            return result
        self.tab[1] = self.tab.pop()
        i = 1
        fini = False
        while not fini:
            fini = True
            mini = self.tab[i][1]
            if 2*i < len(self.tab):
                mini = min(mini, self.tab[2*i][1])
            if 2*i + 1 < len(self.tab): 
                mini = min(mini, self.tab[2*i+1][1])
            if mini < self.tab[i][1]:
                fini = False
                if mini == self.tab[2*i][1]:
                    self._echanger(i,2*i)
                    i = 2*i
                else:
                    self._echanger(i,2*i+1)
                    i = 2*i +1

        return result

    def __nonzero__(self):
        return len(self.tab) > 1

    def __contains__(self, cle):
        return cle in self.indices
