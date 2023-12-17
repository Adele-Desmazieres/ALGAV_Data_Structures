import matplotlib.pyplot as plt
import time

from int_representation import *
from tas_min import *
from file_binomiale import * 

INDICES_JEUX_DONNEES = [1, 2]#, 3, 4, 5]
NOMBRE_CLEFS = [1000, 5000, 10000, 20000, 50000, 80000, 120000, 200000]#, 400000, 1000000]
DIRECTORY = "cles_alea/"

def mesure_temps_union(keys1, keys2) :
    ttree1 = tas_min_tree.Construction(keys1)
    ttree2 = tas_min_tree.Construction(keys2)
    
    tarr1 = tas_min_array.AjoutsIteratifsStatic(keys1)
    tarr2 = tas_min_array.AjoutsIteratifsStatic(keys2)
    
    tfile1 = BinomialQueue.Construction(keys1)
    tfile2 = BinomialQueue.Construction(keys2)
    
    start = time.time()
    tas_min_tree.Union(ttree1, ttree2)
    tree_time = time.time() - start

    start = time.time()
    tas_min_array.Union(tarr1, tarr2)
    arr_time = time.time() - start
    
    start = time.time()
    BinomialQueue.UnionFile(tfile1, tfile2)
    file_time = time.time() - start
    
    return tree_time, arr_time, file_time

def mesure_temps(keys, cons_f) :
    start = time.time()
    cons_f(keys)
    ret = time.time() - start
    return ret


def graphe_temps(temps_tree_cons, temps_tree_ajout, temps_array_cons, temps_array_ajout, temps_tree_union, temps_array_union, temps_file_cons, temps_file_union) : 
    print("Making plots...")
    
    # FIRST GRAPH
    fig, axs = plt.subplots(1, 3)
    fig.suptitle("Temps de création d'un tas min en fonction de sa taille")
    
    xval = [n/1000 for n in NOMBRE_CLEFS]
    
    axs[0].plot(xval, temps_tree_cons, label="Construction", marker='X')
    axs[0].plot(xval, temps_tree_ajout, label="AjoutsIteratifs", marker='X')
    axs[0].legend()
    axs[0].set(xlabel="taille du tas (en milliers de noeuds)", ylabel="temps de création (en secondes)")
    axs[0].set_title("Tas min par arbre")
    axs[0].grid()

    axs[1].plot(xval, temps_array_cons, label="Construction", marker='X')
    axs[1].plot(xval, temps_array_ajout, label="AjoutsIteratifs", marker='X')
    axs[1].legend()
    axs[1].set(xlabel="taille du tas (en milliers de noeuds)")
    axs[1].set_title("Tas min par tableau")
    axs[1].grid()

    axs[2].plot(xval, temps_file_cons, label="Construction", marker='X')
    axs[2].legend()
    axs[2].set(xlabel="taille de la file (en milliers de noeuds)")
    axs[2].set_title("File binomiale")
    axs[2].grid()
    
    plt.show()
    #plt.close()
    
    # SECOND GRAPH
    plt.plot(xval, temps_tree_union, label="Union par arbre", marker='X')
    plt.plot(xval, temps_array_union, label="Union par tableau", marker='X')
    plt.plot(xval, temps_file_union, label="Union de files", marker='X')
    plt.legend()
    plt.xlabel("taille du tas résultant (en milliers de noeuds)")
    plt.ylabel("temps (en secondes)")
    plt.title("Union de deux tas min de même tailles")
    plt.grid()

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
    temps_tree_union = [0] * len(NOMBRE_CLEFS)
    temps_array_union = [0] * len(NOMBRE_CLEFS)
    temps_file_cons = [0] * len(NOMBRE_CLEFS)
    temps_file_union = [0] * len(NOMBRE_CLEFS)
    nombre_de_jeux = [0] * len(NOMBRE_CLEFS)

    print("Processing files...")
    
    for i in range(len(NOMBRE_CLEFS)) :
        keys_number = NOMBRE_CLEFS[i]
        
        for j in range(len(INDICES_JEUX_DONNEES)) :
            jeu_indice = INDICES_JEUX_DONNEES[j]
            
            filename = DIRECTORY + "jeu_" + str(jeu_indice) + "_nb_cles_" + str(keys_number) + ".txt"
            
            try:
                keys = process_keys(filename)
                print("\t" + filename)
                
                t1 = mesure_temps(keys, tas_min_tree.Construction)
                t2 = mesure_temps(keys, tas_min_tree.AjoutsIteratifsStatic)
                #t1 = 0
                #t2 = 0
                
                t3 = mesure_temps(keys, tas_min_array.Construction)
                t4 = mesure_temps(keys, tas_min_array.AjoutsIteratifsStatic)
                
                mid = keys_number//2
                t5, t6, t7 = mesure_temps_union(keys[:mid+1], keys[mid+1:])
                #t5, t6 = 0, 0
                
                t8 = mesure_temps(keys, BinomialQueue.Construction)
                
                
                temps_tree_cons[i] += t1
                temps_tree_ajout[i] += t2
                temps_array_cons[i] += t3
                temps_array_ajout[i] += t4
                temps_tree_union[i] += t5
                temps_array_union[i] += t6
                temps_file_union[i] += t7
                temps_file_cons[i] += t8
                
                nombre_de_jeux[i] += 1
            
            except FileNotFoundError:
                pass

    temps_tree_cons = [temps_tree_cons[i]/nombre_de_jeux[i] for i in range(len(temps_tree_cons))]
    temps_tree_ajout = [temps_tree_ajout[i]/nombre_de_jeux[i] for i in range(len(temps_tree_ajout))]
    temps_array_cons = [temps_array_cons[i]/nombre_de_jeux[i] for i in range(len(temps_array_cons))]
    temps_array_ajout = [temps_array_ajout[i]/nombre_de_jeux[i] for i in range(len(temps_array_ajout))]
    temps_tree_union = [temps_tree_union[i]/nombre_de_jeux[i] for i in range(len(temps_tree_union))]
    temps_array_union = [temps_array_union[i]/nombre_de_jeux[i] for i in range(len(temps_array_union))]
    temps_file_cons = [temps_file_cons[i]/nombre_de_jeux[i] for i in range(len(temps_file_cons))]
    temps_file_union = [temps_file_union[i]/nombre_de_jeux[i] for i in range(len(temps_file_union))]
    
    #temps_tree_ajout = [x/len(temps_tree_ajout) for x in temps_tree_ajout]
    #temps_array_cons = [x/len(temps_array_cons) for x in temps_array_cons]
    #temps_array_ajout = [x/len(temps_array_ajout) for x in temps_array_ajout]
    #temps_tree_union = [x/len(temps_tree_union) for x in temps_tree_union]
    #temps_array_union = [x/len(temps_array_union) for x in temps_array_union]
    
    return (temps_tree_cons, temps_tree_ajout, temps_array_cons, temps_array_ajout, \
        temps_tree_union, temps_array_union, temps_file_cons, temps_file_union)


def main() :
    t1, t2, t3, t4, t5, t6, t7, t8 = process_all_keys()
    graphe_temps(t1, t2, t3, t4, t5, t6, t7, t8)
    print("Done.")


if __name__ == "__main__" :
    main()