# -*- coding: utf-8 -*-
import requests
import shutil
from imagesPortal import imagesPortal
import datetime
import time
import os

class Imoveis(object):
    
    def __init__(self):
        self.inicio = time.time()
        #self.URI = 'http://localhost:5000/'
        self.URI = 'http://201.16.246.176:5000/'
        self.URL_GET = self.URI + 'imoveis_images_gerar/100'
        self.URL_PUT = self.URI + 'imovel_images/'
        self.URL_PUT_IMOVEL = self.URI + 'imovel/'
        self.URL_rodando = '/var/www/html/images/'
        self.images = imagesPortal()

    def main(self):
        if os.path.exists(self.URL_rodando + 'rodando.txt') :
            print('rodando')
        else:
            with open(self.URL_rodando + 'rodando.txt', 'w') as f:
                f.write('rodando')
                f.write(datetime.datetime.now().strftime('%Y-%m-%d %H:%M'))
            images = requests.get(self.URL_GET)
            i = images.json()
            for v in i:
                print('id - ' + str(v['id']) + ' - ' + v['arquivo'])
                res = self.images.copyImage(v)
                if res:
                    data = {'extensao': str(res), 'data':datetime.datetime.now().strftime('%Y-%m-%d %H:%M'), 'gerado_image' : 1}
                    update = requests.put(self.URL_PUT + str(v['id']),params=data)
                    data_imovel = {'integra_mongo_db':"0000-00-00"}
                    update_imovel = requests.put(self.URL_PUT_IMOVEL + str(v['id_imovel']),params=data_imovel)
                    print('res sucesso')
                    print(data)
                    print(self.URL_PUT + str(v['id']))
                    print(self.URL_PUT_IMOVEL + str(v['id_imovel']))
                    print(update.status_code)
                    print(update.content)
                    print(update_imovel.status_code)
                    print(update_imovel.content)
                else:
                    print('res fail')
                    print(v)
                    data = {'data':datetime.datetime.now().strftime('%Y-%m-%d %H:%M'),'gerado_image':2}
                    print(data)
                    update = requests.put(self.URL_PUT + str(v['id']),params=data)
            self.fim = time.time()
            print(self.fim-self.inicio)
            os.unlink(self.URL_rodando + 'rodando.txt')
            
        
    
if __name__ == '__main__':
    Imoveis().main()