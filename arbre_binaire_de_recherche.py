class node:
	def __init__(self,val):
		self.val = val
		self.gauche = None
		self.droite = None
		self.hauteur = 1

	def __str__(self) :
		elt_str = str(self.val)
		g_str = self.gauche.__str__() if self.gauche else "#"
		d_str = self.droite.__str__() if self.droite else "#"
		return "(" + g_str + ", " + elt_str + ", " + d_str + ")"

	def get_hauteur(self):
		if not self:
			return 0
		return self.hauteur

	def AjoutNode(self,e):
		ajout = True
		if not self:
			return node(e),ajout
		if e == self.val:
			ajout = False
			return self,ajout
		elif e < self.val:
			if self.gauche:
				self.gauche,ajout = self.gauche.AjoutNode(e)
			else :
				self.gauche = node(e)
		else:
			if self.droite:
				self.droite,ajout = self.droite.AjoutNode(e)
			else :
				self.droite = node(e)

		self.hauteur = 1 + max(node.get_hauteur(self.gauche),node.get_hauteur(self.droite))

		equilibre = self.valeur_equilibre()

		if equilibre > 1:
			if e < self.gauche.val:
				return self.RR(),ajout
			else:
				self.gauche = self.gauche.LR()
				return self.RR(),ajout

		if equilibre < -1:
			if e > self.droite.val:
				return self.LR(),ajout
			else:
				self.droite = self.droite.RR()
				return self.LR(),ajout

		return self,ajout

	def LR(self):
		new = self.droite
		ndg = self.droite.gauche
		self.droite.gauche = self
		self.droite = ndg

		self.hauteur = 1 + max(node.get_hauteur(self.gauche),node.get_hauteur(self.droite))
		new.hauteur = 1 + max(node.get_hauteur(new.gauche),node.get_hauteur(new.droite))
		return new

	def RR(self):
		new = self.gauche
		ngd = self.gauche.droite
		self.gauche.droite = self
		self.gauche = ngd

		self.hauteur = 1 + max(node.get_hauteur(self.gauche),node.get_hauteur(self.droite))
		new.hauteur = 1 + max(node.get_hauteur(new.gauche),node.get_hauteur(new.droite))

		return new

	def valeur_equilibre(self):
		if not self:
			return 0
		return node.get_hauteur(self.gauche) - node.get_hauteur(self.droite)

	def has_node(self,e):
		if e == self.val:
			return True
		elif e < self.val and self.gauche:
			return self.gauche.has_node(e)
		elif e > self.val and self.droite:
			return self.droite.has_node(e)
		return False

class abr:
	def __init__(self):
		self.root = None
		self.size = 0

	def initVal(val) :
		t = abr()
		t.root = node(val)
		return t

	def ArbreVide():
		a = abr()
		a.root = None
		a.size = 0
		return a

	# def Arbre_Binaire(e, G, D):
	# 	a = abr()
	# 	a.root.val = e
	# 	a.root.gauche = G
	# 	a.root.droite = D
	# 	return a

	def Est_Arbre_Vide(self) :
		return self.root == None

	def Racine(self):
		return self.root.val

	def Sous_Arbre_Gauche(self):
		return self.root.gauche

	def Sous_Arbre_Droite(self):
		return self.root.droite

	def Ajout(self,e) :
		if self.Est_Arbre_Vide() :
			self.root = node(e)
			ajout = True
		else:
			self.root,ajout = self.root.AjoutNode(e)
		if ajout:
			self.size += 1
		# print(self.root)

	def has(self,e):
		return self.root.has_node(e)

def test():
	# a = abr()
	# a.Ajout(3)
	# a.Ajout(2)
	# a.Ajout(1)
	# print(a.root)
	avl = abr()
	elements = [15,5,20,2,10,17,25,1,3,8,12,13]
	for i in elements:
		avl.Ajout(i)
	print(avl.root)
	# a.Ajout(4)
	# a.Ajout(5)
	# a.Ajout(1)
	# a.Ajout(22)
	# a.Ajout(22)

if __name__=="__main__" :
	test()
