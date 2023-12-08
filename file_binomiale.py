
class Node:
    
    def __init__(self, key):
        self.val = key
        self.child = None
        self.next_bro = None
        self.prev_bro = None
        
        #self.childs = []
    
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
        self.next_bro = n
        if n is not None:
            n.prev_bro = self
        
    def union(self, n):
        if n is None: return self
        
        if self.val > n.val:
            return n.union(self)
        else:
            n.setBigBrotherOf(self.child)
            self.child = n
            return self
    
    def getBrothers(self):
        l = []
        if self.next_bro:
            l = self.next_bro.getBrothers()
        l.append(self)
        return l
    
    def deg(self):
        return len(self.child.getBrothers())
    
    # TODO SORT PAR DEGRES ET PAS PAR VAL
    def sortByDeg(self):
        root = self
        curr = self
        nextnode = self
        
        while curr is not None:
            nextnode = curr.next_bro
            newprev = curr
            tmp = newprev.prev_bro
            #while (newprev and newprev.prev_bro and newprev.prev_bro.val > curr.val) or (not newprev):
            while tmp and tmp.val > curr.val:
                #print(tmp.val, newprev.val)
                newprev = tmp
                tmp = tmp.prev_bro
                
            if newprev == curr or newprev.val > curr.val:
                newprev = tmp
            
            a = root.val if root else "None"
            b = curr.val if curr else "None"
            c = nextnode.val if nextnode else "None"
            d = newprev.val if newprev else "None"
            e = tmp.val if tmp else "None"
            #print(a, b, c, d, e,"\n")

            if newprev != curr and newprev != curr.prev_bro:
                                
                if curr.prev_bro is not None: curr.prev_bro.next_bro = curr.next_bro
                if curr.next_bro is not None: curr.next_bro.prev_bro = curr.prev_bro
                
                if newprev is not None:
                    #print(True)
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
            #print(root)

        return root
    
    def decapite(self):
        return BinomialQueue.initTournoisDecapite(self)
    
    def file(self):
        return BinomialQueue.initTournois(self)
    

class BinomialQueue:
    
    # la file binomiale est une liste doublement chaînée de tournois
    # du tournois le plus petit au tournois le plus grand
    def __init__(self):
        self.head = None # la racine du tournois le plus petit
        self.min_key_node = None # la racine du tournois dont la clef est la plus petite
    
    def initTournoisDecapite(node):
        b = BinomialQueue()
        if node.child is not None:
            root = node.child.sortByDeg()
            b.head = root
            b.min_key_node = min(node.getBrothers())
        return b
    
    def initTournois(node):
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
        return (self.head is None)
    
    def minDeg(self):
        return self.minroot
    
    def reste(self):
        pass
    
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