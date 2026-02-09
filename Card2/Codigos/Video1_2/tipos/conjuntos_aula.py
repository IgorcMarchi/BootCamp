print({1, 2, 3})
print(type({1, 2, 3}))

conj = ({1, 2, 3, 3, 3, 3})
# print(conj[1]) Não suporta
print(conj)  # Só mostra numeros unicos(contagem unica)
print(len(conj))  # Só contabiliza apenas um numero se tiver mais de um
