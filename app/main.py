# -*- coding: utf-8 -*-
import requests
import shutil
from myImages import myImages
import datetime

class Imoveis(object):
    
    def __init__(self):
        self.URI = 'http://localhost:5000/'
        #self.URI = 'http://201.16.246.176:5000/'
        self.URL_GET = self.URI + 'imovel_images_copy'
        self.URL_PUT = self.URI + 'imovel_images/'
        self.images = myImages(85344)

    def main(self):
        images = requests.get(self.URL_GET)
        print(images.status_code)
        i = images.json()
        for v in i:
            print(v['arquivo'])
            res = self.images.copyImage(v)
            if res:
                data = {'arquivo': str(res), 'data':datetime.datetime.now().strftime('%Y-%m-%d ')}
                update = requests.put(self.URL_PUT + str(v['id']),params=data)
                print(v)
                print(data)
                print(self.URL_PUT + str(v['id']))
                print(update.status_code)
                print(update.content)
            else:
                print(v)
                data = {'data':datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}
                print(data)
                update = requests.put(self.URL_PUT + str(v['id']),params=data)
                
            
        
    
if __name__ == '__main__':
    Imoveis().main()