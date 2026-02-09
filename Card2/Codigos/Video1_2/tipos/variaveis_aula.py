a = 3
b = 4.4
print(a + b)

texto = 'Sua idade e...'
idade = 23

# print(texto + str(idade))

# Quando utilizado o "f" e o as "{}" você pode posicionar onde você quer as variaveis
print(f'{texto} {idade}')


saudacao = ' Bom dia '
# Quando utilizado o simbulo de multiplicação ele faz ação x vezes
print(3 * saudacao)

PI = 3.14
# nome da variavel - tipo da variavel - texto do terminal
raio = float(input('Informe o raio da circunferencia?'))
area = PI * raio * raio
print(f'A area da circunferencia e {area} m2')
