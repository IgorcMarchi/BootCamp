# Classe Contador
class Contador:
    contador = 10  # atributo de classe

    # Incrementa o contador no objeto
    def inc_maluco(self):
        self.contador = self.contador + 1
        return self.contador

    # Incrementa o contador da classe
    @classmethod
    def inc(cls):
        cls.contador += 1
        return cls.contador

    # Decrementa o contador da classe
    @classmethod
    def dec(cls):
        cls.contador -= 1
        return cls.contador

    # Método estático que apenas soma 1 a um número
    @staticmethod
    def mais_um(n):
        return n + 1
    

# Usando método estático
print(Contador.mais_um(99))

# Criando objeto da classe
c1 = Contador()

# Usando método de instância
print(c1.inc_maluco())
print(c1.inc_maluco())
print(c1.inc_maluco())
print(c1.inc_maluco())

# Usando métodos de classe
print(Contador.inc())
print(Contador.inc())

# print(Contador.inc())
# print(Contador.dec())
# print(Contador.dec())
# print(Contador.dec())
# print(Contador.mais_um(99))
