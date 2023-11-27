import random as rd # temporaire, pour test

class tas_min_interface :

    def SupprMin(self) :
        pass

    def Ajout(self) :
        pass
    
    def AjoutsIteratifs(self) :
        pass
    
    def Construction() :
        pass
    
    def Union(t1, t2) :
        pass


class node :

    def __init__(self, val) :
        self.val = val
        self.gauche = None # node
        self.droite = None # node

    def toStr(self) :
        elt_str = str(self.val)
        g_str = self.gauche.toStr() if self.gauche else "#"
        d_str = self.droite.toStr() if self.droite else "#"
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

    def initUnbalancedNode(keys, lenkeys) :
        if keys == [] :
            return None

        curr_node = node(keys[0])
        keys = keys[1:]
        lenkeys -= 1
        mid = (lenkeys + 1) // 2
        curr_node.gauche = node.initUnbalancedNode(keys[0:mid], mid)
        curr_node.droite = node.initUnbalancedNode(keys[mid:], lenkeys-mid)
        return curr_node

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


class tas_min_tree(tas_min_interface) :

    def __init__(self) :
        self.root = None
        self.size = 0

    def initVal(val) :
        t = tas_min_tree()
        t.root = node(val)
        return t

    def toStr(self) :
        if not self.root :
            return "Empty tree\n"
        else :
            return self.root.toStr()

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
            #print(chemin)
            self.root = self.root.AjoutNode(val, chemin)
        else :
            self.root = node(val)
        self.size += 1

    def AjoutsIteratifs(self, keys) :
        for k in keys :
            self.Ajout(k)

    def Construction(keys) :
        if keys == [] :
            return tas_min_tree()
        else :
            #root = node(keys[1])
            t1 = tas_min_tree()
            t1.root = node.initUnbalancedNode(keys, len(keys))
            t1.root = t1.root.equilibreTout()
            return t1


class tas_min_array(tas_min_interface) :
    
    def __init__(self) :
        self.t = [] # TODO check python list are okay, or use array module
        self.size = 0
    
    def getIndexFilsDroit(self, i_curr) :
        i_droit = 2 * i_curr + 2
        return i_droit if i_droit < self.size else None
    
    def getIndexFilsGauche(self, i_curr) :
        i_gauche = 2 * i_curr + 1
        return i_gauche if i_gauche < self.size else None
    
    def equilibreDescente(self, i_curr) :
        i_gauche = self.getIndexFilsGauche(i_curr)
        i_droit = self.getIndexFilsDroit(i_curr)
        
        i_swap = None
        
        if i_gauche and self.t[i_gauche] < self.t[i_curr] :
            i_swap = i_gauche
        
        if i_droit and self.t[i_droit] < self.t[i_gauche] :
            i_swap = i_droit
        
        if i_swap :
            self.t[i_curr], self.t[i_swap] = self.t[i_swap], self.t[i_curr]
            self.equilibreDescente(i_swap)
    
    def SupprMin(self) :
        last = self.t[self.size-1]
        self.t = [last] + self.t[1:self.size-1]
        self.size -= 1
        self.equilibreDescente(0)
    
    def Ajout(self, key) :
        self.t.append(key)
        self.size += 1
    
    def AjoutsIteratifs(self, keys) :
        for key in keys :
            self.Ajout(key)


def test() :

    t1 = tas_min_tree()
    for i in range(15, 0, -1) :
        t1.Ajout(i)
    print()
    print(t1.toStr())

    t2 = tas_min_tree()
    keys = [x for x in range(15, 0, -1)]
    t2.AjoutsIteratifs(keys)
    print(t2.toStr())

    keys1 = [5, 1, 2, 4, 6, 3]
    t3 = tas_min_tree.Construction(keys1)
    print(t3.toStr())

    t1 = tas_min_tree()
    for i in range(1, 9, 1) :
        t1.Ajout(i)
    print()
    print(t1.toStr())
    chemin1 = [int(bit) for bit in bin(t1.size)[3:]]
    print()
    print(chemin1)
    print()
    t1.SupprMin()
    print(t1.toStr())
    t3 = tas_min_tree()
    t3.Ajout(2)
    t3.Ajout(6)
    t3.Ajout(5)
    t3.Ajout(10)
    t3.Ajout(13)
    t3.Ajout(7)
    t3.Ajout(8)
    t3.Ajout(12)
    t3.Ajout(15)
    t3.Ajout(14)
    print()
    print(t3.toStr())
    chemin3 = [int(bit) for bit in bin(t3.size)[3:]]
    print()
    print(chemin3)
    print()
    t3.SupprMin()
    print(t3.toStr())


def test_array() :
    t1 = tas_min_array()
    for i in range(1, 16) :
        t1.Ajout(i)
    print(t1.t)
    t1.SupprMin()
    print(t1.t)
    
    t2 = tas_min_array()
    t2.AjoutsIteratifs([2, 6, 5, 10, 13, 7, 8, 12, 15, 14])
    print(t2.t)
    t2.SupprMin()
    print(t2.t)
    


if __name__ == "__main__" :
    #test_tree()
    test_array()
