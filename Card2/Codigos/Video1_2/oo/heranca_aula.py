# Classe base Carro
class Carro:
    def __init__(self):
        # Atributo privado de velocidade
        self.__velocidade = 0

    # Getter da velocidade
    @property
    def Velocidade(self):
        return self.__velocidade

    # Aumenta a velocidade
    def acelerar(self):
        self.__velocidade += 5
        return self.__velocidade

    # Diminui a velocidade
    def frear(self):
        self.__velocidade -= 5
        return self.__velocidade


# Classe Ferrari herda de Carro
class Ferrari(Carro):
    # Sobrescreve o método acelerar
    def acelerar(self):
        super().acelerar()
        return super().acelerar()
    

# Criação do objeto
c1 = Ferrari()

# Testes
print(c1.acelerar())
print(c1.acelerar())
print(c1.acelerar())
print(c1.frear())
print(c1.frear())
print(c1.frear())
