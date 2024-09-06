import time

def bissecao(f, a, b, tol=1e-6, max_iter=100):
    """
    Método da Bisseção para encontrar a raiz de uma função.

    :param f: Função para a qual se deseja encontrar a raiz.
    :param a: Limite inferior do intervalo.
    :param b: Limite superior do intervalo.
    :param tol: Tolerância para a convergência.
    :param max_iter: Número máximo de iterações.
    :return: Aproximação da raiz da função.
    """
    #Inicialização de Variáveis e Medição do Tempo:
    iter_count = 0
    start_time = time.time()

    while (b - a) / 2 > tol and iter_count < max_iter: #até atingir a tolerância ou o número máximo de iterações.
        #Cálculo do Ponto Médio e Condições de Atualização:
        c = (a + b) / 2
        if f(c) == 0:
            return c
        elif f(a) * f(c) < 0:
            b = c
        else:
            a = c
        iter_count += 1

    #Medimos o tempo final e calculamos o tempo total de execução.
    #Imprimimos o número de iterações e o tempo de execução.
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Método da Bisseção convergiu em {iter_count} iterações em {elapsed_time:.6f} segundos.")
    
    return (a + b) / 2


def derivada_por_definicao(f, x, h=1e-6):
    """
    Calcula a derivada de uma função usando a definição.

    :param f: Função para a qual se deseja calcular a derivada.
    :param x: Ponto no qual calcular a derivada.
    :param h: Pequeno incremento para a definição de derivada.
    :return: Aproximação da derivada no ponto x.
    """
    return (f(x + h) - f(x)) / h

def newton_raphson(f, x0, tol=1e-6, max_iter=100):
    """
    Método de Newton-Raphson para encontrar a raiz de uma função.

    :param f: Função para a qual se deseja encontrar a raiz.
    :param x0: Ponto inicial para a iteração.
    :param tol: Tolerância para a convergência.
    :param max_iter: Número máximo de iterações.
    :return: Aproximação da raiz da função.
    """
    iter_count = 0
    start_time = time.time()
    #Loop Principal - Método de Newton-Raphson:
    while abs(f(x0)) > tol and iter_count < max_iter:
        x0 = x0 - f(x0) / derivada_por_definicao(f, x0)
        iter_count += 1
    #Finalização do Método de Newton-Raphson:
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Método de Newton-Raphson convergiu em {iter_count} iterações em {elapsed_time:.6f} segundos.")

    return x0

# Exemplo de uso
def exemplo_funcao(x):
    return x**2 - 4

def exemplo_derivada(x):
    return 2 * x

# Utilização dos métodos
raiz_bissecao = bissecao(exemplo_funcao, 0, 3) #pontos a = 0 e b =3
raiz_newton = newton_raphson(exemplo_funcao, 1) #ponto inicial = 1

print("Raiz (Bisseção):", raiz_bissecao)
print("Raiz (Newton-Raphson):", raiz_newton)
