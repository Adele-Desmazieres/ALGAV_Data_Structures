
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
        
        if self.child:
            ret += "\n" + str(self.val) + " père de " + str(self.child.val)
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
            s += "\t> Head : " + str(self.head.val) + "\n"
            s += "\t> Tail : " + str(self.tail.val) + "\n"
            s += "\t> MinKey : " + str(self.min_key_node.val) + "\n"
            return s + self.head.__str__()
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
    
    def AjoutMin(self, tournois):
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
    
    def Ajout(self, key):
        pass
    
    def Union(self, bq2):
        pass
    
    def Construction(keys):
        b = BinomialQueue()
        for key in keys:
            b.Ajout(key)
        return b    
    
    def SupprMin(self):
        pass
    


def test():
    
    n7 = Node(7)
    n12 = Node(12)
    n8 = Node(8)
    n13 = Node(13)
    
    n7 = n7.union(n8)
    n12 = n12.union(n13)
    n7 = n12.union(n7)
    
    b = BinomialQueue()
    print(n7)
    
    
    # TEST DECAPITE 
    
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
    


def main():
    test()
    print("Done.")


if __name__ == "__main__":
    main()