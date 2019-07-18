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
        self.URI_VERIFICA = self.URI + 'imoveis_in/'
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
                            b = arquivo.split('.')
                            a = b[0].split('_')
                            lista_retorno[a[1] + '-' + a[2]] = arquivo
                return lista_retorno
            else:
                return False
        else:
            return False
    
    def listaArquivosTemp(self, pasta):
        if os.path.isdir(pasta):
            lista_arquivos = os.listdir(pasta)
            return lista_arquivos
        else:
            return False
        
    def listaPastas(self, pasta):
        if os.path.isdir(pasta):
            lista_arquivos = os.listdir(pasta)
            if len(lista_arquivos):
                return lista_arquivos
            return []
    
    def deleta_pasta(self):
        if len(self.pastas) > 0 :
            lista = {}
            for pasta in self.pastas:
                pasta_completa = self.cwd + pasta + '/'
                lista[pasta] = self.listaPastas(pasta_completa)
            self.verifica_lista(lista)
        return True
    
    def verifica_lista(self, lista):
        for empresa,itens in lista.items():
            print(empresa)
            if len(itens):
                print(itens)
                data = {'id':json.dumps(itens)}
                res = requests.get(self.URI_VERIFICA + empresa, params=data)
                content = res.content
                r = content.json()
                if content['deleta']:
                    print(str(content['id']))
        pass
    
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
                        copyfile(pasta_completa + arquivo, pasta_completa + arquivo)
                        copyfile(pasta_completa + arquivo, pasta_completa + arquivo.replace('destaque_','vitrine_'))
                        copyfile(pasta_completa + arquivo, pasta_completa + arquivo.replace('destaque_','ampliado_'))
                        os.remove(pasta_completa + arquivo)
                        print(pasta_completa + arquivo)
                        print(pasta_completa + 'destaque_' + arquivo)
        return True
    
    def main(self):
        if len(self.pastas) > 0 :
            for pasta in self.pastas:
                print(pasta)
                pasta_completa = self.cwd + str(pasta) + '/'
                lista = self.listaArquivos(pasta_completa)
                print(lista)
                if lista:
                    for id_imovel, arquivo in lista.items():
                        a = id_imovel.split('-')
                        imovel = a[0]
                        i = self.images.verificaPastaImovel(str(pasta),str(imovel))
                        if i:
                            destaque = arquivo
                            vitrine = arquivo.replace('destaque','vitrine')
                            ampliado = arquivo.replace('destaque','ampliado')
                            if os.path.isfile(pasta_completa + vitrine):
                                os.unlink(pasta_completa + vitrine)
                            if os.path.isfile(pasta_completa + ampliado):
                                copyfile(pasta_completa + ampliado, pasta_completa + str(imovel) + '/' + vitrine)
                                os.unlink(pasta_completa + ampliado)
                            copyfile(pasta_completa + arquivo, pasta_completa + str(imovel) + '/' + arquivo)
                            os.unlink(pasta_completa + arquivo)
                        else:
                            print(pasta,i)    
        return True
    
if __name__ == '__main__':
    Verifica().deleta_pasta()