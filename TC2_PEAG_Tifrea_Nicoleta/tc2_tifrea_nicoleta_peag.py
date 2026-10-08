import numpy as np

# Functia de fitness: numara perechile (i, j) cu i < j și p[i] < p[j]
def fitness(p):# aflam lungimea permutarii
    n = p.size 
    # numara cate perechi sunt in oridne crescatoare
    calitate = len([(i, j) for i in range(n - 1) for j in range(i + 1, n) if p[i] < p[j]]) #parcurge toate perechile de elemente si numara de cate ori un element din stanga este mai mare decat un element din dreapta
    return calitate

# Generarea populatiei initiale
def generare_initiala(dimensiune, n):
    # se genereaza o matrice initiala unde fiecare rand apartine unui individ, ultima coloana este rezervata pt fitness
    populatie_initiala = np.zeros((dimensiune, n + 1), dtype=   "int")
    for i in range(dimensiune):
        #generam o permutare aleatoare pentru fiecare individ
        populatie_initiala[i, :-1] = np.random.permutation(n)
        populatie_initiala[i, -1] = fitness(populatie_initiala[i, :-1])
    return populatie_initiala

# Mutatie prin interschimbare a doua elemente
def mutatie_interschimbare(cromozom):
    cromozom_mutat = cromozom.copy()
    n = cromozom_mutat.size
    pozitii = np.random.choice(n, 2, replace=False)
    # Interschimbam valorile de pe cele doua pozitii alese
    cromozom_mutat[pozitii[0]], cromozom_mutat[pozitii[1]] = cromozom_mutat[pozitii[1]], cromozom_mutat[pozitii[0]]
    return cromozom_mutat

# Aplicarea mutatiei pe populatia de copii
def mutatie_populatie(copii, pm):
    copii_mutatie = copii.copy()
    dimensiune = copii.shape[0]
    n = copii.shape[1] - 1
    for i in range(dimensiune):
        raspuns = np.random.uniform(0, 1)
        if raspuns <= pm:
            print(f"\nA fost selectat pentru mutatie {copii_mutatie[i, :-1]} cu valoarea {copii_mutatie[i, -1]}")
            copii_mutatie[i, :-1] = mutatie_interschimbare(copii_mutatie[i, :-1])
            copii_mutatie[i, n] = fitness(copii_mutatie[i, :-1])
            print(f"Dupa mutatie cromozomul devine {copii_mutatie[i, :-1]} cu noua valoare {copii_mutatie[i, -1]}")
    return copii_mutatie

# incrucisare simpla in un punct
def incrucisare(p1, p2):
    n = p1.size
    # primul copil primeste incrucisarea de la tata si capatul de la mama al doila primeste in mod invers
    punct = np.random.randint(1, n)
    copil1 = np.concatenate((p1[:punct], p2[punct:]))
    copil2 = np.concatenate((p2[:punct], p1[punct:]))
    return copil1, copil2


def algoritm_genetic(dimensiune_populatie, n, nr_generatii, pm):
    populatie = generare_initiala(dimensiune_populatie, n)
    print("Populatia initiala:")
    print(populatie)
    
    for gen in range(nr_generatii):
        print(f"\n--- Generatia {gen + 1} ---")
        
        #selectam parintii
        populatie = populatie[populatie[:, -1].argsort()[::-1]]
        
         # ii alegem pe cei mai buni 2 indivizi pentru a fi parinti
        parinte1 = populatie[0, :-1]
        parinte2 = populatie[1, :-1]
        
        #generam descendenti
        copil1, copil2 = incrucisare(parinte1, parinte2)
        
        
        copii = np.zeros((2, n + 1), dtype="int")
        copii[0, :-1] = copil1
        copii[0, -1] = fitness(copil1)
        copii[1, :-1] = copil2
        copii[1, -1] = fitness(copil2)
        
     
        copii_mutati = mutatie_populatie(copii, pm)
        
  
        populatie = np.vstack((populatie, copii_mutati))
        populatie = populatie[populatie[:, -1].argsort()[::-1]]
        populatie = populatie[:dimensiune_populatie, :]
        
        print(f"Cea mai buna solutie curenta: {populatie[0, :-1]} cu fitness {populatie[0, -1]}")

    return populatie[0, :-1], populatie[0, -1]

if __name__ == "__main__":
    np.random.seed(42)
    dimensiune = 6
    n_dim = 5
    generatii = 3
    probabilitate_mutatie = 0.2
    
    cel_mai_bun, valoare_optima = algoritm_genetic(dimensiune, n_dim, generatii, probabilitate_mutatie)
    
    print("\nRezultat final:")
    print("Cea mai buna solutie:", cel_mai_bun)
    print("Fitness optim:", valoare_optima)

