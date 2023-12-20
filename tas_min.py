import random as rd
import int_representation as ir

class tas_min_interface :

    def SupprMin(self) :
        pass

    def Ajout(self, key) :
        pass
    
    def AjoutsIteratifs(self, keys) :
        pass
    
    def AjoutsIteratifsStatic(keys) :
        pass
    
    def Construction(keys) :
        pass
    
    def Union(t1, t2) :
        pass


class node :

    def __init__(self, val) :
        self.val = val
        self.gauche = None # node
        self.droite = None # node

    def __str__(self) :
        elt_str = str(self.val)
        g_str = self.gauche.__str__() if self.gauche else "#"
        d_str = self.droite.__str__() if self.droite else "#"
        return "(" + g_str + ", " + elt_str + ", " + d_str + ")"

    def equilibreUnEtage(self, n, isFromRight) :
        if n.val < self.val :
            nd, ng = n.droite, n.gauche

            if isFromRight :
                n.droite = self
                n.gauche = self.gauche

            else :
                n.droite = self.droite
                n.gauche = self

            self.droite = nd
            self.gauche = ng
            return n

        else :
            if isFromRight :
                self.droite = n
            else :
                self.gauche = n
            return self

    def equilibreDescente(self) :
        d = self.droite
        g = self.gauche

        # pas d'échange de valeur
        if (not d and not g) or \
                (not d and g.val > self.val) or \
                (d and d.val > self.val and g.val > self.val) :
            return self

        # échange à droite
        elif (d and d.val < self.val and d.val < g.val) :
            d2, g2 = d.droite, d.gauche
            d.droite = self
            d.gauche = g
            self.droite = d2
            self.gauche = g2
            d.droite = d.droite.equilibreDescente()
            return d

        # échange à gauche
        else :
            d2, g2 = g.droite, g.gauche
            g.droite = d
            g.gauche = self
            self.droite = d2
            self.gauche = g2
            g.gauche = g.gauche.equilibreDescente()
            return g

    def recuperer(self,chemin) :
        if chemin == [0] :
            return self, self.gauche, 0
        elif chemin == [1] :
            return self, self.droite, 1
        else :
            if chemin[0] == 0 :
                return self.gauche.recuperer(chemin[1:])
            else :
                return self.droite.recuperer(chemin[1:])

    def AjoutNode(self, val, chemin) :
        if chemin == [0] :
            n = node(val)
            return self.equilibreUnEtage(n, 0)

        elif chemin == [1] :
            n = node(val)
            return self.equilibreUnEtage(n, 1)

        else :
            if chemin[0] == 0 :
                n = self.gauche.AjoutNode(val, chemin[1:])
                return self.equilibreUnEtage(n, 0)
            else :
                n = self.droite.AjoutNode(val, chemin[1:])
                return self.equilibreUnEtage(n, 1)

    def initUnbalancedNodes(self, keys, lenkeys, i_curr) :
        i_gauche = i_curr * 2 + 1
        i_droite = i_curr * 2 + 2
        
        if i_gauche < lenkeys :
            self.gauche = node(keys[i_gauche])
            self.gauche.initUnbalancedNodes(keys, lenkeys, i_gauche)
        
        if i_droite < lenkeys :
            self.droite = node(keys[i_droite])
            self.droite.initUnbalancedNodes(keys, lenkeys, i_droite)
        
        return self

    # parcours suffixe, rééquilibre tous les noeuds
    def equilibreTout(self) :
        if not self.gauche :
            return self

        else :
            self.gauche = self.gauche.equilibreTout()
            if self.droite :
                self.droite = self.droite.equilibreTout()
            rootnode = self.equilibreDescente()
            
            return rootnode

        # TENTATIVE POUR LE FAIRE FONCTIONNER AVEC DES REMONTEES
        # MAIS IL FAUDRAIT REMONTER PLUS D'UN ETAGE CHAQUE NOEUD        
        #print("equilibreTout")
        #curr = self
        #
        #if curr.gauche :
        #    curr = curr.equilibreUnEtage(curr.gauche, 0)
        #    curr.gauche = curr.gauche.equilibreTout()
        #if curr.droite :
        #    curr = curr.equilibreUnEtage(curr.droite, 1)
        #    curr.droite = curr.droite.equilibreTout()
        #return curr

    def equilibreDescente(self) :
        d = self.droite
        g = self.gauche

        # pas d'échange de valeur
        if (not d and not g) or \
                (not d and g.val > self.val) or \
                (d and d.val > self.val and g.val > self.val) :
            return self

        # échange à droite
        elif (d and d.val < self.val and d.val < g.val) :
            d2, g2 = d.droite, d.gauche
            d.droite = self
            d.gauche = g
            self.droite = d2
            self.gauche = g2
            d.droite = d.droite.equilibreDescente()
            return d

        # échange à gauche
        else :
            d2, g2 = g.droite, g.gauche
            g.droite = d
            g.gauche = self
            self.droite = d2
            self.gauche = g2
            g.gauche = g.gauche.equilibreDescente()
            return g
    
    def getKeys(self) :
        res = []
        if self.droite:
            res = self.droite.getKeys()
        if self.gauche:
            res += self.gauche.getKeys()
        res.append(self.val)
        return res
    
    def isWellFormed(self) :
        file = []
        file.append(self)
        reachedLastNode = False
        
        while len(file) > 0 :
            curr_node = file[0]
            file = file[1:]
            if curr_node.gauche :
                if reachedLastNode :
                    print("Arbre mal formé pour un tas min.")
                    return False
                file.append(curr_node.gauche)
            else :
                reachedLastNode = True
            
            if curr_node.droite :
                if reachedLastNode :
                    print("Arbre mal formé pour un tas min.")
                    return False
                file.append(curr_node.droite)
            else :
                reachedLastNode = True
        
        return True
    
    def isCroissant(self) :
        d, g = True, True
        if self.droite :
            if self.val > self.droite.val : 
                print("Arbre non croissant.")
                return False
            d = self.droite.isCroissant()
        if self.gauche :
            if self.val > self.gauche.val : 
                print("Arbre non croissant.")
                return False
            g = self.gauche.isCroissant()
        return (g and d)
        
    def getNumberDesc(self) :
        d, g = 0, 0
        if self.droite :
            d = self.droite.getNumberDesc()
        if self.gauche :
            g = self.gauche.getNumberDesc()
        return (1 + g + d)        
    
    # vérifie que l'arbre a une forme de tas min 
    # (feuilles réparties sur un ou deux étages, et entassées le plus à gauche)
    # que les valeurs de ses noeuds sont croissants depuis la racine
    # et que sa taille est égale à son nombre de noeuds
    def isTasMinNode(self, size) :
        a = self.isWellFormed()
        b = self.isCroissant()
        n = self.getNumberDesc()
        c = True
        if n != size :
            print("Mauvais nombre de noeuds dans l'arbre : ", n, " VS ", size, ".", sep='')
            c = False
        return (a and b and c)
    

class tas_min_tree(tas_min_interface) :

    def __init__(self) :
        self.root = None
        self.size = 0

    def initVal(val) :
        t = tas_min_tree()
        t.root = node(val)
        return t

    def __str__(self) :
        if not self.root :
            return "Empty tree\n"
        else :
            return self.root.__str__()

    def SupprMin(self) :
        if self.size == 0 :
            return None
        elif self.size == 1 :
            self.root = None
            self.size -= 1
        else :
            chemin = [int(bit) for bit in bin(self.size)[3:]]
            triple = self.root.recuperer(chemin)
            parent = triple[0]
            enfant = triple[1]
            dernier_chemin = triple[2]
            if dernier_chemin == 0 :
                enfant.gauche = self.root.gauche
                enfant.droite = self.root.droite
                parent.gauche = None
                self.root = enfant
            else :
                enfant.gauche = self.root.gauche
                enfant.droite = self.root.droite
                parent.droite = None
                self.root = enfant
            self.root = self.root.equilibreDescente()
            self.size -= 1

    def Ajout(self, val) :
        if self.root :
            # le chemin est la liste des bits de [taille arbre + 1] en binaire, sauf le bit le plus lourd
            chemin = [int(bit) for bit in bin(self.size + 1)[3:]] # [3:] car on supprime 0b et le first bit
            self.root = self.root.AjoutNode(val, chemin)
        else :
            self.root = node(val)
        self.size += 1

    def AjoutsIteratifs(self, keys) :
        for k in keys :
            self.Ajout(k)

    def AjoutsIteratifsStatic(keys) :
        ret = tas_min_tree()
        ret.AjoutsIteratifs(keys)
        return ret

    def Construction(keys) :
        if keys == [] :
            return tas_min_tree()
        else :
            t1 = tas_min_tree()
            t1.root = node(keys[0])
            t1.root.initUnbalancedNodes(keys, len(keys), 0)
            t1.size = len(keys)
            t1.root = t1.root.equilibreTout()
            return t1
    
    def Union(t1, t2) :
        if not t1.root :
            return t2
        elif not t2.root :
            return t1
        else :
            k1 = t1.root.getKeys()
            k2 = t2.root.getKeys()
            keys = k1 + k2
            res = tas_min_tree.Construction(keys)
            return res
    
    def isTasMin(self) :
        if not self.root :
            return (self.size == 0)
        return self.root.isTasMinNode(self.size)


class tas_min_array(tas_min_interface) :
    
    def __init__(self) :
        self.t = []
        self.size = 0
    
    def __str__(self) :
        return "[" + (", ".join([str(x) for x in self.t])) + "]"
    
    def getIndexFilsDroit(self, i_curr) :
        i_droit = 2 * i_curr + 2
        return i_droit if i_droit < self.size else -1
    
    def getIndexFilsGauche(self, i_curr) :
        i_gauche = 2 * i_curr + 1
        return i_gauche if i_gauche < self.size else -1
    
    def getIndexPere(self, i_curr) :
        return (i_curr - 1) // 2 if i_curr > 0 else -1
    
    def equilibreDescente(self, i_curr) :
        i_gauche = self.getIndexFilsGauche(i_curr)
        i_droit = self.getIndexFilsDroit(i_curr)
        
        i_swap = -1
        
        if i_gauche > 0 and self.t[i_gauche] < self.t[i_curr] :
            i_swap = i_gauche
        
        if i_droit > 0 and self.t[i_droit] < self.t[i_gauche] and self.t[i_droit] < self.t[i_curr] :
            i_swap = i_droit
        
        if i_swap > 0 :
            self.t[i_curr], self.t[i_swap] = self.t[i_swap], self.t[i_curr]
            self.equilibreDescente(i_swap)
    
    def SupprMin(self) :
        last = self.t[self.size-1]
        self.t = [last] + self.t[1:self.size-1]
        self.size -= 1
        self.equilibreDescente(0)
    
    def equilibreMontee(self, i_curr) :
        i_pere = self.getIndexPere(i_curr)
        
        if i_pere > -1 and self.t[i_pere] > self.t[i_curr] :
            self.t[i_curr], self.t[i_pere] = self.t[i_pere], self.t[i_curr]
            self.equilibreMontee(i_pere)
    
    def Ajout(self, key) :
        self.t.append(key)
        self.size += 1
        self.equilibreMontee(self.size-1)
    
    def AjoutsIteratifs(self, keys) :
        for key in keys :
            self.Ajout(key)
    
    def AjoutsIteratifsStatic(keys) :
        ret = tas_min_array()
        ret.AjoutsIteratifs(keys)
        return ret
    
    def equilibreTout(self, i_curr) :
        i_gauche = self.getIndexFilsGauche(i_curr)
        i_droite = self.getIndexFilsDroit(i_curr)
        
        if i_gauche > 0 :
           self.equilibreTout(i_gauche)
        if i_droite > 0 :
           self.equilibreTout(i_droite)

        #print(self.__str__(), i_curr, self.t[i_curr])
        self.equilibreDescente(i_curr)
    
    def Construction(keys) :
        if keys == [] :
            return tas_min_array()
        else :
            t1 = tas_min_array()
            t1.t = keys
            t1.size = len(keys)
            t1.equilibreTout(0)
            return t1
    
    def Union(t1, t2) :
        return tas_min_array.Construction(t1.t + t2.t)
    
    def isWellFormed(self) :
        return all([(x is not None) for x in self.t])
    
    def isCroissant(self, i_curr) :
        i_g = self.getIndexFilsGauche(i_curr)
        i_d = self.getIndexFilsDroit(i_curr)
        g, d = True, True
        
        if i_g > 0 :
            if self.t[i_curr] > self.t[i_g] :
                print("Tableau non croissant.")
                return False
            else :
                g = self.isCroissant(i_g)
        
        if i_d > 0 :
            if self.t[i_curr] > self.t[i_d] :
                print("Tableau non croissant.")
                return False
            else :
                d = self.isCroissant(i_d)
        
        return (g and d)
    
    def isTasMin(self) :
        if self.t == [] :
            return (self.size == 0)
        a = self.isWellFormed()
        if not a : print("Elément None dans le tableau.")
        b = self.isCroissant(0)
        c = True
        if len(self.t) != self.size :
            print("Mauvais nombre d'éléments dans le tableau.")
            c = False
        return (a and b and c)



def test_tree() :
    keys = [x for x in range(1,6)]
    rd.shuffle(keys)
    
    t1 = tas_min_tree()
    t1.AjoutsIteratifs(keys)
    t2 = tas_min_tree.Construction(keys)
    
    print(t1)
    print(t2)
    

def test_array() :
    t1 = tas_min_array()
    for i in range(1, 16) :
        t1.Ajout(i)
    print(t1)
    t1.SupprMin()
    print(t1)
    
    t2 = tas_min_array()
    t2.AjoutsIteratifs([2, 6, 5, 10, 13, 7, 8, 12, 15, 14])
    print(t2)
    t2.SupprMin()
    print(t2)
    print()
    
    
    #keys = [x for x in range(2, 8)]
    keys = [5, 1, 2, 4, 6, 3]
    
    t3arbre = tas_min_tree()
    t3arbre.AjoutsIteratifs(keys)
    print(t3arbre)
    
    t3 = tas_min_array()
    t3.AjoutsIteratifs(keys)
    print(t3)
    

def test_construction() :
    #keys = [x for x in range(1,6)]
    keys = [1, 4, 2, 5, 3]
    rd.shuffle(keys)
    print(keys)
    
    tt = tas_min_tree.Construction(keys)
    ta = tas_min_array.Construction(keys)
    
    print(tt)
    print(ta)


def test_union() :
    k1 = [ir.uint128(x) for x in range(1, 11)]
    k2 = [ir.uint128(x) for x in range(11, 21)]
    rd.shuffle(k1)
    rd.shuffle(k2)
    
    tt1 = tas_min_tree.Construction(k1)
    tt2 = tas_min_tree.Construction(k2)
    ttu = tas_min_tree.Union(tt1, tt2)
    print(ttu, "\n")
    assert(ttu.isTasMin())
    
    ta1 = tas_min_array.Construction(k1)
    ta2 = tas_min_array.Construction(k2)
    tau = tas_min_array.Union(ta1, ta2)
    print(tau, "\n")
    assert(tau.isTasMin())
    
    print("Tests d'union validés.")


if __name__ == "__main__" :
    #test_tree()
    #test_array()
    #test_construction()
    test_union()
    
