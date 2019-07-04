# -*- coding: utf-8 -*-
import requests
import shutil
from imagesPortal import imagesPortal
import datetime
import time
import os
import sys

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
        self.arquivoVerificador = 'relatorios/verificador.json'
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
                        if 'destaque_' is arquivo[0]:
                            a = arquivo.split('_')
                            lista_retorno[a[1]] = arquivo
                return lista_retorno
            else:
                return False
        else:
            return False
    
    def rodando(self):
        if os.path.exists(self.URL_rodando + 'rodando.txt') :
            print('rodando')
            print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M'))
            stat = os.stat(self.URL_rodando + 'rodando.txt')
            if stat.st_mtime + 360 < time.time():
                self.deleta_rodando()
                print('maior, tente novamente')
                print(stat.st_mtime)
                print(time.time())
                return False
            else:
                print('menor, aguarde...')
                return False
        else:
            with open(self.URL_rodando + 'rodando.txt', 'w') as f:
                f.write('rodando - ')
                f.write(datetime.datetime.now().strftime('%Y-%m-%d %H:%M'))
                return True
    
    def lista_pastas(self):
        return True
    
    
    def deleta_rodando(self):
        if not self.localhost:
            os.unlink(self.URL_rodando + 'rodando.txt')
        
    
    def main(self):
        if len(self.pastas) > 0 :
            for pasta in self.pastas:
                print(pasta)
                pasta_completa = self.cwd + pasta 
                lista = self.listaArquivos(pasta_completa)
                if lista:
                    for arquivo in lista:
                        existe = self.verificaImovelexiste(arquivo)
                        if not existe:
                            self.deletarArquivos(pasta_completa,arquivo)
                            print(arquivo + ' nao existe')
                self.atualizarArquivo(pasta)
        return True
    
if __name__ == '__main__':
    Verifica().main()