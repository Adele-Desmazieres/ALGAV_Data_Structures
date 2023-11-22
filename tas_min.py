import random as rd # temporaire, pour test

class tas_min_interface :
	
	def SupprMin(self) :
		pass
	
	def Ajout(self) :
		pass


class node :
	
	def __init__(self, val) :
		self.val = val
		self.gauche = None # node
		self.droite = None # node
	
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
	
	def AjoutFin(self, val, chemin) :
		print(self.toStr())
		if chemin == [0] :
			n = node(val)
			#self.gauche = n
			return self.equilibreUnEtage(n, 0)
			
		elif chemin == [1] :
			n = node(val)
			#self.droite = n
			return self.equilibreUnEtage(n, 1)
		
		else : 
			if chemin[0] == 0 :
				n = self.gauche.AjoutFin(val, chemin[1:])
				return self.equilibreUnEtage(n, 0)
			else :
				n = self.droite.AjoutFin(val, chemin[1:])
				return self.equilibreUnEtage(n, 1)
	
	def toStr(self) :
		elt_str = str(self.val)
		g_str = self.gauche.toStr() if self.gauche else "#"
		d_str = self.droite.toStr() if self.droite else "#"
		return "(" + g_str + ", " + elt_str + ", " + d_str + ")"


class tas_min_tree(tas_min_interface) :
	
	def __init__(self) :
		self.root = None
		self.size = 0
	
	def init_val(val) :
		t = tas_min_tree()
		t.root = node(val)
		return t
	
	def AjoutFin(self, val) :
		if self.root : 
			# le chemin est la liste des bits de [taille arbre + 1] en binaire, sauf le bit le plus lourd
			chemin = [int(bit) for bit in bin(self.size + 1)[3:]] # [3:] car on supprime 0b et le first bit
			#print(chemin)
			self.root = self.root.AjoutFin(val, chemin)
		else :
			self.root = node(val)
		self.size += 1
	
	def toStr(self) :
		if not self.root :
			return "Empty tree\n"
		else :
			return self.root.toStr()



def test() :
	#rd.seed()
	#x = rd.randrange(100)
	#xnext = next_pow2(x)
	#print(x, xnext)
	#
	#x = 5
	#print(bin_list_of_size(5, -1))
	#
	#print([tmp(x) for x in range(8)])
	
	t1 = tas_min_tree()
	for i in range(1, 16, 1) :
		t1.AjoutFin(i)
	print()
	print(t1.toStr())


if __name__ == "__main__" :
	test()