# -*- coding: utf-8 -*-
import requests
import shutil
from imagesPortal import imagesPortal
import datetime
import time
import os
import sys
import json
from shutil import copyfile


class Verifica(object):
    
    def __init__(self):
        if 'localhost' in sys.argv:
            self.localhost = True
            self.URI = 'http://localhost:5000/'
        else:
            self.localhost = False
            self.URI = 'http://201.16.246.176:5000/'
        self.inicio = time.time()
        self.images = imagesPortal()
        self.cwd = '/var/www/html/images/portais/'
        self.arquivoVerificador = self.cwd + 'verificador.json'
        self.verificaArquivo()
        
        
    def verificaArquivo(self):
        try:
            with open(self.arquivoVerificador,'r') as json_file:
                self.pastas = json.load(json_file)
        except IOError:
            pastas = os.listdir(self.cwd)
            lista_pastas = []
            for pasta in pastas:
                if os.path.isdir(self.cwd + pasta):
                    lista_pastas.append(pasta)
            with open(self.arquivoVerificador,'w') as arq:
                arq.write(json.dumps(lista_pastas))
            self.verificaArquivo()
    
    def listaArquivos(self, pasta):
        if os.path.isdir(pasta):
            lista_arquivos = os.listdir(pasta)
            if len(lista_arquivos):
                lista_retorno = {}
                for arquivo in lista_arquivos:
                    if os.path.isfile(pasta + arquivo):
                        if 'destaque_' in arquivo:
                            a = arquivo.split('_')
                            lista_retorno[a[1]] = arquivo
                return lista_retorno
            else:
                return False
        else:
            return False
    
    def listaArquivosTemp(self, pasta):
        if os.path.isdir(pasta):
            lista_arquivos = os.listdir(pasta)
            if len(lista_arquivos):
                lista_retorno = []
                for arquivo in lista_arquivos:
                    if os.path.isfile(pasta + arquivo):
                        lista_retorno.append(arquivo)
                return lista_retorno
            else:
                return False
        else:
            return False
    
    def lista_pastas(self):
        return True
    
    
    def deleta_rodando(self):
        if not self.localhost:
            os.unlink(self.URL_rodando + 'rodando.txt')
        
    
    def renomeia(self):
        if len(self.pastas) > 0 :
            for pasta in self.pastas:
                print(pasta)
                pasta_completa = self.cwd + pasta + '/'
                lista = self.listaArquivosTemp(pasta_completa)
                if lista:
                    for arquivo in lista:
                        copyfile(pasta_completa + arquivo, pasta_completa + 'destaque_' + arquivo)
                        copyfile(pasta_completa + arquivo, pasta_completa + 'vitrine_' + arquivo)
                        copyfile(pasta_completa + arquivo, pasta_completa + 'ampliado_' + arquivo)
                        os.remove(pasta_completa + arquivo)
                        print(pasta_completa + arquivo)
                        print(pasta_completa + 'destaque_' + arquivo)
        return True
    
    def main(self):
        if len(self.pastas) > 0 :
            for pasta in self.pastas:
                print(pasta)
                pasta_completa = self.cwd + pasta + '/'
                lista = self.listaArquivos(pasta_completa)
                print(lista)
                if lista:
                    for id_imovel, arquivo in lista.items():
                        i = self.images.verificaPastaImovel(pasta,id_imovel)
                        if i:
                            vitrine = arquivo.replace('destaque','vitrine')
                            if os.path.isfile(pasta_completa + vitrine):
                                os.remove(pasta_completa + vitrine)
                            ampliado = arquivo.replace('destaque','ampliado')
                            if os.path.isfile(pasta_completa + ampliado):
                                copyfile(pasta_completa + ampliado, pasta_completa + id_imovel + '/' + vitrine)
                                os.remove(pasta_completa + ampliado)
                            copyfile(pasta_completa + arquivo, pasta_completa + id_imovel + '/' + arquivo)
                            os.remove(pasta_completa + arquivo)
                            print(pasta_completa + arquivo)
                        else:
                            print(pasta,i)    
        return True
    
if __name__ == '__main__':
    Verifica().main()