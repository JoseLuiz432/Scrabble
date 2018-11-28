# -*- coding: utf-8 -*-


from Scrable_IF_CC06.Management.Solve import Solve
from Scrable_IF_CC06.Management.Jogador import Jogador
from Scrable_IF_CC06.Interface.Interface import Provisorio
from Scrable_IF_CC06.IA.Maquina import Maquina
from copy import copy
from random import shuffle, randint


class Gerencia(object):

    (
        TP,
        TL,
        DP,
        DL,
        CENTRO,
        VAZIO
    ) = range(6)

    def __init__(self):
        #self.__interface = Interface()

        self.__tabuleiro = []
        self.__tp = []
        self.__dl = []
        self.__vez = 0
        self.__tl = []
        self.__dp = []
        self.__centro = [(7, 7)]
        self.__solve = Solve(self)
        self.__solve.iniciar_dicionario()
        self.__sacoletras = ['a']*14 + ['e']*11 + ['i']*10 + ['o']*10 + ['s']*8 + ['m']*6 + ['u']*7 + \
                            ['r'] * 6 + ['t']*5 + ['l']*5 + ['d']*5 + ['c']*4 + ['p']*4 + ['n']*4 + ['b'] *4 + \
                            ['b']*3 + ['ç'] * 2 + ['f']* 2 + ['g'] * 2 + ['h'] * 2 + ['v'] * 2 + ['j'] * 2 + \
                            ['q'] + ['x'] + ['z'] + [' '] * 3
        shuffle(self.__sacoletras)
        self.__jogador = []
        self.interface = Provisorio(self)
        self.__numerojogadas = 0
        self.__flagprimeirapalavra = False
        self.__maquina = None

    def iniciar_tabuleiro(self):
        for i in range(15):
            self.__tabuleiro.append([])
            for j in range(15):
                self.__tabuleiro[i].append(0)
                if j == 0 or j == 14:
                    if i == 0 or i == 7 or i == 14:
                        self.__tp.append((i, j))
                    elif i == 3 or i == 11:
                        self.__dl.append((i, j))
                elif i == 0 or i == 14:
                    if j == 7:
                        self.__tp.append((i, j))
                    elif j == 3 or j == 11:
                        self.__dl.append((i, j))
                elif (i < 5 or i > 9) and(j < 5 or j > 9):
                    if i == j or (i+j) == 14:
                        self.__dp.append((i, j))
                else:
                    if (j == 1 or j == 13 or j == 5 or j == 9)and(i==5 or i == 9):
                        self.__tl.append((i, j))
                    elif (j in [2, 3, 6, 8, 11, 12]) and (i in [6, 7, 8, 2, 3, 12, 11]):
                        if not ((j in [6,8] and i == 7) or (i == 7 and j in [2, 12])):
                            self.__dl.append((i, j))

    def inserir_tabuleiro(self, word, x, y, d):
        """
        Inserir a palavra no tabuleiro e verificar se causa algum erro
        :param word:
        :param x: posicao em linha
        :param y: posicao em coluna
        :param d: direcao da insercao
        :return: True se a palavra foi inserida com sucesso
        """
        flag_juncao = False
        if x > 15 or y > 15 or x < 0 or y < 0:
            return False, word, "Erro limite"

        if d == 'h':  # horizontal fixa x verifica y
            if not self.__flagprimeirapalavra:
                if x != 7:
                    return False, word, "erro primeira palavra ao centro"
                if y <= 7:
                    if y + len(word) < 7:
                        return False, word, "erro primeira palavra ao centro"
                else:
                    return False, word, "erro primeira palavra ao centro"

            if y + len(word) > 15:
                return False, word, "Erro limite atingido"
            else:
                word_list = []
                for j in word:
                    word_list.append(j)

                c = 1
                palavra = ''.join(word_list)
                while (y - c) >= 0 and self.__tabuleiro[x][y - c] != 0:
                    palavra = self.__tabuleiro[x][y - c] + palavra
                    c += 1

                c = 0
                while (y + len(word_list) + c) <= 14 and self.__tabuleiro[x][y + len(word_list) + c] != 0:
                    palavra += self.__tabuleiro[x][y + len(word_list) + c]
                    c += 1

                if palavra != word:
                    word = palavra
                    flag_juncao = True

                if not self.__solve.verificar_palavra(word):
                    return False, word, "erro palavra invalida"

                for i in range(y, len(word_list)+y):
                    c = 1
                    palavra = word_list[i - y]
                    while (x + c) <= 14 and self.__tabuleiro[x + c][i] != 0:
                        palavra += self.__tabuleiro[x + c][i]
                        c += 1

                    c = 1
                    while (x - c) >= 0 and self.__tabuleiro[x - c][i] != 0:
                        palavra = self.__tabuleiro[x - c][i] + palavra
                        c += 1

                    if len(palavra) > 1:
                        flag_juncao = True
                        if not self.__solve.verificar_palavra(palavra):
                            return False, word, "erro palavra invalida no formador"
                    elif len(palavra) > 1:
                        flag_juncao = True

                # inserindo
                if self.__flagprimeirapalavra and not flag_juncao:
                    return False, word, "insira com as palavras do tabuleiro"
                else:
                    for i in range(y, len(word_list)+y):
                        self.__tabuleiro[x][i] = word_list[i - y]

        elif d == 'v':
            if not self.__flagprimeirapalavra:
                if y != 7:
                    return False, word, "erro primeira palavra ao centro"
                if x <= 7:
                    if x + len(word) < 7:
                        return False, word, "erro primeira palavra ao centro"
                else:
                    return False, word,  "erro primeira palavra ao centro"

            if x + len(word) > 15:
                return False, word, "erro limite do tabuleiro atingido"
            else:
                word_list = []
                for j in word:
                    word_list.append(j)

                # adicionando as letras da mesma linha a palavra para verificacao
                c = 1
                palavra = ''.join(word_list)
                while (x-c) >= 0 and self.__tabuleiro[x-c][y] != 0:
                    palavra = self.__tabuleiro[x-c][y] + palavra
                    c += 1

                c = 0
                while (x + len(word_list) + c) <= 14 and self.__tabuleiro[x + len(word_list) + c][y] != 0:
                    palavra += self.__tabuleiro[x + len(word_list) + c][y]
                    c += 1

                if palavra != word:
                    word = palavra
                    flag_juncao = True

                if not self.__solve.verificar_palavra(word):
                    return False, word, "erro palavra invalida"

                for i in range(x, len(word_list)+x):
                    c = 1

                    palavra = word_list[i - x]
                    while (y + c) <= 14 and self.__tabuleiro[i][y + c] != 0:
                        palavra += self.__tabuleiro[i][y + c]
                        c += 1

                    c = 1
                    while (y - c) >= 0 and self.__tabuleiro[i][y - c] != 0 :
                        palavra = self.__tabuleiro[i][y - c] + palavra
                        c += 1

                    if len(palavra) > 1:
                        flag_juncao = True
                        if not self.__solve.verificar_palavra(palavra):
                            return False, word, "erro palavra invalida no formador"
                    elif len(palavra) > 1:
                        flag_juncao = True


                # inserindo
                if self.__flagprimeirapalavra and not flag_juncao:
                    return False, word, "insira com as palavras do tabuleiro"
                for i in range(x, len(word_list)+x):
                    self.__tabuleiro[i][y] = word_list[i-x]
        else:
            return False, word, ""

        if not self.__flagprimeirapalavra:
            self.__flagprimeirapalavra = True

        return True, word, ""

    def verificar_coo(self, x, y):
        t = (x, y)
        if t in self.__dl:
            return self.DL
        elif t in self.__tl:
            return self.TL
        elif t in self.__dp:
            return self.DP
        elif t in self.__tp:
            return self.TP
        elif t in self.__centro:
            return self.CENTRO
        else:
            return self.VAZIO

    def sorteio(self, n):
        lista = []
        tamanho = len(self.__sacoletras)
        for i in range(n):
            if tamanho == 0:
                break
            lista.append(self.__sacoletras.pop(randint(0, tamanho-1)))
            tamanho -= 1
        shuffle(self.__sacoletras)
        return lista

    @property
    def sacola(self):
        return len(self.__sacoletras)

    def jogadas(self, n):
        return self.__jogador[n].jogadas

    def inserir_jogador(self, tipo, nome):
        j = Jogador(tipo, self, nome)
        self.__jogador.append(j)
        return j

    def jogada(self):
        return self.__jogador[self.__numerojogadas % 2].ultima_jogada()

    def pontuacao(self, j):
        return self.__jogador[j].pontuacao

    def letras(self):
        return self.__jogador[self.__numerojogadas % 2].letras

    def iniciar_jogo(self):
        self.iniciar_tabuleiro()

        # entregando 7 letras para cada
        for j in self.__jogador:
            if j.tipo == 'm':
                j.atrelar_ia(Maquina(self, j, self.__solve))
            j.adicionar_letra(7)

        # iniciando tabuleiro
        self.interface.atualizar_tabuleiro(self.__tabuleiro)
        self.proxima_jogada()

    def proxima_jogada(self):
        while len(self.__sacoletras) != 0:
            player = self.__jogador[self.__numerojogadas % 2]

            # Verificar se o jogador e maquina
            if player.tipo == 'm':
                flag, word, x, y, d = player.acionar_ia()
                if flag:
                    pontuacao = self.__solve.calcular_pontuacao(word, x, y, d)
                    player.add_palavra(word, pontuacao)
                    i = 0
                    for l in word:
                        if player.retirar_letra(l):
                            i += 1
                    player.adicionar_letra(i)
                    self.interface.printar_jogada()

                self.__numerojogadas += 1
                self.interface.atualizar_tabuleiro(self.__tabuleiro)
                continue

            print('Entre com a palavra "YXD <words>" (Y=col, x=row, D=h/v) ou escreva opcoes')
            jogada = input(':')

            if jogada == 'opcoes':
                self.opcoes()
                continue
            dir, word = '', ''
            try:
                dir, word = jogada.split()
            except:
                print('Erro parametros invalidos')
                continue
            lista = []
            for l in dir:
                if l not in "hv":
                    lista.append(int(l, 16))
                else:
                    lista.append(l)

            if len(lista) < 3:
                print('Erro parametros invalidos')
                continue

            x = lista[1]
            y = lista[0]
            dir = lista[2]
            if type(x) != int or type(y) != int or (dir != 'h' and dir != 'v'):
                print('Erro parametros invalidos')
                continue
            # verificar letras
            letras_jogador = copy(player.letras)
            if not self.verificar_letras(word, letras_jogador, x, y, dir):
                print('Voce nao tem as letras correspondentes')  # erro
                continue
            # verificar insercao tabuleiro
            signal, word, erro = self.inserir_tabuleiro(word, x, y, dir) # x, y, d
            if signal: # palavra inserida com sucesso calculando pontuacao
                pontuacao = self.__solve.calcular_pontuacao(word, x, y, dir)
                player.add_palavra(word, pontuacao)
                i = 0
                for l in word:
                    if player.retirar_letra(l):
                        i += 1
                player.adicionar_letra(i)

            else:
                print(erro)
                continue

            self.interface.printar_jogada()
            self.__numerojogadas += 1
            self.interface.atualizar_tabuleiro(self.__tabuleiro)
            continue
        else:
            self.final_de_jogo()

    def final_de_jogo(self):
        if self.__jogador[0].pontuacao > self.__jogador[1].pontuacao:
            print('Jogador 1 venceu')
        else:
            print('jogador 2 venceu')

    def opcoes(self):
        print("1- Passar a vez")
        print("2- Trocar de letras")
        print("3- Ver regras")
        print("4- Voltar")
        escolha = input(":")
        if escolha == '1':
            self.passarvez()
        elif escolha == '2':
            self.trocarletras()
        elif escolha == '3':
            pass
        else:
            self.interface.atualizar_tabuleiro(self.__tabuleiro)

    def passarvez(self):
        self.__numerojogadas += 1
        self.interface.atualizar_tabuleiro(self.__tabuleiro)

    def trocarletras(self):
        print('informe as letras em sequencia que voce deseja trocar. ex: "abc"')
        letras = self.__jogador[self.__numerojogadas % 2].letras
        print('Suas letras sao: ' + str(letras))
        escolha = input(":")

        for letra in escolha:
            if letra not in letras:
                print('informe letras validas')
                self.trocarletras()
                return

        for letra in escolha:
            self.__jogador[self.__numerojogadas % 2].retirar_letra(letra)
            self.__sacoletras.append(letra)

        self.__jogador[self.__numerojogadas % 2].adicionar_letra(len(escolha))
        self.interface.atualizar_tabuleiro(self.__tabuleiro)

    def pegar_palavras_tabuleiro(self):
        verticais = []
        horizontais = []

        pos_h = []
        for i in range(15):
            for j in range(15):
                if self.__tabuleiro[i][j] != 0:
                    pos_h.append((i, j))
                    horizontais.append(self.__tabuleiro[i])
                    break

        pos_v = []
        for j in range(15):
            for i in range(15):
                if self.__tabuleiro[i][j] != 0:
                    x = []
                    pos_v.append((i, j))
                    for c in range(15):
                        x.append(self.__tabuleiro[c][j])
                    verticais.append(x)
                    break

        return (horizontais, pos_h), (verticais, pos_v)

    def verificar_letras(self, word, letras, x, y, d):
        flag = False
        if d == 'h': # fixa x
            for c, letra in enumerate(word):
                if self.__tabuleiro[x][y + c] == letra:
                    continue
                elif self.__tabuleiro[x][y + c] != 0:
                    return False
                elif letra in letras:
                    flag = True
                    letras.remove(letra)
                elif ' ' in letras:
                    flag = True
                    letras.remove(' ')
                else:
                    return False
        elif d == 'v':
            for c, letra in enumerate(word):
                if self.__tabuleiro[x+c][y] == letra:
                    continue
                elif self.__tabuleiro[x+c][y] != 0:
                    return False
                elif letra in letras:
                    flag = True
                    letras.remove(letra)
                elif ' ' in letras:
                    flag = True
                    letras.remove(' ')
                else:
                    return False

        return flag
