import os
from PIL import Image
from resizeimage import resizeimage
import requests
import os.path

# https://github.com/charlesthk/python-resize-image
class myImages(object):

    def __init__(self, id_empresa):
        self.ID = id_empresa

    def executa(self,image,nome):
        for tamanho in self.tamanhos():
            self.geraImages(image,nome,tamanho)

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
            caminho = '../../originais/'
            with open(caminho + arquivo, 'wb') as f:
                f.write(res.content)
            self.executa(caminho + arquivo, arquivo)
            return 'F_' + arquivo
        else:
            return False

    def geraImages(self,image,nome,tamanho):
        pa = '../../imo/' + tamanho['prefixo'] + nome
        if os.path.exists(pa):
            with Image.open(image) as imagem:
                print(tamanho['width'])
                print(imagem.width)
                if tamanho['width'] == 'auto' :
                    cover = resizeimage.resize_width(imagem,imagem.size[0])
                elif tamanho['width'] > imagem.width :
                    cover = resizeimage.resize_width(imagem,imagem.size[0])
                else:
                    cover = resizeimage.resize_width(imagem,tamanho['width'])
                cover.save('../../imo/' + tamanho['prefixo'] + nome, 'jpeg')

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
        myImages(83544)
    except KeyboardInterrupt:
        pass
    finally:
        print("Finaliza myPNG")
