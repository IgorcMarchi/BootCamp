b1 = True
b2 = False
b3 = True

print(b1 and b2 and b3)  # Para ser True todos tem que ser True
print(b1 or b2 or b3)  # Precisa que apenas um seja True para ser True
print(b1 != b2)  # xor ^ para ser True os dois tem que ser diferente
print(not b1)  # inverte o valor
print(not b2)

print(b1 and not b2 and b3)

x = 3
y = 4

print(b1 and not b2 and x < y)  # Para ser True todos tem que ser verdadeiro
