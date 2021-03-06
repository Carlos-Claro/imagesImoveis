# -*- coding: utf-8 -*-
import requests
import shutil
from imagesPortal import imagesPortal
import datetime
import time
import os
import sys
import json
from requests.auth import HTTPBasicAuth

class Imoveis(object):
    
    def __init__(self):
        argument = sys.argv
        if 'localhost' in argument:
            self.localhost = True
            self.URI = 'http://localhost:5000/'
            with open('../../../json/keys.json') as json_file:
                data = json.load(json_file)
        else:
            self.localhost = False
            self.URI = 'http://imoveis.powempresas.com/'
            with open('/home/carlos/json/keys.json') as json_file:
                data = json.load(json_file)
        self.user = data['basic']['user']
        self.passwd = data['basic']['passwd']
        self.auth = HTTPBasicAuth(self.user,self.passwd)
        self.inicio = time.time()
        self.URL_GET = self.URI + 'imoveis_images_gerar/50'
        self.URL_PUT = self.URI + 'imovel_images_imovel/'
        self.URL_PUT_IMOVEL = self.URI + 'imovel/'
        self.URL_PUT_MONGO = self.URI + 'imoveismongo/'
        self.URL_rodando = '/home/images/'
        self.images = imagesPortal()
        self.id_empresa = False
        if '-e' in sys.argv:
            posicao_e = argument.index('-e')
            self.id_empresa = argument[posicao_e+1]
        self.main()
        
    def rodando(self):
        if ( self.localhost ):
            return True
        else:
            if os.path.exists(self.URL_rodando + 'rodando.txt') :
                print('rodando')
                print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M'))
                stat = os.stat(self.URL_rodando + 'rodando.txt')
                if stat.st_mtime + 720 < time.time():
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
    
    def deleta_rodando(self):
        if not self.localhost:
            os.unlink(self.URL_rodando + 'rodando.txt')
        
    
    def main(self):
        if self.rodando():
            if self.id_empresa:
                data = {'id_empresa':self.id_empresa}
                imoveis = requests.get(self.URL_GET, params=data, auth=self.auth)
            else:
                imoveis = requests.get(self.URL_GET, auth=self.auth)
            i = imoveis.json()
            print(i)
            for v in i['itens']:
                print('imovel - ' + str(v['_id']) + ' empresa - ' + v['id_empresa'])
                if 'images' in v:
                    res = self.images.copyImage(v)
                    print(res)
                    if res:
                        for r in res:
                            update = requests.put(self.URL_PUT,params=r, auth=self.auth)
                            print(update.status_code)
                        data_imovel = {'integra_mongo_db':"0000-00-00"}
                        update_imovel = requests.put(self.URL_PUT_IMOVEL + str(v['_id']),params=data_imovel, auth=self.auth)
                        data_mongo = {'tem_foto':1,'data_update':datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}
                        update_mongo = requests.put(self.URL_PUT_MONGO + str(v['_id']),params=data_mongo, auth=self.auth)
                        print('res sucesso')
                        print(r)
                        print(self.URL_PUT + str(v['id']))
                        print(self.URL_PUT_IMOVEL + str(v['id']))
                        print(update.content)
                        print('imovel')
                        print(update_imovel.status_code)
                        print(update_imovel.content)
                        print('mongo')
                        print(update_mongo.status_code)
                        print(update_mongo.content)
                    else:
                        data_mongo = {'tem_foto':1,'data_update':datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}
                        update_mongo = requests.put(self.URL_PUT_MONGO + str(v['_id']),params=data_mongo, auth=self.auth)
                        print('res fail')
                        print(v['_id'])
            self.fim = time.time()
            print(self.fim-self.inicio)
            self.deleta_rodando()
            
        
    
if __name__ == '__main__':
    Imoveis()