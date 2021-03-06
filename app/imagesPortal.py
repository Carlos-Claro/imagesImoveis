import os
from PIL import Image
Image.LOAD_TRUNCATED_IMAGES = True
from resizeimage import resizeimage
import requests
import os.path
import time
import datetime

# https://github.com/charlesthk/python-resize-image
class imagesPortal(object):

    def __init__(self):
        self.pasta_cwd = '/home/images/portais/'
        self.headers = {'User-Agent': 'Portaisimobiliarios.com.br - gerador de images 1.0'}

    def executa(self,image,nome, caminho):
        for tamanho in self.tamanhos():
            self.geraImages(image,nome,tamanho, caminho)

    def get_extensao_original(self, mime):
        if 'jpeg' in mime:
            return 'jpg'
        elif 'png' in mime:
            return 'png'
        else:
            return 'jpg'
    
    def verificaPasta(self,id_empresa):
        if os.path.isdir(self.pasta_cwd + id_empresa):
            if os.path.isdir(self.pasta_cwd + id_empresa + '/originais'):
                return True
            else:
                os.mkdir(self.pasta_cwd + id_empresa + '/originais', 0o777)
                return self.verificaPasta(id_empresa)
        else:
            os.mkdir(self.pasta_cwd + id_empresa, 0o777)
            return self.verificaPasta(id_empresa)
    
    def verificaPastaImovel(self,id_empresa,id_imovel):
        if os.path.isdir(self.pasta_cwd + id_empresa + '/' + id_imovel):
            return True
        else:
            os.mkdir(self.pasta_cwd + id_empresa + '/' + id_imovel, 0o777)
            return self.verificaPastaImovel(id_empresa, id_imovel)
    
    def setArquivo(self,image,imovel):
        if 'http' in image['arquivo'] :
            return image['arquivo']
        else:
            return 'http://pow.com.br/powsites/' + str(imovel['id_empresa']) + '/imo/650F_' + image['arquivo']
        
    
    def copyImage(self,imovel):
        inicio = time.time()
        self.verificaPasta(imovel['id_empresa'])
        retorno = []
        for image in imovel['images']:
            self.verificaPastaImovel(imovel['id_empresa'], imovel['id'])
            a = self.setArquivo(image, imovel)
            print(a)
            try:
                res = requests.get(a, stream=True, headers=self.headers, timeout=10)
            except requests.exceptions.HTTPError as e:
                fim = time.time()
                print(fim-inicio)
                print('httperror')
                print(a)
                retorno.append({'id': image['id'], 'gerado_image':2, 'data':datetime.datetime.now().strftime('%Y-%m-%d %H:%M')})
                # Whoops it wasn't a 200
                print("Error: " + str(e))
                return retorno
            except requests.exceptions.Timeout as e:
                fim = time.time()
                print(fim-inicio)
                print('timeout')
                print(a)
                retorno.append({'id': image['id'], 'gerado_image':2, 'data':datetime.datetime.now().strftime('%Y-%m-%d %H:%M')})
                # Whoops it wasn't a 200
                print("Error: " + str(e))
                return retorno
            except requests.exceptions.SSLError as e:
                fim = time.time()
                print(fim-inicio)
                print('sslerror')
                print(a)
                retorno.append({'id': image['id'], 'gerado_image':2, 'data':datetime.datetime.now().strftime('%Y-%m-%d %H:%M')})
                # Whoops it wasn't a 200
                print("Error: " + str(e))
                return retorno
            else:
                if res.status_code == 200:
                    if 'content-type' in res.headers:
                        content_type = res.headers['content-type']
                    else:
                        content_type = 'html'
                    print(res.status_code)
                    print(res.headers)
                    print(res.headers['content-type'])
                    if not 'html' in content_type:
                        print(content_type)
                        extensao = self.get_extensao_original(content_type)
                        nome_arquivo = '{}_{}.{}'.format(imovel['id'],image['id'], extensao)
                        caminho = self.pasta_cwd + str(imovel['id_empresa']) + '/'
                        caminho_id = self.pasta_cwd + str(imovel['id_empresa']) + '/' + str(imovel['_id']) + '/'
                        with open(caminho + 'originais/' + nome_arquivo, 'wb') as f:
                            f.write(res.content)
                        print(caminho + 'originais/' + nome_arquivo)
                        self.executa(caminho + 'originais/' + nome_arquivo, nome_arquivo, caminho_id)
                        arquivo_destaque = caminho_id + 'destaque_' + nome_arquivo
                        os.unlink(caminho + 'originais/' + nome_arquivo)
                        if os.path.exists(arquivo_destaque):
                            fim = time.time()
                            print(fim-inicio)
                            retorno.append({'id': image['id'], 'extensao':extensao, 'gerado_image':1,'data':datetime.datetime.now().strftime('%Y-%m-%d %H:%M')})
                        else:
                            fim = time.time()
                            print(fim-inicio)
                            retorno.append({'id': image['id'], 'gerado_image':2, 'data':datetime.datetime.now().strftime('%Y-%m-%d %H:%M')})
                    else:
                        fim = time.time()
                        print(fim-inicio)
                        retorno.append({'id': image['id'], 'gerado_image':2, 'data':datetime.datetime.now().strftime('%Y-%m-%d %H:%M')})
                else:
                    fim = time.time()
                    print(fim-inicio)
                    retorno.append({'id': image['id'], 'gerado_image':2, 'data':datetime.datetime.now().strftime('%Y-%m-%d %H:%M')})
        return retorno    
        
    def geraImages(self,image,nome,tamanho, caminho):
        pa = caminho +  tamanho['prefixo'] + nome
        print(pa)
        if os.path.exists(pa) == False:
            with Image.open(image) as imagem:
                print(tamanho['width'])
                print(imagem.width)
                try:
                    if tamanho['width'] == 'auto' :
                        cover = resizeimage.resize_width(imagem,imagem.size[0])
                    elif tamanho['width'] >= imagem.width :
                        cover = resizeimage.resize_width(imagem,imagem.size[0])
                    else:
                        cover = resizeimage.resize_width(imagem,tamanho['width'])
                    cover.convert('RGB').save(caminho + tamanho['prefixo'] + nome, 'jpeg')
                except IOError:
                    pass

    def tamanhos(self):
        tamanho = [
                    {'width':300,       'height':'auto', 'prefixo':'destaque_'},
                    {'width':'auto',    'height':'auto', 'prefixo':'vitrine_'},
                    #{'width':'auto',    'height':'auto', 'prefixo':'ampliado_'},
                ]
        return tamanho


if __name__ == '__main__':
    try:
        imagesPortal()
    except KeyboardInterrupt:
        pass
    finally:
        print("Finaliza myPNG")
