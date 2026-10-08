#importa biblioteca pt calcule matematice avansata vectori si functii trigonometrice
import numpy as np
#importam biblioteca pt a desena graficele 3d la final
import matplotlib.pyplot as grafic


#definim functia obiectiv din enunt

def f(x):
    x1, x2 = x
    y = 2 * np.sin(x1) + x2 - (x1 * x2) ** 3
    return y

def vecini (x,a,b,eps,nr):
    """
    :param x: punctul pentru care calculam vecini
    :param a: limita pentru stanga
    :param b: limita din dreapta
    :param eps: pasul cu care ne deplasam
    :param nr: numarul vecinilor din stanga / dreapta
    :return: lista vecinilor lui x si lista calitatilor acestora
    """

    #initializam doua lista goale una pt coordonatele vecinilor vecinilor si una pentru calitate

    Vx = []
    #lista cu inaltimile tuturor vecinilor actuali
    Cx = []
    x1, x2 = x

    #scriem vecinii pentru ambele axe x1 si x2

    #cu acest for ne deplasam cu un numar de pasi la stanga dreapta sus jos

    for i in range (-nr, nr+1):
        for j in range(-nr, nr+1):
            #calculam noua coordonata pe axa x folosind eps
            x1_nou = x1 + i * eps
            x2_nou = x2 + j * eps

            #verificam daca punctul generat se afla in interiorul domeniului de definitie D

            if(a[0] <= x1_nou <= b[0]) and (a[1] <= x2_nou <=b[1]):

                #daca vecinul este valid salvam si calculam inaltimea folosind functia f
                Vx.append((x1_nou, x2_nou))
                Cx.append(f((x1_nou, x2_nou)))

    return Vx, Cx


def HC(a, b, eps, nr):
    # Generare aleatoare a punctului de start in domeniul [a, b]
    x1_init = np.random.uniform(a[0], b[0])
    x2_init = np.random.uniform(a[1], b[1])
    x = (x1_init, x2_init)

    val_x = f(x)
    gata = False
    max_iter = 1000
    iter_count = 0

    while not gata and iter_count < max_iter:
        Vx, Cx = vecini(x, a, b, eps, nr)

        # Căutăm vecinul cu cea mai bună calitate
        val_max = max(Cx) #gaseste cea mmai mare inaltime din jur
        poz_max = Cx.index(val_max) # afla la ce numar de ordine se afla inaltimea respectiva
        best_vx = Vx[poz_max] # se duce in lista de locatii si o ia pe cea de la numarul de ordine gasit

        if val_x < val_max:
            x = best_vx
            val_x = val_max
        else:
            gata = True

        iter_count += 1

    return x, val_x


def deseneaza(a1, b1, a2, b2, X1, X2, Y, xmax1, xmax2, ymax):
    x1_vals = np.arange(a1, b1, 0.05)
    x2_vals = np.arange(a2, b2, 0.05)
    X1g, X2g = np.meshgrid(x1_vals, x2_vals)
    Zg = 2 * np.sin(X1g) + X2g - (X1g * X2g) ** 3

    fig = grafic.figure(figsize=(10, 7))
    ax = fig.add_subplot(111, projection='3d')

    ax.plot_surface(X1g, X2g, Zg, cmap='viridis', alpha=0.6)
    
 
    ax.scatter(X1, X2, Y,
               color='blue', s=50, zorder=5, label='Puncte finale (reporniri)')
    ax.scatter([xmax1], [xmax2], [ymax],
               color='red', s=200, marker='*', zorder=6, label='Cel mai bun punct')

    ax.set_xlabel('x₁')
    ax.set_ylabel('x₂')
    ax.set_zlabel('f(x₁, x₂)')
    ax.set_title('Hill Climbing – f(x₁,x₂) = 2·sin(x₁) + x₂ − (x₁x₂)³')
    ax.legend()
    grafic.tight_layout()
    grafic.show()


if __name__ == "__main__":
    # Domeniul de definiție x1 in [0, 2] si x2 in [0, 3]
    a = [0.0, 0.0]
    b = [2.0, 3.0]
    eps = 0.01
    nr = 5

    sol, val = HC(a, b, eps, nr)
    print(f"Soluția calculată (x1, x2): ({sol[0]:.4f}, {sol[1]:.4f}) cu valoarea: {val:.4f}")
   
"""
     Este intotdeauna obtinuta solutia optima?

    Raspuns:
    Nu, deoarece algoritmul de tip Hill Climbing este o metoda de cautare locala.
    Acesta se opreste la primul punct de maxim local pe care il gaseste.
    Daca functia are mai multe puncte de maxim, algoritmul va rata punctul de maxim global

"""