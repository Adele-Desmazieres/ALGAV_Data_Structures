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
	
	def AjoutFin(self, val, chemin) :
		if chemin == [0] :
			self.gauche = node(val)
		elif chemin == [1] :
			self.droite = node(val)
		else : 
			if chemin[0] == 0 :
				self.gauche.AjoutFin(val, chemin[1:])
			else :
				self.droite.AjoutFin(val, chemin[1:])
	
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
			print(chemin)
			self.root.AjoutFin(val, chemin)
		else :
			self.root = node(val)
		self.size += 1
	
	def toStr(self) :
		if not self.root :
			return "Empty tree\n"
		else :
			return self.root.toStr()


# TODO : remove this function
def next_pow2(val) :
	# 1 décalé à gauche du nombre de bits nécessaires pour écrire val-1
	return 1 << (val-1).bit_length()

def floor_log2(val) :
	return val.bit_length() - 1

# TODO : remove this function
def bin_list_of_size(val, size) :
	return [int(d) for d in bin(val)[2:]]


def tmp(x) :
	#nbr_bits = floor_log2(x + 1)
	#binary = bin(x)[2:]
	#
	#chemin = [0 if int(i) < nbr_bits else int(binary[i]) for i in range(nbr_bits)]
	chemin = [int(bit) for bit in bin(x+1)[3:]]
	print(chemin)


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
	for i in range(1, 13) :
		t1.AjoutFin(i)
	print(t1.toStr())


if __name__ == "__main__" :
	test()