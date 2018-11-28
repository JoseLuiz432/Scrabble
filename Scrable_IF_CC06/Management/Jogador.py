class Jogador(object):
    def __init__(self, tipo, gerente, nome):
        self.tipo = tipo # C computador e H humano
        self.__pontuacao = 0
        self.__letras = []
        self.__gerente = gerente
        self.__palavras = []
        self.nome = nome
        self.__maquina = None


    @property
    def pontuacao(self):
        return self.__pontuacao

    @property
    def letras(self):
        return self.__letras

    def aumentar_pontuacao(self, n):
        self.__pontuacao += n

    def retirar_letra(self, letra):
        if letra in self.__letras:
            self.__letras.remove(letra)
            return True
        else:
            return False

    def adicionar_letra(self, n):
        self.__letras += self.__gerente.sorteio(n)

    def ultima_jogada(self):
        return self.__palavras[-1]

    def add_palavra(self, palavra, pontuacao):
        self.__palavras.append((palavra, pontuacao))
        self.aumentar_pontuacao(pontuacao)

    @property
    def jogadas(self):
        return self.__palavras

    def atrelar_ia(self, m):
        self.__maquina = m

    def acionar_ia(self):
        return self.__maquina.montar_letras()
