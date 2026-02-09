# Classe Produto
class Produto:
    def __init__(self, nome, preco=1.99, desc=0):
        self.nome = nome           # nome do produto
        self.__preco = preco      # preço (atributo privado)
        self.desc = desc          # desconto

    # Getter do preço
    @property
    def preco(self):
        return self.__preco

    # Getter alternativo
    @preco.getter
    def get_preco(self):
        return self.__preco

    # Setter do preço
    @preco.setter
    def preco(self, novo_preco):
        if novo_preco > 0:
            self.__preco = novo_preco

    # Calcula o preço final com desconto
    def preco_final(self):
        return (1 - self.desc) * self.preco


# Criação dos objetos
p1 = Produto('Caneta', 10, 0.1)
p2 = Produto('Caderno', 14, 0.5)

# Alterando preços usando setter
p1.preco = 70.89
p2.preco = 17.99

# Exibindo os dados
print(p1.nome, p1.preco, p1.desc, p1.preco_final())
print(p2.nome, p2.preco, p2.desc, p2.preco_final())
