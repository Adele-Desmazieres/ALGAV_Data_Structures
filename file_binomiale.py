
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
        
        if self.child:
            ret += ", pere de " + str(self.child.val)
            others += self.child.__str__()
        
        if self.next_bro:
            ret += ", frere de " + str(self.next_bro.val)
            others += self.next_bro.__str__()
        
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
        return l.append(self)
    
    def degre(self):
        return len(self.child.getBrothers())
    
    def sortByDeg(self):
        root = self
        curr = self
        while curr not None:
            pass
            # TODO
        
        
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
        racine = node.sortByDeg()
        self.head = racine
        self.min_key_node = min(node.getBrothers())
        return self
    
    def initTournois(node):
        self.head = node
        self.min_key_node = node
        return self
    
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
    print(n7)

    #b = BinomialQueue()
    
    #print(n7)
    
    


def main():
    test()
    print("Done.")


if __name__ == "__main__":
    main()