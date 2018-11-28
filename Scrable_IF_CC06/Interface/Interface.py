from tkinter import *


class Application:
    def __init__(self, master=None):
        self.pai = Frame(master)

        self.pai.pack()
        background_image = PhotoImage(file='./Imagens/background.png')



        self.container_superior = Frame(master)
        self.container_superior.pack(side=TOP, fill='x')

        self.container_direita = Frame(master)
        self.container_direita.pack(side=RIGHT)
        photo = PhotoImage(file="./Imagens/Novo_jogo.png")
        self.novo_jogo = Button(self.container_direita, image=photo, relief='flat')
        self.novo_jogo.imagem = photo
        self.novo_jogo.bind("<Button-1>", self.iniciar_jogo)
        photo = PhotoImage(file="./Imagens/ranking.png")
        self.ranking = Button(self.container_direita, image=photo, relief='flat')
        self.ranking.imagem = photo
        self.ranking.bind("<Button-1>", self.rank)
        photo = PhotoImage(file="./Imagens/Instrucoes.png")
        self.instrucoes = Button(self.container_direita, image=photo, relief='flat')
        self.instrucoes.imagem = photo
        self.instrucoes.bind("<Button-1>", self.instruc)

        self.novo_jogo.pack()
        self.ranking.pack()
        self.instrucoes.pack()

        #self.msg = Label(self.pai, text="Jogo Iniciado", font=("Calibri", "9", "italic"))

        self.container_esquerda = Frame(self.pai)
        self.container_esquerda.pack(side=LEFT)
        self.imagem_scrabble = Text()

    def iniciar_jogo(self, event):
        if event == "<Button-1>":
            self.msg.pack()

    def instruc(self, event):
        pass

    def rank(self, event):
        pass


class Interface(object):
    def __init__(self):
        root = Tk()
        root.title("Scrabble")
        root.geometry('800x800+100+100')
        app = Application(root)
        root.mainloop()


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

    def printar_jogada(self):
        print('Placed: ')
        j = self.__gerente.jogada()
        print('  ' + str(j[1]) + " " + str(j[0]))
        print('For a total of ' + str(j[1]) + 'points')

