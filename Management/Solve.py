from BD.mount import Mount


class Solve(object):
    pontuacao_palavra = {
        0: 3, #tp
        2: 2, #dp
        4: 2, #centro
    }
    pontuacao_letra = {
        3: 2,  # dl
        1: 3,  # tl
        5: 1,  # nada
        0: 1,
        2: 1,
        4: 1,
    }

    def __init__(self, gerente):
        self.__dados = Mount(self)
        self.__arvore = None
        self.__gerente = gerente
        self.__usadas = []

    def verificar_palavra(self, word):
        """
        Verifica a existencia da palavra
        :param word: palavra a ser verificada
        :return: boolean sendo true para aceitacao da palavra e false para recusa
        """
        return self.__arvore.busca(len(word), word)

    def calcular_pontuacao(self, word, x, y, d):
        """
        :param word: palavra a ser verificada
        :return: int com a pontuacao
        """
        soma = 0
        mult = 1
        for c, letra in enumerate(word):
            if d == "h":
                coo = (x, y+c)
                p = self.__gerente.verificar_coo(x, y+c)

                if p in self.pontuacao_palavra and mult == 1 and coo not in self.__usadas:
                    mult = self.pontuacao_palavra[p]
                if p in self.pontuacao_letra.keys() and coo not in self.__usadas:
                    self.__usadas.append(coo)
                    soma += Enum.pontuacao(letra) * self.pontuacao_letra[p]
                else:
                    soma += Enum.pontuacao(letra)
            elif d == 'v':
                p = self.__gerente.verificar_coo(x + c, y)
                coo = (x+c, y)
                if p in self.pontuacao_palavra and mult == 1 and coo not in self.__usadas:
                    mult = self.pontuacao_palavra[p]
                if p in self.pontuacao_letra.keys() and coo not in self.__usadas:
                    self.__usadas.append(coo)
                    soma += Enum.pontuacao(letra) * self.pontuacao_letra[p]
                else:
                    soma += Enum.pontuacao(letra)
        return soma * mult

    def iniciar_dicionario(self):
        self.__arvore = self.__dados.retornar()

    def retorno_palavras(self, word):

        return self.__arvore.busca_maquina(len(word), word)

    def mostrar_porcentagem(self, x, y):
        porcentagem = 100*x/y
        print(porcentagem)


class Enum(object):
    @staticmethod
    def pontuacao(letra):
        if letra in 'aeiosumrt':
            return 1
        elif letra in 'dlcp':
            return 2
        elif letra in 'nbç':
            return 3
        elif letra in 'fghv':
            return 4
        elif letra == 'j':
            return 5
        elif letra == 'q':
            return 6
        else:
            return 7
