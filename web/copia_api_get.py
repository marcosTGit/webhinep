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
        url=url.lower().replace(" ", "_")
        return url
    else:
        return url
    



# 000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000

# def leerJsonConvertirtojson(dato= None, path_archivo=ruta_archivo, accion="r"):
#     # Obtener la ruta absoluta
#     # print(ruta_archivo)
#     if accion=='w':
#         print("escribiendo json")
#         d=json.dumps(dato)
#         with open(path_archivo, accion) as f:
#             f.write(d)
#     if accion=='r':
#         print("leyendo json")
#         with open(path_archivo, accion) as f:
#             datos = json.load(f)
#         return datos





# 000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000

def getMenuPortalAPi():

    #VERIFICAMOS SI EXISTE AL RCHIVO Y SI FUE ACTUALIZADO HOY 
    # propiedades = os.stat(ruta_archivo) # Ruta al archivo JSON
    # fecha_creacion = time.ctime(propiedades.st_ctime) # Obtener las propiedades del archivo # Fecha de creación (solo en Windows, en otros sistemas muestra el tiempo de modificación)
    # fecha_modificacion = time.ctime(propiedades.st_mtime)# Fecha de última modificación
    # if fecha_modificacion == fecha_actual:
    #     # print("El archivo no fue creado hoy, debe actualizarse.")
    #     return obtenerMenu()
    #     else:
    #     #EL ARCHIVO EST ACTUALIZADO NO HACE FALTA ACTUALIZARLO
    #     # Imprimir el contenido
    #     return obtenerMenu()
    #     # return leerJsonConvertirtojson()
    # except:
    #     # SI SE PRODUCE U NERRO ES POR QUE EL ARCHIVO EXISTE
    #     return obtenerMenu()

    return obtenerMenu()




# 000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000

def obtenerMenu():
    fecha_actual = date.today()
    l
    # print("0000000000000000000000000000000000000000000000000000000000000000000000000000000")
    # print("0000000000000000000000000000000000000000000000000000000000000000000000000000000")
    # print("0000000000000000000000000000000000000000000000000000000000000000000000000000000")
    # print("0000000000000000000000000000000000000000000000000000000000000000000000000000000")
    # print("0000000000000000000000000000000000000000000000000000000000000000000000000000000")
    config, created = Configuracion.objects.get_or_create(
        nombre='menu',  # Campos de búsqueda (deben ser únicos o parte de una combinación única)
        # data=menu  # Valores por defecto si se crea
    )
    
    if not created and (config.registro_actualizado).date() < fecha_actual:
        #TENEMOS QUE ACTUALIZAR EL MENU 
        url="https://api-portal.catamarca.gob.ar/api/v1/cms/menu/?organismo_id=300&include=organismo"
        res = requests.get(url)
        try:
            response = json.loads(res.text)
            primer_segmento = ""
            segundo_segmento = ""
            i=1     # menu
            j=0     # submenu
            k=0     # seccion de submenu
            menu=[]
            #voy a agregar la agregar foto en el menu
            # data={'data':{'logo': "*"}}
            data={'data':{'logo': response['included'][0]['attributes']['logo']}}
            menu.append(data)
            # nulo=None  # Valido para sqlite
            nulo=False  # Valido para mysql
            for r in response['data']:  
                opcion={}

                if r['attributes']['tipo_enlace']=="submenu" and r['attributes']['titulo']:
                    print("0000000000000000000000000000000000000000")
                    print(r['attributes']['titulo'])
                    primer_segmento=r['attributes']['titulo']
                    opcion['titulo']=r['attributes']['titulo']
                    opcion['url']=nulo
                    opcion['submenu']=[]

                    j=0
                    key=i
                elif r['relationships']['nodo_padre']['data']:
                    opciones_submenu={}
                    opciones_submenu['titulo']=r['attributes']['titulo']
                    opciones_submenu['url']=nulo
                    opciones_submenu['submenu']=[]
                    menu[key]['submenu'].append(opciones_submenu)
                    
                    u=f"https://api-portal.catamarca.gob.ar/api/v1/cms/seccion/?pagina_id={r['attributes']['enlace_interno']['id']}&include=contenidos"
                    ressponse_smenu=requests.get(u)
                    submenu= json.loads(ressponse_smenu.text)
                    
                    k=0
                    for sm in submenu['included']:
                        try:
                            segundo_segmento = f"{r['attributes']['titulo']}/{sm['attributes']['componente']['attributes']['enlace_interno']['id']}"
                            seccion={}
                            seccion['titulo']=sm['attributes']['componente']['attributes']['titulo']
                            seccion['url']=saniticzarUrl(f"/{primer_segmento}/{segundo_segmento}")
                            seccion['submenu']=nulo
                            menu[key]['submenu'][j]['submenu'].append(seccion)
                            k=k+1
                        except:
                            segundo_segmento = f"{r['attributes']['titulo']}/{sm['relationships']['seccion']['data']['id']}"
                        
                    if k==0:
                        segundo_segmento = f"{r['attributes']['titulo']}/{r['attributes']['enlace_interno']['id']}"
                        menu[key]['submenu'][j]['url']=saniticzarUrl(f"/{primer_segmento}/{segundo_segmento}")
                        menu[key]['submenu'][j]['submenu']=nulo
                        # print(r['attributes']['enlace_interno']['id']) # DEPURACION
                    j=j+1
                if opcion:
                    print("agrega")
                    menu.append(opcion)
                    i=i+1   
            print("0000000000000000000000000000000000000000000000000000000000000000000000000000000000000")
            print("0000000000000000000000000000000000000000000000000000000000000000000000000000000000000")
            print(menu)
            print("0000000000000000000000000000000000000000000000000000000000000000000000000000000000000")
            print("0000000000000000000000000000000000000000000000000000000000000000000000000000000000000")
            print(json.dumps(menu))
            print("0000000000000000000000000000000000000000000000000000000000000000000000000000000000000")
            print("0000000000000000000000000000000000000000000000000000000000000000000000000000000000000")
            config.data = json.dumps(menu) # esto seria valido para MYSQL
            config.data = menu # esto seria valido para sqlite 
            config.save()
            print("Se actualizó el registro existente.")
            # leerJsonConvertirtojson(menu, ruta_archivo, "w") # convierte a json 
            # return json.loads(menu)
            return config.data
        except:
            print("Se PRODUJO UN ERROR PERO IGUAL OBTENEMO EL MENU ALMACENADO EN LA BASE")
            config = Configuracion.objects.get(nombre='menu')
            return  config.data
    else:
        return  config.data

        




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
            if datos['included'][0]['attributes']['componente']['attributes']['texto']:
                html_content = datos['included'][0]['attributes']['componente']['attributes']['texto']
                soup = BeautifulSoup(html_content, 'html.parser')
                images = soup.find_all('img') # busca todoas la etqieuta img 
                datos['included'][0]['attributes']['componente']['attributes']['imagenes'] = [img['src'] for img in images if 'src' in img.attrs] # extraigo los url de todas la etiquetas img encontradas 
                soup.img.extract() # extraigo la etiqueta img si encuentra
                for img in soup.find_all('img'):
                    img.extract()
                datos['included'][0]['attributes']['componente']['attributes']['texto']= soup.prettify()
                
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
