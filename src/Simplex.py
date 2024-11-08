import numpy as np
import sys
import time

def read_file(file):
    with open(file, 'r') as f:
        n, m = map(int, f.readline().split())
        c = np.array([int(num) for num in f.readline().split()])
        A = []
        b = []
        for i in range(m):
            A.append([int(num) for num in f.readline().split()])
            b.append(A[i].pop())
    return n, m, c, np.array(A), np.array(b)

def set_tableau(A, B, C):
    #m, n = A.shape
    tableau = np.hstack([A, B.reshape(-1, 1)])              # Junta A com B
    tableau = np.vstack([np.hstack([C, [0]]), tableau])     # Junta C 
    #print(tableau)
    return tableau                                         

def pivotagem(tableau, row, col):
    pivot_element = tableau[row][col]
    for j in range(len(tableau[row])):
        tableau[row][j] /= pivot_element
        
    for i in range(len(tableau)):
        if i != row:
            factor = tableau[i][col]
            for j in range(len(tableau[i])):
                tableau[i][j] -= factor * tableau[row][j]
    
    #print(tableau)
    return tableau

def simplex(n, m, C, A, B):
    tableau = set_tableau(A, B, C)
    iteracao=0
    tempo_inicio = time.time()
    
    while True:
        iteracao += 1
        tempo_atual = time.time()
        tempo_passado = tempo_atual - tempo_inicio
        
    
        col = np.argmin(tableau[0, :-1])  
        if tableau[0, col] >= 0:
            # solução é ótima
            break

        ratios = [] # razões
        for i in range(1, len(tableau)):
            if tableau[i][col] > 0:
                ratio = tableau[i][-1] / tableau[i][col]
            else:
                ratio = float('inf')  # tableau[i][col] <= 0
            ratios.append(ratio)

        min_ratio = float('inf')
        row = -1
        for i in range(len(ratios)): 
            if ratios[i] < min_ratio: # Ir separando a menor ratio.
                min_ratio = ratios[i]
                row = i + 1           # Atualiza a linha que está a menor razão.
        
        tableau = pivotagem(tableau, row, col)
        
        print(f"\nIteração: {iteracao}")
        print(f"Tempo(s): {tempo_passado:.4f}")
        print(f"Objetivo: {-tableau[0, -1]:.4f}")
    
    tempo_final = time.time()
    tempo_final_toltal = tempo_final - tempo_inicio
    
    print(f"\nSolução ótima encontrada em {tempo_final_toltal:.4f} segundos!")
    print(f"Função objetivo é {-tableau[0, -1]:.4f}.")

    variaveis = np.zeros(n)
    for j in range(n):
        col = tableau[1:, j]                                    # Pega a coluna j, exceto a primeira linha
        if np.count_nonzero(col) == 1 and np.sum(col) == 1:
            row_idx = np.where(col == 1)[0][0] + 1              # Acha a linha onde está o 1
            variaveis[j] = tableau[row_idx, -1]                 # Pega o valor do lado direito do tableau

    print("\nSolução:")
    for i in range(n):
        print(f"x[{i+1}] = {variaveis[i]:.4f}")

if __name__ == "__main__":
    filename = sys.argv[1]
    n, m, C, A, B = read_file(filename) 
    simplex(n, m, C, A, B)



'''
Função set tableau, apenas monta o tableau para a resolução:
A montagem é feita da seguinte forma:
Junçaõ da matriz A de coeficientes, o vetor B, e o vetor C de coeficientes da função objetivo.

[[-180 -300    0    0    0    0]
 [   1    0    1    0    0   60]
 [   0    1    0    1    0   50]
 [   1    1    0    0    1  120]]

-> Resultado da função set_tableau(A,B,C)
--EXECUÇÃO DO TABLEAU--
1- O processo da tableau se começa selecionando o menor numero na linha 0 do tableau (linha de custo).
Sendo essa a variável de entrada (coluna). (Linha 48).
s
2- Depois temos que determinar a variável de saída (linha). Começa calculando as razões:
percorre as linhas do tableau, exceto a linha da função objetivo (linha 0). Para cada linha, verifica se o coeficiente da coluna pivô é positivo. 
Se for, calcula a razão entre o valor do lado direito (tableau[i][-1]) e o coeficiente da coluna pivô (tableau[i][col]). (linhas 54 a 59).

3- A variável row que vai receber qual a linha de saída, vai sendo calculada percorrendo o vetor de razões, selecionando no final a linha com a menor razão.

4- Pivotagem: Atualiza o tableau. No caso, ele começa dividindo todos os elementos da linha pivô pelo elemento pivô (linhas 24 a 26).
Depois vai subtraindo o restante das linhas para zerar a coluna do pivô; Retornando o tableau atualizado.

Esses passos são executados até encontrarmos a solução ótima.
'''
