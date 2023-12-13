import random as rd

class Node:
    """ Représente un tournois binomial.
    Chaque noeud a une valeur et un degré. 
    Ses noeuds fils sont représentés par un lien vers son fils le plus à gauche
    (celui de degré maximal), ainsi qu'une liste doublement chaînée depuis
    ce fils vers ses frères. Cette liste doublement chaînée est triée 
    par ordre décroissant de degré des noeuds."""
    
    def __init__(self, key):
        self.val = key
        self.child = None
        self.next_bro = None
        self.prev_bro = None
        self.deg = 0
    
    def __str__(self) :
        ret = str(self.val) + " (degré " + str(self.deg) + ")"
        others = ""
        
        if self.next_bro:
            if self.next_bro.prev_bro == self:
                ret += " <-> "
            else:
                ret += " -> " 
            ret += str(self.next_bro.val)
            others += self.next_bro.__str__()
        #ret = ""
        if self.child:
            ret += "\n"
            ret += str(self.val) + " père de " + str([x.val for x in self.child.getBrothers()])
            others += self.child.__str__()
        
        return ret + "\n" + others

    def setBigBrotherOf(self, n):
        """ Node, Node -> Node
        Met un noeud en tant que grand frère de l'autre. 
        Ne met PAS à jour le degré du père."""
        self.next_bro = n
        if n is not None:
            n.prev_bro = self
        
    def union(self, n):
        """ Node, Node -> Node
        Renvoie l'union de deux tournois."""
        if n is None: return self
        
        if self.val > n.val:
            return n.union(self)
        else:
            n.setBigBrotherOf(self.child)
            self.child = n
            self.deg += 1
            return self
    
    def getBrothers(self):
        """ Node -> Node list
        Renvoie la liste des frères d'un noeud, lui compris, dans le même ordre."""
        l = [self]
        if self.next_bro:
            l += self.next_bro.getBrothers()
        return l
    
#    def deg(self):
#        """ Node -> int
#        Renvoie le degré de la racine du tournois."""
#        #if self.child is None: return 0
#        #else: return len(self.child.getBrothers())
#        return self.deg
    
    # TODO : A SUPPRIMER
    def sortByDeg(self):
        """ Node -> Node
        Tri les noeuds de cette fraterie par degré croissant.
        Utilise l'algorithme de tri par insertion."""
        root = self
        curr = self
        nextnode = self
        
        while curr is not None:
            nextnode = curr.next_bro
            newprev = curr
            tmp = newprev.prev_bro
            while tmp and tmp.deg() > curr.deg():
                newprev = tmp
                tmp = tmp.prev_bro
                
            if newprev == curr or newprev.deg() > curr.deg():
                newprev = tmp

            if newprev != curr and newprev != curr.prev_bro:
                                
                if curr.prev_bro is not None: curr.prev_bro.next_bro = curr.next_bro
                if curr.next_bro is not None: curr.next_bro.prev_bro = curr.prev_bro
                
                if newprev is not None:
                    newnext = newprev.next_bro
                    curr.next_bro = newnext
                    newnext.prev_bro = curr
                    newprev.next_bro = curr
                
                else:
                    curr.next_bro = root
                    root.prev_bro = curr
                    root = curr
                curr.prev_bro = newprev
            curr = nextnode
        return root
    
    def decapite(self):
        """ Node -> BinomialQueue
        Renvoie la file binomiale constituée des tournois 
        obtenus en supprimant la racine du tournois."""
        return BinomialQueue.initTournoisDecapite(self)
    
    def file(self):
        """ Node -> BinomialQueue
        Renvoie la file binomiale constituée du tournois en argument."""
        return BinomialQueue.initTournois(self)
    
    def getMinBro(self):
        if self.next_bro is None:
            return self
        else:
            mb = self.next_bro.getMinBro()
            mb = self if self.val < mb.val else mb
            return mb
    
    def isTournoisBinomial(self):
        # vérifier la décroissance des degrés des frères
        for b in self.getBrothers():
            if b.deg > self.deg: 
                print("Décroissance des degrés non respectée.")
                return False
        # vérifier la croissances des clefs des fils
        if self.child:
            for f in self.child.getBrothers():
                if f.val < self.val: 
                    print("Croissance des valeurs non respectée.")
                    return False
        return True

class BinomialQueue:
    """ La file binomiale est une liste doublement chaînée de tournois
    listés par ordre décroissant de taille.
    Elle possède un pointeur vers le premier tournois de la liste,
    un pointeur vers le dernier élément de la liste, et un pointeur vers
    le tournois dont la clef racine est de valeur minimale."""
    
    def __init__(self):
        self.head = None # le tournois le plus grand en taille, premier de la liste
        self.tail = None # le tournois le plus petit en taille, dernier de la liste
        self.min_key_node = None # le tournois dont la racine a la plus petite valeur de clef
    
    def initTournoisDecapite(tournois):
        """ Node -> BinomialQueue
        Renvoie la file binomiale constituée des tournois 
        obtenus en supprimant la racine du tournois."""
        b = BinomialQueue()
        if tournois.child is not None:
            b.head = tournois.child
            brothers = b.head.getBrothers()
            b.tail = brothers[tournois.deg - 1]
            b.min_key_node = b.head.getMinBro()
            tournois.child = None
            tournois.deg = 0
        return b
    
    def initTournois(node):
        """ Node -> BinomialQueue
        Renvoie la file binomiale contenant uniquement le tournois en argument."""
        b = BinomialQueue()
        b.head = node
        b.tail = node
        b.min_key_node = node
        return b
    
    def __str__(self):
        if self.head:
            s = "File binomiale\n"
            s += "< " + str(["TB"+str(b.deg) for b in self.head.getBrothers()]) + " >\n"
            s += "\t> Head : " + str(self.head.val) + " deg " + str(self.head.deg) + "\n"
            s += "\t> Tail : " + str(self.tail.val) + " deg " + str(self.tail.deg) + "\n"
            s += "\t> MinKey : " + str(self.min_key_node.val) + " deg " + str(self.min_key_node.deg) + "\n"
            #s += self.head.__str__()
            return s
        else:
            return "File binomiale vide\n"
    
    def isEmpty(self):
        """ BinomialQueue -> booleen
        Renvoie vrai ssi la file est vide."""
        return (self.head is None)
    
    def minDeg(self):
        """ BinomialQueue -> Node 
        Renvoie le tournois de degré minimum."""
        return self.tail
    
    def reste(self):
        """ BinomialQueue -> BinomialQueue
        Renvoie la file privée de son tournoi de degré minimal
        ou elle-même si la file est vide."""
        if self.isEmpty():
            return self
        
        removed = self.tail
        self.tail = removed.prev_bro
        removed.prev_bro = None
        if self.tail:
            self.tail.next_bro = None
            if self.min_key_node == removed:
                self.min_key_node = self.head.getMinBro()
        
        else:
            self.head = None
            self.min_key_node = None
        return self
    
    def ajoutMin(self, tournois):
        """ BinomialQueue * Node -> BinomialQueue
        Hypothèse : le tournoi est de degré inférieur au tournois de degré min.
        Renvoie la file obtenue en ajoutant le tournoi comme
        tournoi de degré minimal de la file initiale."""
        oldtail = self.tail
        oldtail.next_bro = tournois
        tournois.prev_bro = oldtail
        self.tail = tournois
        if tournois.val < self.min_key_node.val:
            self.min_key_node = tournois
        return self
            
    def UFret(self, F2, T):
        """ BinomialQueue * BinomialQueue * Node -> BinomialQueue
        Renvoie la file binomiale union de deux files et d'un tournoi."""
        F1 = self
        if T is None: # pas de tournoi en retenue
            if F1.isEmpty():
                return F2
            if F2.isEmpty():
                return F1
            T1 = F1.minDeg()
            T2 = F2.minDeg()
            if T1.deg < T2.deg:
                return F1.reste().UnionFile(F2).ajoutMin(T1)
            if T2.deg < T1.deg:
                return F2.reste().UnionFile(F1).ajoutMin(T2)
            else: # T1.deg == T2.deg
                return F1.reste().UFret(F2.reste(), T1.union(T2))
        
        else: # tournoi T en retenue
            if F1.isEmpty():
                return BinomialQueue.initTournois(T).UnionFile(F2)
            if F2.isEmpty():
                return BinomialQueue.initTournois(T).UnionFile(F1)
            T1 = F1.minDeg()
            T2 = F2.minDeg()
            if T.deg < T1.deg and T.deg < T2.deg:
                return F1.UnionFile(F2).ajoutMin(T)
            if T.deg == T1.deg and T.deg == T2.deg:
                return F1.reste().UFret(F2.reste(), T1.union(T2)).ajoutMin(T)
            if T.deg == T1.deg and T.deg < T2.deg:
                return F1.reste().UFret(F2, T1.union(T))
            if T.deg == T2.deg and T.deg < T1.deg:
                return F2.reste().UFret(F1, T2.union(T))
            else:
                print("=== WTF ?! ===")
                print(T.deg, T1.deg, T2.deg)
                print(T)
                print(F1)
                print(F2)
                print("=== WTF END ===")
            

    def UnionFile(self, F2):
        """ BinomialQueue * BinomialQueue -> BinomialQueue
        Renvoie la file résultant de l'union des deux files."""
        return self.UFret(F2, None)
    
    def Ajout(self, key):
        """ BinomialQueue * int -> BinomialQueue
        Renvoie la file résultant de l'ajout de la clef dans la file."""
        return self.UnionFile(BinomialQueue.initTournois(Node(key)))
    
    def Construction(keys):
        """ int list -> BinomialQueue
        Renvoie la file résultant des ajouts successifs des clefs dans une file vide."""
        print("Construction")
        b = BinomialQueue()
        for key in keys:
            b = b.Ajout(key)
        return b    
    
    def SupprMin(self):
        """ BinomialQueue -> BinomialQueue
        Renvoie la file résultant de la suppression de la clef de valeur minimale."""
        minTB = self.min_key_node
        print("Suppression de la racine du tournois TB" + str(minTB.deg))
        F1 = self.reste()
        F2 = BinomialQueue.initTournoisDecapite(minTB)
        return F1.UnionFile(F2)
    
    def isBinomialQueue(self):
        if self.head is None:
            return (self.tail is None and self.min_key_node is None)
        
        if self.head.prev_bro is not None:
            print("a")
            return False
        
        if self.tail.next_bro is not None:
            print("b")
            return False
        
        #brothers = self.head.getBrothers()
        m = self.head.getMinBro()
        if m != self.min_key_node:
            print("c")
            print(m.val)
            print(self.min_key_node.val)
            return False
            
        return self.head.isTournoisBinomial()


def testPrint():
    
    n7 = Node(7)
    n12 = Node(12)
    n8 = Node(8)
    n13 = Node(13)
    
    n7 = n7.union(n8)
    n12 = n12.union(n13)
    n7 = n12.union(n7)
    
    b = BinomialQueue()
    print(n7)

def testDecapite():
    n7 = Node(7)
    n12 = Node(12)
    n8 = Node(8)
    n13 = Node(13)
    
    n7 = n7.union(n8)
    n12 = n12.union(n13)
    n7 = n12.union(n7)
    
    n3 = Node(3)
    n10 = Node(10)
    n5 = Node(5)
    n9 = Node(9)
    
    n5 = n5.union(n9)
    n3 = n10.union(n3)
    n3 = n3.union(n5)
    
    n0 = n7.union(n3)
    
    b = BinomialQueue.initTournoisDecapite(n0)
    print(b)
    b = b.reste()
    print(b)
    b = b.reste()
    print(b)
    b = b.reste()
    print(b)
    b = b.reste()
    print(b)

def testUnion():
    n = 4
    k = [x for x in range(1, n+1)]
    rd.shuffle(k)
    tb0_a = Node(k[0])
    tb0_b = Node(k[1])
    tb0_c = Node(k[2])
    tb0_d = Node(k[3])
    
    f1_a = BinomialQueue.initTournois(tb0_a)
    f1_b = BinomialQueue.initTournois(tb0_b)
    f1_c = BinomialQueue.initTournois(tb0_c)
    f1_d = BinomialQueue.initTournois(tb0_d)
    
    f2_a = f1_a.UnionFile(f1_b)
    f3_a = f1_c.UnionFile(f2_a)
    f4_a = f3_a.UnionFile(f1_d)
    print(f4_a)
    assert(f4_a.isBinomialQueue())
    
def testConstructionSupp():
    n1 = 5
    n2 = 7
    
    k1 = [x for x in range(1, n1+1)]
    rd.shuffle(k1)
    print(k1)
    
    k2 = [x for x in range(n1+1, n1+n2+1)]
    rd.shuffle(k2)
    print(k2)
    
    
    f1 = BinomialQueue.Construction(k1)
    print(f1)
    assert(f1.isBinomialQueue())
    
    f2 = BinomialQueue.Construction(k2)
    print(f2)
    assert(f2.isBinomialQueue())
    
    f3 = f1.UnionFile(f2)
    print(f3)
    assert(f3.isBinomialQueue())
    
    # TESTS DE SUPPR
    while not f3.isEmpty():
        f3 = f3.SupprMin()
        print(f3)
        assert(f3.isBinomialQueue())

def main():
    #testPrint()
    #testDecapite()
    #testUnion()
    testConstructionSupp()
    print("Done.")


if __name__ == "__main__":
    main()