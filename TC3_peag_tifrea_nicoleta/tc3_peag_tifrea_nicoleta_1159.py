"""
În apropierea Sfintele Sărbători Pascale, o cofetărie produce două tipuri de cozonac și un tip de pască. 
Materiile prime utilizate sînt: aluat pentru cozonac, nucă, stafide, cacao, brînză, fructe confiate.
Cantitățile disponibile din fiecare materie primă sînt, în ordine: 500, 10, 5, 2, 20, 3 kg.
Produsele sînt ambalate în pachete de cîte 1 kg și conțin

 - Cozonac 1: 75% aluat pentru cozonac, 12%nucă, 10% stafide, 3% cacao;

 - Cozonac 2: 75% aluat pentru cozonac, 10% stafide, 10% cacao, 5% fructe confiate;

 - Pască: 50% aluat pentru cozonac, 35% brînză, 10 % fructe confiate, 5% stafide.

Profiturile aduse de fiecare combinație sînt, în ordine: 20, 18, 22 unități pe pachet.
Utilizați un algoritm genetic pentru a determina cantitățile (în număr de bucăți) din fiecare combinație care trebuie produse pentru a maximiza profitul.
"""

#rezolvarea cerintei

import random

# capacitati aluat, nuca, stafide, cacao, branza, fructe confiate (in kg)
capacitati = [500.0, 10.0, 5.0, 2.0, 20.0, 3.0]
profituri = [20.0, 18.0, 22.0]

#functia fitness
def calcul_fitness(individ):
    x1, x2, x3 = individ
    
    # calculam consumul de materii prime in functie de cantitati
    consum_aluat = 0.75 * x1 + 0.75 * x2 + 0.50 * x3
    consum_nuca = 0.12 * x1
    consum_stafide = 0.10 * x1 + 0.10 * x2 + 0.05 * x3
    consum_cacao = 0.03 * x1 + 0.10 * x2
    consum_branza = 0.35 * x3
    consum_fructe = 0.05 * x2 + 0.10 * x3
    
    # verificam stocul, daca depasim restrictiile atunci individul este invalid
    if (consum_aluat > capacitati[0] + 1e-7 or
        consum_nuca > capacitati[1] + 1e-7 or
        consum_stafide > capacitati[2] + 1e-7 or
        consum_cacao > capacitati[3] + 1e-7 or
        consum_branza > capacitati[4] + 1e-7 or
        consum_fructe > capacitati[5] + 1e-7):
        return -1 
        
    # calculam profitul total
    profit = profituri[0] * x1 + profituri[1] * x2 + profituri[2] * x3
    return profit


# algoritmul
def algoritm_genetic():
 
    dimensiune_populatie = 50
    numar_generatii = 50
    rata_mutatie = 0.15
    
    # generam populatia
    populatie = []
    for i in range(dimensiune_populatie):
        x1 = random.randint(0, 83)
        x2 = random.randint(0, 50)
        x3 = random.randint(0, 57)
        populatie.append([x1, x2, x3])
        
    for generatie in range(numar_generatii):
      
        populatie_evaluata = []
        for ind in populatie:
            fit = calcul_fitness(ind)
            if fit != -1:
                populatie_evaluata.append((fit, ind))
                
        # sortam descrescator dupa profit
        populatie_evaluata.sort(key=lambda x: x[0], reverse=True)
        
        # daca nu avem indivizi valizi, generam o populatie noua de indivizi
        if not populatie_evaluata:
            populatie = []
            for i in range(dimensiune_populatie):
                populatie.append([random.randint(0, 83), random.randint(0, 50), random.randint(0, 57)])
            continue
            
        
        noua_populatie = [ind[1] for ind in populatie_evaluata[:5]]
        
        # generam resul populatiei prin incrucusare si crossover
        while len(noua_populatie) < dimensiune_populatie:
            p1 = random.choice(populatie_evaluata[:10])[1]
            p2 = random.choice(populatie_evaluata[:10])[1]
            
         
            punct = random.randint(1, 2)
            copil = p1[:punct] + p2[punct:]
            
            # mutatie scimpla, schimbam o gene aleatoriu
            if random.random() < rata_mutatie:
                gena_mutata = random.randint(0, 2)
                if gena_mutata == 0:
                    copil[0] = random.randint(0, 83)
                elif gena_mutata == 1:
                    copil[1] = random.randint(0, 50)
                else:
                    copil[2] = random.randint(0, 57)
                    
            noua_populatie.append(copil)
            
        populatie = noua_populatie
        
    #selectam cel mai bun individ din ultima generatie
    populatie_evaluata = [(calcul_fitness(ind), ind) for ind in populatie if calcul_fitness(ind) != -1]
    populatie_evaluata.sort(key=lambda x: x[0], reverse=True)
    
    if populatie_evaluata:
        return populatie_evaluata[0]
    else:
        return None, [0, 0, 0]

cel_mai_bun_profit = -1
cel_mai_bun_individ = [0, 0, 0]

for i in range(10):
    rezultat = algoritm_genetic()
    if rezultat[0] is not None and rezultat[0] > cel_mai_bun_profit:
        cel_mai_bun_profit = rezultat[0]
        cel_mai_bun_individ = rezultat[1]

# Afisarea rezultatelor
print("Rezultate Optimizare:")
print(f"Profit maxim: {cel_mai_bun_profit}")
print(f"Cozonac 1 (x1): {cel_mai_bun_individ[0]} bucati")
print(f"Cozonac 2 (x2): {cel_mai_bun_individ[1]} bucati")
print(f"Pasca (x3): {cel_mai_bun_individ[2]} bucati")