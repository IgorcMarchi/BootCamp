# Função de soma
def soma(a, b):
    return a + b

print(soma(3, 4))

# Função de subtração
def sub(a, b):
    return a - b

# Atribuindo a função a uma variável
subr = sub
print(subr(4, 3))

# Outra variável apontando para a função soma
somar = soma
print(somar(3, 4))


# Função que recebe outra função como parâmetro
def operacao_aritmetica(fn, op1, op2):
    return fn(op1, op2)

# Usando soma como parâmetro
resultado = operacao_aritmetica(soma, 13, 48)
print(resultado)

# Usando subtração como parâmetro
resultado = operacao_aritmetica(sub, 13, 48)
print(resultado)


# Função que retorna outra função (closure)
def soma_parcial(a):
    # Simula processamento pesado
    def concluir_soma(b):
        return a + b
    return concluir_soma

# Criando funções especializadas
soma_1 = soma_parcial(1)

# Executando as funções retornadas
r1 = soma_1(2)
r2 = soma_1(3)
r3 = soma_1(4)

# Executando a função de forma direta
resultado_final = soma_parcial(10)(12)

print(resultado_final, r1, r2, r3)
