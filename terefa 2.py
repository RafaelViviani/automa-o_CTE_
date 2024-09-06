def interpolacao_lagrange(valores_x, valores_y, x):
    """
    Calcula o valor interpolado P(x) usando o Método de Lagrange.

    :param valores_x: Lista dos valores x conhecidos.
    :param valores_y: Lista dos valores y conhecidos correspondentes a valores_x.
    :param x: Valor para o qual deseja-se interpolar.
    :return: Valor interpolado P(x).
    """
    resultado = 0

    # Loop sobre cada ponto conhecido (xi, yi)
    for i in range(len(valores_x)):
        termo = valores_y[i]

        # Cálculo do termo de Lagrange associado a cada ponto
        for j in range(len(valores_x)):
            if j != i:
                termo *= (x - valores_x[j]) / (valores_x[i] - valores_x[j])

        # Adição do termo ao resultado final
        resultado += termo

    return resultado

# Dados do exemplo
#considerando os pontos (1,2), (3,5) e (4,7) e x=2
x=2
valores_x = [1, 3, 4]
valores_y = [2, 5, 7]
x_interp = 2

# Aplicação do Método de Lagrange
resultado_interp = interpolacao_lagrange(valores_x, valores_y, x_interp)
print("Valor interpolado para x =", x_interp, ":", resultado_interp)
