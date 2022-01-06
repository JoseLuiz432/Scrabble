from tkinter import *


class Provisorio(object):
    x = [
        'TP',
        'TL',
        'DP',
        'DL',
        ' *',
        '  ',
    ]

    def __init__(self, gerente):
        self.__gerente = gerente

    def atualizar_tabuleiro(self, tabuleiro):
        verde = '\033[32m'
        branco = '\033[37m'
        print("{:>20} letras sobrando".format(self.__gerente.sacola))
        print("{:>3}".format(""), end='')
        for i in range(15):
            print("{:2X}".format(i), end='   ')
        print('')
        print("  {:_<75}".format(''))
        a = 0
        for i in range(15):
            print("{:2X}".format(i), end='')
            if i <= 14:
                for j in range(15):
                    if tabuleiro[i][j] == 0:
                        print("|", end='')
                        print(self.x[self.__gerente.verificar_coo(i, j)], end=' |')
                    else:
                        print("|", end=' ')
                        print(verde + tabuleiro[i][j], end='')
                        print(branco, end=' |')

            if i == 0:
                print("{:>20}".format("My words:"), end='')

            elif (i >= 1) and (i < 7):
                print("{:>13}".format(""), end=" ")
                for jogada in self.__gerente.jogadas(0)[a:a+5]:
                    print(str(jogada[0] + '(' + str(jogada[1]) + ')'), end=' ')
                a += 5
            elif i == 8:
                a = 0
                print("{:>20}".format("You words:"), end='')
            elif i >= 9:
                print("{:>13}".format(""), end=" ")
                for jogada in self.__gerente.jogadas(1)[a:a+5]:
                    print(str(jogada[0] + '(' +  str(jogada[1]) + ')'), end=' ')
                a += 5
            print('')

        print("  {:_<75}".format(''))
        print("{:>3}".format(""), end='')
        for i in range(15):
            print("{:2X}".format(i), end='   ')
        print('')
        self.atualizar_letras()

    def atualizar_letras(self):
        print(' me:' + str(self.__gerente.pontuacao(0)), end='  ')
        print(' '.join(self.__gerente.letras()), end='  ')
        print(' you:' + str(self.__gerente.pontuacao(1)))

    def printar_jogada(self, x, y):
        print('Placed: ')
        j = self.__gerente.jogada()
        print('  ' + str(j[1]) + " " + str(j[0]))
        print('For a total of ' + str(j[1]) + 'points')
        print("Na posicao: x:%s, y:%s" %(x, y))
