import int_representation

class tas_min_interface :
	
	def SupprMin(self) :
		pass
	
	def Ajout(self) :
		pass


class tas_min_tree(tas_min_interface) :
	
	def __init__(self) :
		self.elt = None
		self.gauche = None
		self.droite = None
	
	def new_tas_min_val(val) :
		t = tas_min_tree()
		t.elt = val
		return t
	
	def AjoutFin(self, val) :
		if not self.elt :
			self.elt = val
			return True
		else :
			if not self.gauche : 
				self.gauche = tas_min_tree.new_tas_min_val(val)
				return True
			elif not self.droite :
				self.droite = tas_min_tree.new_tas_min_val(val)
				return True
			else : 
				inserted_gauche = self.gauche.AjoutFin(val)
				if not inserted_gauche :
					self.droite.AjoutFin(val)
				return False
	
	def Ajouttest(self, val) :
		if not self :
			return tas_min_tree.new_tas_min_val(val)
		elif not self.elt :
			self.elt = val
		else :
			if not self.gauche : 
				self.gauche = tas_min_tree.Ajouttest(self.gauche,val)
			elif not self.droite :
				self.droite = tas_min_tree.Ajouttest(self.droite,val)
	
	def AfficherAux(self) :
		if not self or not self.elt :
			print("Empty" , end="" , sep="")
		else :
			print("( ", end="" , sep="")
			tas_min_tree.AfficherAux(self.gauche)
			print(" , " , self.elt , " , " , end="", sep="")
			tas_min_tree.AfficherAux(self.droite)
			print(" )" , end="" , sep="")
		
	def Afficher(self) :
		self.AfficherAux()
		print()
	
	def SupprMin(self) -> tas_min_interface :
		pass




tas1 = tas_min_tree()
print(tas1.elt)
tval = tas_min_tree.new_tas_min_val(3)
print(tval.elt)

tval.Ajouttest(8)
tval.Ajouttest(9)
tval.Afficher()

tree = tas_min_tree()
tree.AjoutFin(1)
tree.AjoutFin(2)
tree.AjoutFin(3)
tree.AjoutFin(4)
tree.Afficher()
class tas_min_array(tas_min_interface) :
	
	def __init__(self) :
		pass
		

