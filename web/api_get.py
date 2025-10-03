import requests
from bs4 import BeautifulSoup
import json
import os
import time
from datetime import datetime, date
from .models import *

# ruta_archivo = os.path.join(os.path.dirname(__file__), "menu.json")
# import unicodedata
# # from colorama import init, Fore, Style
# # init(autoreset=True)
 
# 000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000

def saniticzarUrl(url=False):
    if url:
        url=url.replace("á", "a")
        url=url.replace("é", "e")
        url=url.replace("í", "i")
        url=url.replace("ó", "o")
        url=url.replace("ú", "u")
        # url=url.replace(".", "")
        url=url.lower().replace(" ", "-")
        return url
    else:
        return url
    



# 000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000

def leerJsonConvertirtojson(dato= None, path_archivo="data.json", accion="r"):
    # Obtener la ruta absoluta
    if accion=='w':
        d=json.dumps(dato)
        with open(path_archivo, accion) as f:
            f.write(d)
    if accion=='r':
        with open(path_archivo, accion) as f:
            datos = json.load(f)
        return datos


# 000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000

def getMenuPortalAPi():

    url_api="https://api-portal.catamarca.gob.ar/api/v1/cms/menu/?organismo_id=300&include=organismo" 
    res = requests.get(url_api)
    response = json.loads(res.text)
    nulo=False  # Valido para mysql
    menu={}
    menu[0]={
        'logo': response['included'][0]['attributes']['logo'],
        "titulo":None,
        "nodo_padre":False,
        "url": None, # None, # aqui debe llebvar un url  
        "submenu":{},
    }
    
    for r in response['data']:  
        id=int(r['id'])
        if r['relationships']['nodo_padre']['data']==None:
            # 000000000000000000000000000000000000000000000000000000000000000
            # 000000000000000000000000000000000000000000000000000000000000000
            try:
                url=saniticzarUrl(f"{r['attributes']['titulo']}/{r['attributes']['enlace_interno']['id']}") 
            except:                
                url="#"

            menu[id]={
                "titulo":r['attributes']['titulo'],
                "key": f"menu{id}",
                "nodo_padre":False,
                "url": url, # None, # aqui debe llebvar un url  
                "submenu":{},
            }
            # 000000000000000000000000000000000000000000000000000000000000000
            # 000000000000000000000000000000000000000000000000000000000000000

        else:
            nodo_padre=int(r['relationships']['nodo_padre']['data']['id'])
            url=None
            try:
                try:
                    path0=menu[nodo_padre]['titulo']
                    path1 = r['attributes']['titulo']
                    path2 = r['attributes']['enlace_interno']['id']
                    url= saniticzarUrl(f"{path0}/{path1}/{path2}")
                except:
                    pass
                # 000000000000000000000000000000000000000000000000000000000000000
                # 000000000000000000000000000000000000000000000000000000000000000
                menu[nodo_padre]['submenu'][id]={
                    "titulo":r['attributes']['titulo'],
                    "nodo_padre":nodo_padre,
                    "key": f"menu{id}",
                    "url":url,
                    "submenu":{}
                }
                # 000000000000000000000000000000000000000000000000000000000000000
                # 000000000000000000000000000000000000000000000000000000000000000
            except:
                for m, sm  in menu.items():
                    # print(sm["submenu"][nodo_padre]["titulo"])
                    if nodo_padre in sm['submenu']:
                        # menu[nodo_padre]
                        # print(sm["titulo"])
                        # print(sm["submenu"][nodo_padre]["titulo"])
                        path0=sm["titulo"]
                        path1=sm["submenu"][nodo_padre]["titulo"]
                        path2 = r['attributes']['titulo']
                        path3 = r['attributes']['enlace_interno']['id']
                        url= saniticzarUrl(f"{path0}/{path1}/{path2}/{path3}")
                        sm['submenu'][nodo_padre]['submenu'][id]={
                            "titulo":r['attributes']['titulo'],
                            "nodo_padre":nodo_padre,
                            "key": f"menu{id}",
                            "url": url, #None, # aqui debe llevar el url 
                            "submenu":None,
                        }

    return menu

# 000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000

def getContenidoURL(url):
    try:
        response=requests.get(url)
        datos=json.loads(response.text) # envio en forma de diccionario modificado`
        try:
            datos['carrusel']=[]
            for d in datos['included']:
                # if d['relationships']['nodo_padre']['data']==None:
                if d['attributes']['componente']['type'] == "ImagenCarousel": #ContenidoTexto  ImagenCarousel
                    datos['carrusel'].append(d['attributes']['componente']['attributes']['imagen'])

                if d['attributes']['componente']['type'] == "ContenidoTexto": #ContenidoTexto  ImagenCarousel
                    print(d['attributes']['componente']['type'])
                # if d['attributes']['componente']['attributes']['texto']: #ContenidoTexto
                    html_content = d['attributes']['componente']['attributes']['texto']
                    try:
                        soup = BeautifulSoup(html_content, 'html.parser')
                        images = soup.find_all('img') # busca todoas la etqieuta img
                        # print("0000000000000000000000000000000000000000000000000000000000000000000000000000000")
                        # print(images)
                        # print("0000000000000000000000000000000000000000000000000000000000000000000000000000000")
                        d['attributes']['componente']['attributes']['imagenes'] = [img['src'] for img in images if 'src' in img.attrs] # extraigo los url de todas la etiquetas img encontradas 
                        soup.img.extract() # extraigo la etiqueta img si encuentra
                        for img in soup.find_all('img'):
                            img.extract()
                        d['attributes']['componente']['attributes']['texto']= soup.prettify()
                    except:
                        pass
               
        except:
            return json.loads(response.text) # envio en forma de diccionario modificado
        finally:
            return datos # envio en forma de diccionario modificadok
    except:
        return False





# 000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000

# # # def getMenuPortalAPi():

# # #     # return leerJsonConvertirtojson(path_archivo="web\data.json", accion="r")
# # #     url_api="https://api-portal.catamarca.gob.ar/api/v1/cms/menu/?organismo_id=300&include=organismo" 
# # #     # url_api
# # #     # ="https://api-portal.catamarca.gob.ar/api/v1/cms/menu/?organismo_id=300"
# # #     res = requests.get(url_api)
# # #     response = json.loads(res.text)
# # #     # menu=[]
# # #     # data={'data':{'logo': response['included'][0]['attributes']['logo']}}
# # #     # menu.append(data)
# # #     # nulo=None  # Valido para sqlite
# # #     nulo=False  # Valido para mysql
# # #     menu={}
# # #     menu[0]={
# # #         'logo': response['included'][0]['attributes']['logo'],
# # #         "titulo":None,
# # #         "nodo_padre":False,
# # #         "url": None, # None, # aqui debe llebvar un url  
# # #         "submenu":{},
# # #     }
    
# # #     for r in response['data']:  
# # #         id=int(r['id'])
# # #         if r['relationships']['nodo_padre']['data']==None:
# # #             # print(r['id'])
# # #             # print(r['attributes']['titulo'])
# # #             # if r['attributes']['enlace_interno']:
# # #             #     path0 = r['attributes']['titulo']
# # #             #     path1 = r['attributes']['enlace_interno']['id']
# # #             #     url= saniticzarUrl(f"{path0}/{path1}")
# # #             # 000000000000000000000000000000000000000000000000000000000000000
# # #             # 000000000000000000000000000000000000000000000000000000000000000
# # #             try:
# # #                 url=saniticzarUrl(f"{r['attributes']['titulo']}/{r['attributes']['enlace_interno']['id']}") 
# # #             except:                
# # #                 url="#"

# # #             menu[id]={
# # #                 "titulo":r['attributes']['titulo'],
# # #                 "key": f"menu{id}",
# # #                 "nodo_padre":False,
# # #                 "url": url, # None, # aqui debe llebvar un url  
# # #                 "submenu":{},
# # #             }
# # #             # 000000000000000000000000000000000000000000000000000000000000000
# # #             # 000000000000000000000000000000000000000000000000000000000000000

# # #         else:
# # #             nodo_padre=int(r['relationships']['nodo_padre']['data']['id'])
# # #             url=None
# # #             try:
# # #                 try:
# # #                     path0=menu[nodo_padre]['titulo']
# # #                     path1 = r['attributes']['titulo']
# # #                     path2 = r['attributes']['enlace_interno']['id']
# # #                     url= saniticzarUrl(f"{path0}/{path1}/{path2}")
# # #                 except:
# # #                     pass
# # #                 # 000000000000000000000000000000000000000000000000000000000000000
# # #                 # 000000000000000000000000000000000000000000000000000000000000000
# # #                 menu[nodo_padre]['submenu'][id]={
# # #                     "titulo":r['attributes']['titulo'],
# # #                     "nodo_padre":nodo_padre,
# # #                     "key": f"menu{id}",
# # #                     "url":url,
# # #                     "submenu":{}
# # #                 }
# # #                 # 000000000000000000000000000000000000000000000000000000000000000
# # #                 # 000000000000000000000000000000000000000000000000000000000000000
# # #             except:
# # #                 for m, sm  in menu.items():
# # #                     # print(sm["submenu"][nodo_padre]["titulo"])
# # #                     if nodo_padre in sm['submenu']:
# # #                         # menu[nodo_padre]
# # #                         # print(sm["titulo"])
# # #                         # print(sm["submenu"][nodo_padre]["titulo"])
# # #                         path0=sm["titulo"]
# # #                         path1=sm["submenu"][nodo_padre]["titulo"]
# # #                         path2 = r['attributes']['titulo']
# # #                         path3 = r['attributes']['enlace_interno']['id']
# # #                         url= saniticzarUrl(f"{path0}/{path1}/{path2}/{path3}")
# # #                         sm['submenu'][nodo_padre]['submenu'][id]={
# # #                             "titulo":r['attributes']['titulo'],
# # #                             "nodo_padre":nodo_padre,
# # #                             "key": f"menu{id}",
# # #                             "url": url, #None, # aqui debe llevar el url 
# # #                             "submenu":None,
# # #                         }
# # #             # opciones_submenu={}
# # #             # opciones_submenu['titulo']=r['attributes']['titulo']
# # #             # opciones_submenu['url']=nulo
# # #             # opciones_submenu['submenu']=[]
# # #             # menu[key]['submenu'].append(opciones_submenu)                    
# # #             # print(r['attributes']['titulo'])
# # #             # print(r['id'])
# # #             # primer_segmento=r['attributes']['titulo']

# # #         #     i=i+1   
# # #     # print(json.dumps(menu))
# # #     # config.data = json.dumps(menu) # esto seria valido para MYSQL
# # #     # config.data = menu # esto seria valido para sqlite 
# # #     # config.save()
# # #     # return  menu

# # #     # menu = json.dumps(menu)
# # #     # menu = json.load(menu)
# # #     return menu
# # #     # return  menu