def derivada_primeira_dois_pontos(f, x, h=1e-5):
    """
    Calcula a derivada primeira de f(x) usando a fórmula de dois pontos avançada.

    :param f: Função para a qual calcular a derivada.
    :param x: Ponto no qual calcular a derivada.
    :param h: Tamanho do incremento.
    :return: Valor aproximado da derivada primeira.
    """
    return (f(x + h) - f(x)) / h

def derivada_segunda_tres_pontos_central(f, x, h=1e-5):
    """
    Calcula a derivada segunda de f(x) usando a fórmula de três pontos centrada.

    :param f: Função para a qual calcular a derivada.
    :param x: Ponto no qual calcular a derivada.
    :param h: Tamanho do incremento.
    :return: Valor aproximado da derivada segunda.
    """
    return (f(x + h) - 2 * f(x) + f(x - h)) / (h ** 2)

def derivada_segunda_tres_pontos_nao_central(f, x, h=1e-5):
    """
    Calcula a derivada segunda de f(x) usando a fórmula de três pontos não centrada.

    :param f: Função para a qual calcular a derivada.
    :param x: Ponto no qual calcular a derivada.
    :param h: Tamanho do incremento.
    :return: Valor aproximado da derivada segunda.
    """
    return (f(x + 2 * h) - 2 * f(x + h) + f(x)) / (h ** 2)


# Dados do exemplo
def exemplo_funcao(x):
    return x ** 2 + 3 * x + 1

ponto_avaliacao = 2

# Aplicação das fórmulas
derivada_primeira = derivada_primeira_dois_pontos(exemplo_funcao, ponto_avaliacao)
derivada_segunda_central = derivada_segunda_tres_pontos_central(exemplo_funcao, ponto_avaliacao)
derivada_segunda_nao_central = derivada_segunda_tres_pontos_nao_central(exemplo_funcao, ponto_avaliacao)

# Impressão dos resultados
print("Derivada Primeira:", derivada_primeira)
print("Derivada Segunda (Centrada):", derivada_segunda_central)
print("Derivada Segunda (Não Centrada):", derivada_segunda_nao_central)


# Comparação entre os métodos para derivada segunda
derivada_segunda_central = derivada_segunda_tres_pontos_central(exemplo_funcao, ponto_avaliacao)
derivada_segunda_nao_central = derivada_segunda_tres_pontos_nao_central(exemplo_funcao, ponto_avaliacao)

# Impressão dos resultados
print("Derivada Segunda (Centrada):", derivada_segunda_central)
print("Derivada Segunda (Não Centrada):", derivada_segunda_nao_central)

# Comparação e conclusão
if abs(derivada_segunda_central) < abs(derivada_segunda_nao_central):
    print("A fórmula centrada proporciona uma aproximação mais precisa da derivada segunda.")
else:
    print("A fórmula não centrada pode ser menos precisa para este exemplo específico.")
