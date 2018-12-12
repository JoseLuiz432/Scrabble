from copy import copy


class Maquina(object):

    def __init__(self, gerente, jogador, solve):
        self.__jogador = jogador
        self.__gerente = gerente
        self.__solve = solve

    def montar_letras(self):
        minhas_letras = self.__jogador.letras
        palavras_tabuleiro = self.pegar_tabuleiro()
        return self.backtrackingnew(minhas_letras, palavras_tabuleiro)

    def pegar_tabuleiro(self):
        x, y = self.__gerente.pegar_palavras_tabuleiro()
        r = (x, y)
        return r

    def backtracking(self, letras, tabuleiro):
        """

        :param letras:
        :param tabuleiro:
        :return:
        """
        horizontais = tabuleiro[0][0]
        pos_ho = tabuleiro[0][1]
        pos_ve = tabuleiro[1][1]
        verticais = tabuleiro[1][0]
        cont = 0
        if ' ' in letras:
            letras.remove(' ')
            letras.append('a')
        if not(horizontais and verticais):
            l = []
            self.perm(''.join(letras) + ' ', l)
            provisorio = self.__solve.retorno_palavras(''.join(letras))

            b = ''
            for i in l:
                p = i
                if ' ' in i:
                    i = i.split(' ')
                    p = i[0]
                    b = i[1]
                if p in provisorio:
                    s, word, erro = self.__gerente.inserir_tabuleiro(p, 7, 7, 'v')
                    if not s:
                        print(erro)
                        input()
                        continue

                    return True, word, 7, 7, 'v'
                elif b in provisorio:
                    s, word, erro = self.__gerente.inserir_tabuleiro(b, 7, 7, 'v')
                    if not s:
                        print(erro)
                        input()
                        continue

                    return True, word, 7, 7, 'v'

        for hor in horizontais:
            qnt_antes = 0
            qnt_depois = 0
            flag = False
            h = ''
            pos_h = pos_ho[cont]
            cont += 1
            for i in hor:
                if i != 0:
                    h += i
                else:
                    if flag:
                        qnt_depois += 1
                    else:
                        qnt_antes += 1

            prov_antes = copy(letras) + [' ']
            prov_depois = copy(letras) + [" "]
            left = []
            right = []
            self.perm(''.join(prov_antes), left)

            provisorio = self.__solve.retorno_palavras(h + ''.join(letras))

            for l in left:
                l = l.split(' ')
                for r in left:
                    r = r.split(' ')
                    for opcao in range(2):
                        for opcao2 in range(2):
                            p = l[opcao] + h + r[opcao2]
                            if p == h:
                                continue
                            if p in provisorio:
                                inserir = ''
                                for i in l[opcao]:
                                    inserir += i
                                for j in h:
                                    inserir += 'k'
                                for z in r[opcao2]:
                                    inserir += z

                                s, word, erro = self.__gerente.inserir_tabuleiro(inserir, pos_h[0], pos_h[1] - len(l[opcao]), 'h')
                                if not s:
                                    print(erro)
                                    input()
                                    continue

                                return True, word, pos_h[0], pos_h[1] - len(l[opcao]), 'h'
        cont = 0
        for ver in verticais:
            v = ''
            flag = False
            qnt_depois = 0
            qnt_antes = 0
            pos_h = pos_ve[cont]
            cont += 1
            for i in ver:
                if i != 0:
                    v += i
                else:
                    if flag:
                        qnt_depois += 1
                    else:
                        qnt_antes += 1

            prov_antes = copy(letras) + [' ']
            prov_depois = copy(letras) + [" "]
            left = []
            right = []
            self.perm(''.join(prov_antes), left)
            provisorio = self.__solve.retorno_palavras(v+''.join(letras))
            for l in left:
                l = l.split(' ')
                for r in left:
                    r = r.split(' ')
                    for opcao in range(2):
                        for opcao2 in range(2):
                            p = l[opcao] + v + r[opcao2]
                            if p == v:
                                continue

                            if p in provisorio:
                                inserir = ''
                                for i in l[opcao]:
                                    inserir += i
                                for j in v:
                                    inserir += 'k'
                                for z in r[opcao2]:
                                    inserir += z

                                s, word, erro = self.__gerente.inserir_tabuleiro(inserir, pos_h[0] - len(l[opcao]), pos_h[1] , 'v')
                                if not s:
                                    print(erro)
                                    input()
                                    continue

                                return True, word, pos_h[0], pos_h[1] - len(l[opcao]), 'v'

        return False, 0, 0, ''

    def backtrackingnew(self, letras, tabuleiro):
        horizontais = copy(tabuleiro[0][0])
        pos_ho = tabuleiro[0][1]
        pos_ve = tabuleiro[1][1]
        verticais = copy(tabuleiro[1][0])
        cont = 0
        zero = [0]*15

        if not (horizontais and verticais): # primeira jogada
            inicio = self.__solve.retorno_palavras('')
            minhas_letras = copy(letras)
            resposta = self.back(inicio, minhas_letras, '')
            if not (resposta is None or not resposta):
                signal, word, erro = self.__gerente.inserir_tabuleiro(resposta, 7, 7, 'h')
                if signal:
                    return True, word, 7, 7, 'h'
                else:
                    print(erro)

        if pos_ho[0][0] != 0:
            horizontais = [zero] + horizontais
            new_tuple = (pos_ho[0][0] - 1, pos_ho[0][1])
            pos_ho = [new_tuple] + pos_ho

        if pos_ho[-1][0] != 14:
            horizontais += [zero]
            new_tuple = (pos_ho[-1][0] + 1, pos_ho[-1][1])
            pos_ho += [new_tuple]

        if pos_ve[0][1] != 0 :
            verticais = [zero] + verticais
            new_tuple = (pos_ve[0][0], pos_ve[0][1] -1)
            pos_ve = [new_tuple] + pos_ve
        if pos_ve[-1][1] != 14:
            verticais += [zero]
            new_tuple = (pos_ve[-1][0], pos_ve[-1][1] + 1)
            pos_ve += [new_tuple]

        cont = 0
        palavras = []
        for hor in horizontais:
            pos_h = pos_ho[cont]
            cont += 1
            inicio = self.__solve.retorno_palavras('')
            minhas_letras = letras + ['<']

            for i in range(15):
                nova = self.backlinha(inicio, minhas_letras, hor, i, '', False)
                if nova is not None:
                    pos = i
                    pontos = self.__solve.calcular_pontuacao(nova, pos_h[0], pos, 'h')
                    palavras.append(((nova, pos_h[0], pos, 'h'), pontos))

        cont = 0
        for ver in verticais:
            pos_v = pos_ve[cont]
            cont += 1
            inicio = self.__solve.retorno_palavras('')
            minhas_letras = letras + ['<']

            for i in range(15):
                nova = self.backlinha(inicio, minhas_letras, ver, i, '',  False)
                if nova is not None:
                    pos = i
                    pontos = self.__solve.calcular_pontuacao(nova, pos, pos_v[1], 'v')
                    palavras.append(((nova, pos, pos_v[1], 'v'), pontos))

        # colocando na ordem das melhores palavras pela pontuacao
        palavras.sort(key=lambda x: -x[1])
        for palavra in palavras:
            palavra = palavra[0]
            signal, word, erro = self.__gerente.inserir_tabuleiro(palavra[0], palavra[1], palavra[2], palavra[3])
            if signal:
                return True, palavra[0], palavra[1], palavra[2], palavra[3]

        return False, '', 0, 0, ''

    def back(self, dict, letras, new):

        for letra in letras:
            if letra in dict.keys():
                novas_letras = copy(letras)
                novas_letras.remove(letra)

                nova = self.back(dict[letra], novas_letras, new+letra)
                if nova is not None:
                    return nova
        if '<' in dict.keys():
            return new
        else:
            return None

    def backlinha(self, dict, minhas_letras, tabuleiro, pos, new,  flag_le):
        if pos > 14:
            if '<' in dict.keys():
                if flag_le:
                    return new
                else:
                    return None
            else:
                return None

        # verificando se ha algo na posicao
        if tabuleiro[pos] != 0:
            # usando todas as letras da posicao
            if tabuleiro[pos] in dict.keys():
                nova = self.backlinha(dict[tabuleiro[pos]], minhas_letras, tabuleiro, pos+1, new+tabuleiro[pos],  flag_le)
                if nova is None:
                    return None
                else:
                    return nova
            else:
                return None
        else:
            for letra in minhas_letras:
                if letra in dict.keys():
                    if letra == '<':
                        if flag_le:
                            return new
                        else:
                            continue
                    novas_letras = copy(minhas_letras)
                    novas_letras.remove(letra)
                    nova = self.backlinha(dict[letra], novas_letras, tabuleiro, pos+1, new + letra,  True)
                    if nova is not None:
                        return nova

                elif ' ' in minhas_letras:
                    for coringa in dict.keys():
                        if coringa == '<':
                            continue
                        novas_letras = copy(minhas_letras)
                        novas_letras.remove(' ')
                        nova = self.backlinha(dict[coringa], novas_letras, tabuleiro, pos+1, new + coringa,  True)
                        if nova is not None:
                            return nova

        return None

    def perm(self, s, lista, i=0):
        if i == len(s) - 1:
            lista.append(s)
        else:
            for j in range(i, len(s)):
                t = s
                s = s[j] + s[:j] + s[(j + 1):]
                self.perm(s, lista, i + 1)
                s = t
