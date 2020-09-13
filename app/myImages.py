import os
from PIL import Image
from resizeimage import resizeimage
import requests
import os.path

# https://github.com/charlesthk/python-resize-image
class myImages(object):

    def __init__(self, id_empresa):
        self.ID = id_empresa
        # self.pasta = '/var/www/html/powsites/powsites/{}/'.format(id_empresa)
        self.pasta = '/home/pow/www/powsites/{}/'.format(id_empresa)

    def executa(self,image,nome,id_imovel):
        for tamanho in self.tamanhos():
            self.geraImages(image,nome,tamanho,id_imovel)

    def get_extensao_original(self, mime):
        if 'jpeg' in mime:
            return 'jpg'
        elif 'png' in mime:
            return 'png'
    
    def copyImage(self,image):
        res = requests.get(image['arquivo'], stream=True)
        if res.status_code == 200 :
            content_type = res.headers['content-type']
            arquivo = '{}_{}.{}'.format(image['id_imovel'],image['id'], self.get_extensao_original(content_type))
            caminho = self.pasta + 'originais/'
            print(caminho + arquivo)
            with open(caminho + arquivo, 'wb') as f:
                f.write(res.content)
            pasta_ = self.pasta + 'imo/{}'.format(image['id_imovel'])
            self.verifica_pasta(pasta_)
            self.executa(caminho + arquivo, arquivo,image['id_imovel'])
            arquivo_imo = self.pasta + 'imo/{}/F_{}'.format(image['id_imovel'],arquivo)
            if os.path.exists(arquivo_imo):
                return 'F_' + arquivo
            else:
                return False
        else:
            
            return False

    def verifica_pasta(self,pasta):
        return os.makedirs(pasta,0o777,True)

    def geraImages(self,image,nome,tamanho,id_imovel):
        pa = self.pasta + 'imo/{}/{}{}'.format(id_imovel,tamanho['prefixo'],nome)
        if os.path.exists(pa) == False:
            with Image.open(image) as imagem:
                print(tamanho['width'])
                print(imagem.width)
                if tamanho['width'] == 'auto' :
                    cover = resizeimage.resize_width(imagem,imagem.size[0])
                elif tamanho['width'] > imagem.width :
                    cover = resizeimage.resize_width(imagem,imagem.size[0])
                else:
                    cover = resizeimage.resize_width(imagem,tamanho['width'])
                cover.convert("RGB").save(self.pasta + 'imo/{}/{}{}'.format(id_imovel,tamanho['prefixo'],nome), 'jpeg')

    def tamanhos(self):
        tamanho = [
                    {'width':300,   'height':'auto', 'pasta':'powsites/'+str(self.ID)+'/imo/', 'prefixo':'F_'},
                    {'width':80,    'height':60,     'pasta':'powsites/'+str(self.ID)+'/imo/', 'prefixo':'T_F_'},
                    {'width':240,   'height':'180',  'pasta':'powsites/'+str(self.ID)+'/imo/', 'prefixo':'TM_F_'},
                    {'width':120,   'height':'90',   'pasta':'powsites/'+str(self.ID)+'/imo/', 'prefixo':'T3_F_'},
                    {'width':650,   'height':'auto', 'pasta':'powsites/'+str(self.ID)+'/imo/', 'prefixo':'T5_F_'},
                    {'width':788,   'height':'auto', 'pasta':'powsites/'+str(self.ID)+'/imo/', 'prefixo':'650F_F_'},
                    {'width':'auto',  'height':'auto', 'pasta':'powsites/'+str(self.ID)+'/imo/', 'prefixo':'1150F_F_'},
                ]
        return tamanho


if __name__ == '__main__':
    try:
        myImages(7932)
    except KeyboardInterrupt:
        pass
    finally:
        print("Finaliza myPNG")
