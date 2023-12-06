
class Node:
    
    def __init__(self, key):
        self.val = key
        self.childs = []
    
    def __str__(self) :
        ret = str(self.val) + " pere de [ "
        other_nodes = ""
        for child in self.childs :
            ret += str(child.val) + " "
            other_nodes += child.__str__()
        ret = ret + "]\n" + other_nodes
        return ret


class HeapMin:
    
    def __init__(self, key):
        self.root = Node(key)
        self.size = 1
    
    def __str__(self) :
        return "HeapMin\n" + self.root.__str__()
    
    def union(self, hm2):
        if self.size != hm2.size:
            raise IllegalArgumentException("Union of heaps of different sizes impossible.")
        if self.root.val > hm2.root.val:
            return hm2.union(self)
        else:
            self.root.childs = [hm2.root] + self.root.childs
            self.size += hm2.size
            return self


class BinomialQueue:
    
    def __init__(self):
        self.heaps = [] # tableau, ou head d'une liked list de heap min ?
        self.size = 0
    
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
    
    h1 = HeapMin(4)
    h2 = HeapMin(2)
    hu1 = h1.union(h2)
    print(hu1)

    h3 = HeapMin(5)
    h4 = HeapMin(3)
    hu2 = h4.union(h3)
    print(hu2)
    
    h = hu2.union(hu1)    
    print(h)
    


def main():
    test()
    print("Done.")


if __name__ == "__main__":
    main()