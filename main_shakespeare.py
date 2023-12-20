import matplotlib.pyplot as plt
import time
from os import listdir
from os.path import isfile, join

from int_representation import *
from tas_min import *
from file_binomiale import * 
from arbre_binaire_de_recherche import *
from md5 import *

DIRNAME = "Shakespeare"

def get_files_from_dir(dirname):
	pass

def files_parsing(filesname):
	words = []
	hachs = abr()
	for filename in filesname:
		f = open(filename)
		for line in f:
			word = line.rstrip() # there is one word per line
			if word not in words:
				hach = md5(word)
				hachs.add(hach)
				words.append(word)
		
		f.close()
	return words


def main():
	files = [join(DIRNAME, f) for f in listdir(DIRNAME) if isfile(join(DIRNAME, f))]
	print(files)
	words = files_parsing(files)
	print(len(words), words[1:10], words[1000:1010])


if __name__ == "__main__":
	main()