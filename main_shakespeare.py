import matplotlib.pyplot as plt
import time
import random as rd
from os import listdir
from os.path import isfile, join

from tas_min import *
from file_binomiale import *
from arbre_binaire_de_recherche import *
from md5 import *

DIRNAME = "Shakespeare"


def graph_ajout(keys):
	ajouts_tas = []
	ajouts_file = []
	
	keys_shuffled = keys.copy()
	rd.shuffle(keys_shuffled)
	
	tas = tas_min_array()
	file = BinomialQueue()
	
	for k in keys_shuffled:
		start = time.time()
		tas.Ajout(keys)
		ajouts_tas = time.time() - start
		
		start = time.time()
		file.Ajout(keys)
		ajouts_file = time.time() - start
		
	plt.plot(xval, ajouts_tas, label="Ajouts itératifs par tas min tableau", marker='X')
	plt.plot(xval, ajouts_file, label="Ajouts itératifs par file binomiale", marker='X')
	plt.legend()
	plt.xlabel("nombre de nœuds (en milliers)")
	plt.ylabel("temps (en secondes)")
	plt.title("Ajouts itératifs des clefs des mots du recueil de Shakespeare")
	plt.grid()
	plt.show()


def files_parsing(filesname):
	words = []
	collide = dict()
	hachs = abr()
	
	for filename in filesname:
		f = open(filename)
		for line in f:
			word = line.rstrip() # there is one word per line
			hach = md5(word)
			if word not in words:
				words.append(word)
				if hach in collide.keys():
					collide[hach].append(word)
				else:
					collide[hach] = [word]
			else:
				hachs.Ajout(hach)
		
		f.close()
	
	collide = {k:v for k,v in collide.items() if len(v) > 1}
	return words, collide, hachs


def main():
	files = [join(DIRNAME, f) for f in listdir(DIRNAME) if isfile(join(DIRNAME, f))]
	
	print(files, "\n")
	words, collide, hachs = files_parsing(files)
	
	print(len(words), words[1:10], words[1000:1010])
	print("Mots en collision pour MD5 :", collide)
	print("Nombre de clefs :", hachs.size)
	
	graph_ajout(hachs)


if __name__ == "__main__":
	main()