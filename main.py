import matplotlib.pyplot as plt
import time

from int_representation import *
from tas_min import *

INDICES_JEUX_DONNEES = [1, 2, 3, 4, 5]
#INDICES_JEUX_DONNEES = [5]
NOMBRE_CLEFS = [1000, 5000, 10000, 20000, 50000, 80000, 120000, 200000]
DIRECTORY = "cles_alea/"


def mesure_temps(keys, cons_f) :
    start = time.time()
    cons_f(keys)
    ret = time.time() - start
    return ret


def moyenne_temps(keys_list, cons_f) :
    m = 0
    for keys in keys_list :
        m = m + mesure_temps(keys, cons_f)
    m = m / len(keys_list)
    return m


# [liste_des_listes_de_1000_clefs, liste_des_listes_de_5000_clefs...]
def graphe_temps(keys_lists_by_size) : 
    print("Measuring construction times...")
    
    temps_tree_cons = []
    temps_tree_ajout = []
    temps_array_cons = []
    temps_array_ajout = []
    
    for keys_list in keys_lists_by_size :
        temps_tree_cons.append(moyenne_temps(keys_list, tas_min_tree.Construction))
        temps_tree_ajout.append(moyenne_temps(keys_list, tas_min_tree.AjoutsIteratifsStatic))
        temps_array_cons.append(moyenne_temps(keys_list, tas_min_array.Construction))
        temps_array_ajout.append(moyenne_temps(keys_list, tas_min_array.AjoutsIteratifsStatic))

    print("Making plots...")
    fig, axs = plt.subplots(1, 2)
    fig.suptitle("Temps de création d'un tas min en fonction de sa taille")
    
    xval = [n/1000 for n in NOMBRE_CLEFS]
    
    axs[0].plot(xval, temps_tree_cons, label="Construction", marker='X')
    axs[0].plot(xval, temps_tree_ajout, label="AjoutsIteratifs", marker='X')
    axs[0].legend()
    axs[0].set(xlabel="taille du tas (en milliers de noeuds)", ylabel="temps de création (en secondes)")
    axs[0].set_title("Tas min par arbre")
    #axs[0].set_xticks(xval, minor=False)
    axs[0].grid()

    axs[1].plot(xval, temps_array_cons, label="Construction", marker='X')
    axs[1].plot(xval, temps_array_ajout, label="AjoutsIteratifs", marker='X')
    axs[1].legend()
    axs[1].set(xlabel="taille du tas (en milliers de noeuds)")
    axs[1].set_title("Tas min par tableau")
    #axs[1].set_xticks(xval, minor=False)
    axs[1].grid()
    
    plt.show()
    plt.close()


def process_keys(filename) :
    f = open(filename, 'r')
    ret = []
    for l in f :
        intvalue = int(l.rstrip(), 16) # 16 car valeurs hexadécimales
        val = uint128(intvalue)
        ret.append(val)
    f.close()
    return ret


def process_all_keys() :
    keys_lists_by_size = [[None for x in range(len(INDICES_JEUX_DONNEES))] for y in range(len(NOMBRE_CLEFS))]
    print("Processing files...")
    #print(len(keys_lists_by_size))
    #print(len(keys_lists_by_size[0]))
    #print(len(keys_lists_by_size[0][0]))
    
    for i in range(len(NOMBRE_CLEFS)) :
        keys_number = NOMBRE_CLEFS[i]
        
        for j in range(len(INDICES_JEUX_DONNEES)) :
            jeu_indice = INDICES_JEUX_DONNEES[j]
            
            filename = DIRECTORY + "jeu_" + str(jeu_indice) + "_nb_cles_" + str(keys_number) + ".txt"
            keys_lists_by_size[i][j] = process_keys(filename)
    
    return keys_lists_by_size


def main() :
    #keys = process_keys("cles_alea/jeu_1_nb_cles_1000.txt")
    #print(keys[0], keys[1], keys[2])
    keys_lists_by_size = process_all_keys()
    graphe_temps(keys_lists_by_size)
    print("Done.")


if __name__ == "__main__" :
    main()