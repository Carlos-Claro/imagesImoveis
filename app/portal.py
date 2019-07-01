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
        self.images = imagesPortal()

    def main(self):
        if os.path.exists('rodando.txt') :
            print('rodando')
        else:
            with open('rodando.txt', 'w') as f:
                f.write('rodando')
            images = requests.get(self.URL_GET)
            i = images.json()
            for v in i:
                print('id - ' + str(v['id']) + ' - ' + v['arquivo'])
                res = self.images.copyImage(v)
                if res:
                    data = {'extensao': str(res), 'data':datetime.datetime.now().strftime('%Y-%m-%d %H:%M'), 'gerado_image' : 1}
                    update = requests.put(self.URL_PUT + str(v['id']),params=data)
                    print('res sucesso')
                    print(data)
                    print(self.URL_PUT + str(v['id']))
                    print(update.status_code)
                    print(update.content)
                else:
                    print('res fail')
                    print(v)
                    data = {'data':datetime.datetime.now().strftime('%Y-%m-%d %H:%M'),'gerado_image':2}
                    print(data)
                    update = requests.put(self.URL_PUT + str(v['id']),params=data)
            self.fim = time.time()
            print(self.fim-self.inicio)
            os.unlink('rodando.txt')
            
        
    
if __name__ == '__main__':
    Imoveis().main()