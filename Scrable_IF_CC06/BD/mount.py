# -*- coding: utf-8 -*-

from pymongo import MongoClient, ASCENDING
from unicodedata import normalize
from copy import copy
from re import match
import pickle


class Mount(object):
    # instancia as variaveis do host e porta para acesso ao mongo
    def __init__(self, gerente):
        self.__dicionario = '/home/jose/Faculdade/Faculdade_cc_06/PAA_Wallace/Scrable/Scrable_IF_CC06/BD/wordlist-big-latest.txt'
        self.__gerente = gerente
        self.__dict_words = None

    def montar(self):
        count = 0
        arquivo = open(self.__dicionario, 'r', encoding='latin-1')
        linhas = arquivo.readlines()
        aux = {}
        for linha in linhas:
            estado = aux
            if linha == '':
                continue
            linha = self.remover_acentos(linha)
            count += 1

            for letra in linha:
                if letra == '<':
                    if letra not in estado.keys():
                        estado[letra] = 'FINAL'
                    break
                if letra not in estado.keys():
                    estado[letra] = {}
                    estado = estado[letra]
                else:
                    estado = estado[letra]


        arquivo.close()
        arquivo = open('novo.o', 'wb')
        self.__dict_words = Class_dict(aux)
        arquivo.write(pickle.dumps(self.__dict_words))
        arquivo.close()
        return self.__dict_words

    def retornar(self):
        try:
            arquivo = open('novo.o', 'rb')
            return pickle.loads(arquivo.read())
        except:
            return self.montar()

    def remover_acentos(self, txt):
        txt = txt.replace('ç', '9')
        txt = txt.replace('-', '')
        txt = txt.replace('\n', '<')
        txt = normalize('NFKD', txt).encode('ASCII', 'ignore').decode('ASCII')
        txt = txt.replace('9', 'ç')
        return txt.lower()

class Class_dict(object):
    def __init__(self, dicionario):
        self.__dicionario = dicionario

    def busca(self, n, palavra):
        """
        retorna se a palavra existe no dicionario
        :param palavra:
        :return:
        """
        estado = self.__dicionario
        p = copy(palavra) + '<'
        for letra in p:
            if letra in estado.keys():
                estado = estado[letra]
            else:
                return False

        return True

    def busca_maquina(self, n, palavra):
        """
        Retorna para a maquina as transicoes possiveis
        :param n:
        :param palavra:
        :return:
        """
        estado = self.__dicionario
        p = copy(palavra)
        for letra in p:
            if letra in estado.keys():
                estado = estado[letra]
            else:
                return estado

        return estado


class Montador(object):

    def __init__(self, gerente):
        self.__dicionario = '/home/jose/Faculdade/Faculdade_cc_06/PAA_Wallace/Scrable/Scrable_IF_CC06/BD/dicion.txt'
        self.__arvore = None
        self.__gerente = gerente

    def montar(self):
        arquivo = open(self.__dicionario, 'r')

        primeira = arquivo.readline()
        primeira = self.remover_acentos(primeira)
        self.__arvore = No(len(primeira), primeira)

        linhas = arquivo.readlines()
        max = len(linhas)
        cont = 0
        for word in linhas:
            word = self.remover_acentos(word)
            self.__arvore.insere(len(word), word)
            cont += 1
            self.__gerente.mostrar_porcentagem(cont, max)
        arquivo = open('arvore.o', 'wb')
        arquivo.write(pickle.dumps(self.__arvore))
        arquivo.close()
        return self.__arvore

    def retornar(self):
        try:
            arquivo = open('arvore.o', 'rb')
            return pickle.loads(arquivo.read())
        except:
            return self.montar()

    def remover_acentos(self, txt):
        txt = txt.replace('ç', '9')
        txt = txt.replace('\n', '')
        txt =  normalize('NFKD', txt).encode('ASCII', 'ignore').decode('ASCII')
        txt = txt.replace('9', 'ç')
        return txt.lower()


class No:
    def __init__(self, data, palavra):
        self.data = data
        self.palavra = palavra
        self.setaFilhos(None, None)

    def setaFilhos(self, esquerda, direita):
        self.esquerda = esquerda
        self.direita = direita

    def balanco(self):
        prof_esq = 0
        if self.esquerda:
            prof_esq = self.esquerda.profundidade()
        prof_dir = 0
        if self.direita:
            prof_dir = self.direita.profundidade()
        return prof_esq - prof_dir

    def profundidade(self):
        prof_esq = 0
        if self.esquerda:
            prof_esq = self.esquerda.profundidade()
        prof_dir = 0
        if self.direita:
            prof_dir = self.direita.profundidade()
        return 1 + max(prof_esq, prof_dir)

    def rotacaoEsquerda(self):
        self.data, self.direita.data = self.direita.data, self.data
        old_esquerda = self.esquerda
        self.setaFilhos(self.direita, self.direita.direita)
        self.esquerda.setaFilhos(old_esquerda, self.esquerda.esquerda)

    def rotacaoDireita(self):
        self.data, self.esquerda.data = self.esquerda.data, self.data
        old_direita = self.direita
        self.setaFilhos(self.esquerda.esquerda, self.esquerda)
        self.direita.setaFilhos(self.direita.direita, old_direita)

    def rotacaoEsquerdaDireita(self):
        self.esquerda.rotacaoEsquerda()
        self.rotacaoDireita()

    def rotacaoDireitaEsquerda(self):
        self.direita.rotacaoDireita()
        self.rotacaoEsquerda()

    def executaBalanco(self):
        bal = self.balanco()
        if bal > 1:
            if self.esquerda.balanco() > 0:
                self.rotacaoDireita()
            else:
                self.rotacaoEsquerdaDireita()
        elif bal < -1:
            if self.direita.balanco() < 0:
                self.rotacaoEsquerda()
            else:
                self.rotacaoDireitaEsquerda()

    def insere(self, data, palavra):
        if data <= self.data:
            if not self.esquerda:
                self.esquerda = No(data, palavra)
            else:
                self.esquerda.insere(data, palavra)
        else:
            if not self.direita:
                self.direita = No(data, palavra)
            else:
                self.direita.insere(data, palavra)
        self.executaBalanco()

    def busca(self, data, palavra):
        if data < self.data:
            if not self.esquerda:
                return False
            else:
                return self.esquerda.busca(data, palavra)
        elif data > self.data:
            if not self.direita:
                return False
            else:
                return self.direita.busca(data, palavra)
        else: # igual
            lista = []
            self.esquerda.traverse(No.visit, lista, 'pre')

            if palavra in lista:
                return True
            else:
                return False

    def busca_maquina(self, data, palavra):
        if data < self.data:
            if not self.esquerda:
                return []
            else:
                return self.esquerda.busca_maquina(data, palavra)
        elif data > self.data:
            if not self.direita:
                return []
            else:
                return self.direita.busca_maquina(data, palavra)
        else: # igual
            lista = []
            self.esquerda.traverse(No.visit, lista, 'pre')
            return lista

    def traverse(self, visit, lista, order='pre'):
        """Percorre a árvore na ordem fornecida como parâmetro (pre, pos ou in)
           visitando os nós com a função visit() recebida como parâmetro.
        """
        if order == 'pre':
            lista.append(visit(self))
        if self.esquerda is not None:
            self.esquerda.traverse(visit, lista, order)
        if self.direita is not None and order == "pre":
            self.direita.traverse(visit, lista, order)

    def visit(self):
        return self.palavra


if __name__ == '__main__':
    m = Mount()
    m.montar()
