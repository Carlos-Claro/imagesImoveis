# -*- coding: utf-8 -*-
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
        self.args = sys.argv
        self.argumentos = {}
        if 'localhost' in sys.argv:
            self.localhost = True
            self.URI = 'http://localhost:5000/'
            self.cwd = '/home/www/images/pow/'
        else:
            self.localhost = False
            self.URI = 'http://imoveis.powempresas.com/'
            self.cwd = '/home/pow/www/powsites/'
        for a in self.args:
            if '-' in a:
                cortado = a.split('-')
                posicao_e = self.args.index(a)
                self.argumentos[cortado[1]] = self.args[posicao_e+1]
        self.ARQUIVO_LOG = self.cwd + 'integra_mongo.log'
        self.FORMATO_LOG = '{data} - empresa {id_empresa} - id {id} - arquivo {arquivo} - status {status} '
        self.inicio = time.time()
        self.images = imagesPortal()
        self.arquivoVerificador = self.cwd + '/verifica_deleta.json'
        if 'e' in self.argumentos:
            self.runEmpresa(self.argumentos['e'])
        else:
            if self.verificaArquivo():
                self.run()
        
        
    def runEmpresa(self, idEmpresa):
        pastaCompleta = self.cwd + idEmpresa + '/imo/'
        self.moveArquivos(pastaCompleta,idEmpresa)
    
    def run(self):
        for pasta in self.pastas:
            pastaCompleta = self.cwd + pasta + '/imo/'
            self.moveArquivos(pastaCompleta,pasta)
        
    def setLog(self, data):
        linha = self.FORMATO_LOG.format(**data)
        with open(self.ARQUIVO_LOG,'a') as arq:
            arq.write(linha)
            arq.write('\r\n')
    
    def verificaArquivo(self):
        try:
            with open(self.arquivoVerificador,'r') as json_file:
                self.pastas = json.load(json_file)
                return True
        except IOError:
            pastas = os.listdir(self.cwd)
            lista_pastas = []
            for pasta in pastas:
                if os.path.isdir(self.cwd + pasta):
                    print(pasta)
                    lista_pastas.append(pasta)
            with open(self.arquivoVerificador,'w') as arq:
                arq.write(json.dumps(lista_pastas))
            return self.verificaArquivo()
    
    def moveArquivos(self, pastaCompleta, pasta):
        data_log = {'data':datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'id_empresa':pasta}
        if os.path.isdir(pastaCompleta):
            lista_arquivos = os.listdir(pastaCompleta)
            if len(lista_arquivos):
                lista_retorno = {}
                for arquivo in lista_arquivos:
                    move = True
                    if os.path.isfile(pastaCompleta + arquivo):
                        arquivo_explode = arquivo.split('_')
                        if 'F' is arquivo[0]:
                            id_imovel = arquivo_explode[1]
                        elif 'TM' in arquivo_explode[0]:
                            if 'F' in arquivo_explode[1]:
                                id_imovel = arquivo_explode[2]
                            else:
                                id_imovel = arquivo_explode[1]
                        elif 'destaque' in arquivo_explode[0]:
                            if 'F' in arquivo_explode[1]:
                                id_imovel = arquivo_explode[2]
                            else:
                                id_imovel = arquivo_explode[3]
                        else:
                            if len(arquivo_explode) == 1:
                                move = False
                                id_imovel = '0'
                            else:
                                id_imovel = arquivo_explode[2]
                        data_log['id'] = id_imovel;
                        data_log['arquivo'] = arquivo;
                        if move:
                            if self.criaPasta(pastaCompleta + id_imovel):
                                try:
                                    shutil.move(pastaCompleta + arquivo, pastaCompleta + id_imovel + '/' + arquivo)
                                    data_log['status'] = 'ok'
                                except OSError as e:
                                    data_log['status'] = 'erro movendo'
                            else:
                                data_log['status'] = 'erro criando pasta'
                            self.setLog(data_log)
                        else:
                            data_log['id'] = '0';
                            data_log['arquivo'] = arquivo;
                            data_log['status'] = 'erro arquivo não move'
                            self.setLog(data_log)
            else:
                data_log['id'] = '0';
                data_log['arquivo'] = '';
                data_log['status'] = 'erro sem arquivos'
                self.setLog(data_log)
        else:
            data_log['id'] = '0';
            data_log['arquivo'] = '';
            data_log['status'] = 'erro sem diretorio ' + pastaCompleta
            self.setLog(data_log)
            
            
    def criaPasta(self,pasta):
        if os.path.exists(pasta):
            return True
        else:
            try:
                os.mkdir(pasta)
                return True
            except OSError as e:
                print(' problemas para criar pasta ' + pasta)
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
    
    def deleta_rodando(self):
        if not self.localhost:
            os.unlink(self.URL_rodando + 'rodando.txt')
        
    def main(self):
        return True
    
if __name__ == '__main__':
    Verifica().main()