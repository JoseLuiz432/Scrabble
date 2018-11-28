from Scrable_IF_CC06.Management.Gerencia import Gerencia


class main(object):

    @staticmethod
    def main():
        # instanciando
        gerente = Gerencia()

        t = input('Informe o tipo do jogador 1: m-maquina, h-humano')
        jogador1 = gerente.inserir_jogador(t, 0)

        t = input('Informe o tipo do jogador 2: m-maquina, h-humano')
        jogador2 = gerente.inserir_jogador(t, 0)

        gerente.iniciar_jogo()



main.main()