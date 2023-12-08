
class Node:
    
    def __init__(self, key):
        self.val = key
        self.child = None
        self.next_bro = None
        self.prev_bro = None
        
    def __str__(self) :
        ret = str(self.val)
        others = ""
        
        if self.next_bro:
            if self.next_bro.prev_bro == self:
                ret += " <-> "
            else:
                ret += " -> " 
            ret += str(self.next_bro.val)
            others += self.next_bro.__str__()
        
        if self.child:
            ret += ", pere de " + str(self.child.val)
            others += self.child.__str__()
        
        return ret + "\n" + others

    def setBigBrotherOf(self, n):
    """ Node, Node -> Node
        Met un noeud en tant que grand frère de l'autre."""
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
            return self
    
    def getBrothers(self):
    """ Node -> Node list
        Renvoie la liste des frères d'un noeud, lui compris."""
        l = []
        if self.next_bro:
            l = self.next_bro.getBrothers()
        l.append(self)
        return l
    
    def deg(self):
    """ Node -> int
        Renvoie le degré de la racine du tournois."""
        if self.child is None: return 0
        else: return len(self.child.getBrothers())
    
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
    

class BinomialQueue:
    
    # la file binomiale est une liste doublement chaînée de tournois
    # du tournois le plus petit au tournois le plus grand
    def __init__(self):
        self.head = None # le tournois le plus petit en taille
        self.min_key_node = None # le tournois dont la clef est la plus petite
    
    def initTournoisDecapite(node):
    """ Node -> BinomialQueue
        Renvoie la file binomiale constituée des tournois 
        obtenus en supprimant la racine du tournois."""
        b = BinomialQueue()
        if node.child is not None:
            root = node.child.sortByDeg()
            b.head = root
            b.min_key_node = min(node.getBrothers())
        return b
    
    def initTournois(node):
    """ Node -> BinomialQueue
        Renvoie la file binomiale constituée du tournois en argument."""
        b = BinomialQueue()
        b.head = node
        b.min_key_node = node
        return b
    
    def __str__(self):
        if self.head:
            return "File binomiale\n" + self.head.__str__()
        else:
            return "File binomiale vide\n"
    
    def isEmpty(self):
    """ BinomialQueue -> booleen
        Renvoie vrai ssi la file est vide."""
        return (self.head is None)
    
    def minDeg(self):
    """ BinomialQueue -> Node 
        Renvoie le tournois de degré minimum."""
        return self.head
    
    def reste(self):
        oldroot = self.head
        self.head = oldroot.next_bro
        oldroot.next_bro = None
        self.head.prev_bro = None
        return self
            
    def SupprMin(self):
        pass
    
    def Ajout(self, key):
        pass
    
    def Construction(keys):
        b = BinomialQueue()
        for key in keys:
            b.Ajout(key)
        return b
        
    def Union(self, bq2):
        pass



def test():
    
    n7 = Node(7)
    n12 = Node(12)
    n8 = Node(8)
    n13 = Node(13)
    
    #n7.child = n12
    #n12.setBigBrotherOf(n8)
    #n12.child = n13
    n7 = n7.union(n8)
    n12 = n12.union(n13)
    n7 = n12.union(n7)
    #print(n7)
    
    #b = BinomialQueue()
    #print(n7)
    
    
    # TEST DECAPITE 
    
    n7 = Node(7)
    n1 = Node(1)
    n3 = Node(3)
    n5 = Node(5)
    n2 = Node(2)

    n7.setBigBrotherOf(n1)
    n1.setBigBrotherOf(n3)
    n3.setBigBrotherOf(n5)
    n5.setBigBrotherOf(n2)

    n0 = Node(0)
    n0.child = n7
    
    b = BinomialQueue.initTournoisDecapite(n0)
    print(b) 
    


def main():
    test()
    print("Done.")


if __name__ == "__main__":
    main()