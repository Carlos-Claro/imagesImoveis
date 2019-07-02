import os
from PIL import Image
from resizeimage import resizeimage
import requests
import os.path
import time

# https://github.com/charlesthk/python-resize-image
class imagesPortal(object):

    def __init__(self):
        self.pasta_cwd = '/var/www/html/images/portais/'

    def executa(self,image,nome, caminho):
        for tamanho in self.tamanhos():
            self.geraImages(image,nome,tamanho, caminho)

    def get_extensao_original(self, mime):
        if 'jpeg' in mime:
            return 'jpg'
        elif 'png' in mime:
            return 'png'
    
    def verificaPasta(self,id_empresa):
        if os.path.isdir(self.pasta_cwd + id_empresa):
            if os.path.isdir(self.pasta_cwd + id_empresa + '/originais'):
                return True
            else:
                os.mkdir(self.pasta_cwd + id_empresa + '/originais')
                return self.verificaPasta(id_empresa)
        else:
            os.mkdir(self.pasta_cwd + id_empresa)
            return self.verificaPasta(id_empresa)
    
    def setArquivo(self,image):
        if 'http' in image['arquivo'] :
            return image['arquivo']
        else:
            return 'http://pow.com.br/powsites/' + str(image['id_empresa']) + '/imo/650F_' + image['arquivo']
        
    
    def copyImage(self,image):
        inicio = time.time()
        a = self.setArquivo(image)
        res = requests.get(a, stream=True)
        content_type = res.headers['content-type']
        if res.status_code == 200 and not 'html' in content_type:
            id_empresa = str(image['id_empresa'])
            self.verificaPasta(id_empresa)
            extensao = self.get_extensao_original(content_type)
            nome_arquivo = '{}_{}.{}'.format(image['id_imovel'],image['id'], extensao)
            caminho = self.pasta_cwd + id_empresa + '/'
            with open(caminho + 'originais/' + nome_arquivo, 'wb') as f:
                f.write(res.content)
            self.executa(caminho + 'originais/' + nome_arquivo, nome_arquivo, caminho)
            arquivo_destaque = caminho + 'destaque_' + nome_arquivo
            os.unlink(caminho + 'originais/' + nome_arquivo)
            if os.path.exists(arquivo_destaque):
                fim = time.time()
                print(fim-inicio)
                return extensao
            else:
                fim = time.time()
                print(fim-inicio)
                return False
        else:
            fim = time.time()
            print(fim-inicio)
            return False

    def geraImages(self,image,nome,tamanho, caminho):
        pa = caminho + tamanho['prefixo'] + nome
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
                cover.save(caminho + tamanho['prefixo'] + nome, 'jpeg')

    def tamanhos(self):
        tamanho = [
                    {'width':300,       'height':'auto', 'prefixo':'destaque_'},
                    {'width':600,       'height':'auto', 'prefixo':'vitrine_'},
                    {'width':'auto',    'height':'auto', 'prefixo':'ampliado_'},
                ]
        return tamanho


if __name__ == '__main__':
    try:
        imagesPortal()
    except KeyboardInterrupt:
        pass
    finally:
        print("Finaliza myPNG")
