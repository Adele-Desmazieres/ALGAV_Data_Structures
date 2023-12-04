import matplotlib.pyplot as plt
import time

from int_representation import *
from tas_min import *

INDICES_JEUX_DONNEES = [1, 2, 3, 4, 5]
NOMBRE_CLEFS = [1000, 5000, 10000, 20000, 50000, 80000, 120000, 200000]
DIRECTORY = "cles_alea/"


def mesure_temps(keys, cons_f) :
    start = time.time()
    cons_f(keys)
    ret = time.time() - start
    return ret


def graphe_temps(temps_tree_cons, temps_tree_ajout, temps_array_cons, temps_array_ajout) : 
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
    temps_tree_cons = [0] * len(NOMBRE_CLEFS)
    temps_tree_ajout = [0] * len(NOMBRE_CLEFS)
    temps_array_cons = [0] * len(NOMBRE_CLEFS)
    temps_array_ajout = [0] * len(NOMBRE_CLEFS)

    print("Processing files...")
    
    for i in range(len(NOMBRE_CLEFS)) :
        keys_number = NOMBRE_CLEFS[i]
        
        for j in range(len(INDICES_JEUX_DONNEES)) :
            jeu_indice = INDICES_JEUX_DONNEES[j]
            
            filename = DIRECTORY + "jeu_" + str(jeu_indice) + "_nb_cles_" + str(keys_number) + ".txt"
            print("\t" + filename)
            keys = process_keys(filename)
            t1 = mesure_temps(keys, tas_min_tree.Construction)
            t2 = mesure_temps(keys, tas_min_tree.AjoutsIteratifsStatic)
            t3 = mesure_temps(keys, tas_min_array.Construction)
            t4 = mesure_temps(keys, tas_min_array.AjoutsIteratifsStatic)
            
            temps_tree_cons[i] += t1
            temps_tree_ajout[i] += t2
            temps_array_cons[i] += t3
            temps_array_ajout[i] += t4

    temps_tree_cons = [x/len(temps_tree_cons) for x in temps_tree_cons]
    temps_tree_ajout = [x/len(temps_tree_ajout) for x in temps_tree_ajout]
    temps_array_cons = [x/len(temps_array_cons) for x in temps_array_cons]
    temps_array_ajout = [x/len(temps_array_ajout) for x in temps_array_ajout]
    
    return (temps_tree_cons, temps_tree_ajout, temps_array_cons, temps_array_ajout)


def main() :
    t1, t2, t3, t4 = process_all_keys()
    graphe_temps(t1, t2, t3, t4)
    print("Done.")


if __name__ == "__main__" :
    main()