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


class Verifica_cidade(object):
    
    def __init__(self):
        if 'localhost' in sys.argv:
            self.localhost = True
            self.URI = 'http://localhost:5000/'
        else:
            self.localhost = False
            self.URI = 'http://imoveis.powempresas.com/'
        self.URI_VERIFICA = self.URI + 'imoveis_cidade/'
        self.URL_PUT = self.URI + 'update_imovel_verifica/'
        self.URL_DELETA_MONGO = self.URI + 'imoveismongo/'
        self.URL_PUT_IMOVEL = self.URI + 'imovel/'
        self.inicio = time.time()
        self.images = imagesPortal()
        self.cwd = '/var/www/html/images/portais/'
        self.arquivoVerificador = self.cwd + 'verifica_cidades_.json'
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
            self.verifica_lista(lista, pasta_completa)
        #os.unlink(self.arquivoVerificador)
        return True
    
    def verifica_lista(self, lista, pasta):
        for empresa,itens in lista.items():
            print('empresa',empresa)
            if len(itens):
                qtde_mantem = 0
                qtde_deleta = 0
                for item in itens:
                    if item.isnumeric():
                        res_v = requests.get(self.URI_VERIFICA + item)
                        if res_v.status_code == 403:
                            p = self.cwd + empresa + '/' + item
                            data_update = {'gerado_image':'0'}
                            update = requests.put(self.URL_PUT + str(item),params=data_update)
                            data_imovel = {'integra_mongo_db':"0000-00-00"}
                            update_imovel = requests.put(self.URL_PUT_IMOVEL + str(item),params=data_imovel)
                            delete_imovel_mongo = requests.delete(self.URL_DELETA_MONGO + str(item))
                            shutil.rmtree(p)
                            qtde_deleta = qtde_deleta + 1
                        else:
                            qtde_mantem = qtde_mantem + 1
                print('mantem', qtde_mantem)
                print('deleta', qtde_deleta)
        return True
    
    def main(self):
        
        return True
    
if __name__ == '__main__':
    Verifica_cidade().deleta_pasta()