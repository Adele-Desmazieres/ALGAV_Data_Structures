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
	
	def Ajout(self, val) :
		if self.root : 
			# le chemin est la liste des bits de [taille arbre + 1] en binaire, sauf le bit le plus lourd
			chemin = [int(bit) for bit in bin(self.size + 1)[3:]] # [3:] car on supprime 0b et le first bit
			#print(chemin)
			self.root = self.root.AjoutNode(val, chemin)
		else :
			self.root = node(val)
		self.size += 1
	
	def toStr(self) :
		if not self.root :
			return "Empty tree\n"
		else :
			return self.root.toStr()
	
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


if __name__ == "__main__" :
	test()