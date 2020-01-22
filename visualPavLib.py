import cv2
import os
from xml.etree import ElementTree
from xml.dom import minidom
import random
import matplotlib.pyplot as plt
import collections
import matplotlib as matplot
import seaborn as sns


def contar_fallas(vias,codigos_falla):
    #################################################################
    # recibe una lista de carpetas de los proyectos a procesar (vias) y la lista de codigos de falla
    # calcula el numero total de imagenes a procesar y el numero total de etiquetas en esas imagenes
    # Realiza un grafico de barras de las fallas y su ocurrencia
    # retorna una lista con el conteo de cada falla
    #################################################################
    codigos_encontrados = []  # etiquetas encontradas en la base de datos
    total_imagenes = 0        # El numero total de imagenes
    #Ruta del archivo donde se encuentra la base de datos
    ruta = os.getcwd() + '/base_datos/'
    #se recorren las carpetas de vias 
    for via in vias:
        #genera una lista de los archivos existentes en la carpeta de Etiquetas
        lista_archivos = [filename for filename in os.listdir(ruta + via + '/Etiquetas/') if not filename.startswith('.')]
        #se recorren los archivos dentro de la carpeta  
        for archivo in lista_archivos:
            total_imagenes = total_imagenes + 1 #lleva la cuenta de los archivos procesados
            if archivo =='.DS_Store':
                pass #si es un archivo del sistema no haga nada
            else:
                #Leer el archivo xml 
                archivo_xml = open(ruta + via + '/Etiquetas/' +archivo)
                arbol = ElementTree.parse(archivo_xml)
                raiz = arbol.getroot()
                #Se recorre cada objeto dentro del xml
                for obj in raiz.iter('object'):
                    codigo = obj.find('name').text
                    codigos_encontrados.append(codigo) #se agrega el codigo de la falla al final de la lista
    print("Numero Total de Imagenes：" + str(total_imagenes))
    print("Numero Total de Etiquetas：" + str(len(codigos_encontrados)))

    #diccionario de codigo de falla y su numero de ocurrencias 
    dicci_conteo = collections.Counter(codigos_encontrados) 
    conteo_falla = [] #conteo de ocurrencias por cada falla
    #se recorren la lista de los codigos de falla 
    for codigo in codigos_falla:
        print(str(codigo) + ' : ' + str(dicci_conteo[codigo]))
        conteo_falla.append(dicci_conteo[codigo]) 
    #Grafico de Barras   
    plt.subplots(figsize=(12, 4))
    miColor=['darkgoldenrod','lemonchiffon','ivory','olive', 'yellowgreen','lawngreen','lightgreen','g','mediumseagreen','mediumaquamarine']
    plt.bar(codigos_falla, conteo_falla,color=miColor,edgecolor='white')
    plt.xlabel('Codigos de Falla', fontsize=15); plt.ylabel('Etiquetas por Falla', fontsize=15,rotation=90)
    plt.show()  
    return conteo_falla


def graficar_imagen_etiquetada(ruta_img):
    #################################################################
    # Recibe la ruta de una imagen
    # Dibuja la imagen y sus etiquetas
    # retorna el archivo de la imagen dibujando las etiquetas 
    #################################################################
    #Ruta del archivo donde se encuentra la base de datos
    ruta = os.getcwd() + '/base_datos/'
    #Cargar la imagen
    img = cv2.imread(ruta_img)
    #Generar la ruta del directorio donde se encuentran las etiquetas
    ruta_eti=(ruta+ruta_img.split('/')[-3]+'/Etiquetas/'+ruta_img.split('/')[-1].rstrip('.JPG').rstrip('.jpg').rstrip('.jpeg').rstrip('.PNG').rstrip('.png')+'.xml')
    #Leer el archivo xml que corresponde a la imagen
    archivo_xml = open(ruta_eti)
    arbol = ElementTree.parse(archivo_xml)
    raiz = arbol.getroot()
    #Se recorre cada objeto dentro del xml
    for obj in raiz.iter('object'):
        codigo = obj.find('name').text
        limites = obj.find('bndbox')
        xmin = int(limites.find('xmin').text)
        xmax = int(limites.find('xmax').text)
        ymin = int(limites.find('ymin').text)
        ymax = int(limites.find('ymax').text)
        #Elegir color aleatorio
        #color = [random.randint(0,255) for i in range(3)] 
        color = [0,random.randint(0,255),random.randint(0,255)] 
        # Agregar Rectangulo
        cv2.rectangle(img, (xmin, ymin), (xmax, ymax), color,6,cv2.LINE_8,0)
        #cv2.rectangle(imagen, puntoInicio,puntoFinal,color,grueso,tipoLinea,shifft)
        # Agregar texto
        cv2.putText(img,codigo,(xmin,ymin-10),cv2.FONT_HERSHEY_DUPLEX,2,color,4,cv2.LINE_AA,0)
        #cv2.putText(imagen,texto,coordenadas,fuente,tamaño,color,grueso,tipoLinea,inverso)
    plt.imshow(img)        
    return img


def recortar_imagen(ruta_img):
    #################################################################
    # Recibe la ruta de una imagen
    # Grafica la imagen y las subimagenes de las etiquetas
    # Guarda las subimagenes en el directorio correspondiente 
    #################################################################
    #Ruta del archivo donde se encuentra la base de datos
    ruta = os.getcwd() + '/base_datos/'
    #Cargar la imagen
    img = cv2.imread(ruta_img)
    #Generar la ruta del directorio donde se encuentran las etiquetas
    ruta_eti=(ruta+ruta_img.split('/')[-3]+'/Etiquetas/'+ruta_img.split('/')[-1].rstrip('.JPG').rstrip('.jpg').rstrip('.jpeg').rstrip('.PNG').rstrip('.png')+'.xml')
    #Leer el archivo xml que corresponde a la imagen
    archivo_xml = open(ruta_eti)
    arbol = ElementTree.parse(archivo_xml)
    raiz = arbol.getroot()
    #Se recorre cada objeto dentro del xml
    for obj in raiz.iter('object'):
        codigo = obj.find('name').text
        limites = obj.find('bndbox')
        xmin = int(limites.find('xmin').text)
        xmax = int(limites.find('xmax').text)
        ymin = int(limites.find('ymin').text)
        ymax = int(limites.find('ymax').text)
        #Elegir color aleatorio
        #color = [random.randint(0,255) for i in range(3)] 
        color = [0,random.randint(0,255),random.randint(0,255)] 
        # Agregar Rectangulo
        cv2.rectangle(img, (xmin, ymin), (xmax, ymax), color,5,cv2.LINE_8,0)
        #cv2.rectangle(imagen, puntoInicio,puntoFinal,color,grueso,tipoLinea,shifft)
        # Agregar texto
        cv2.putText(img,codigo,(xmin+10,ymin+30),cv2.FONT_HERSHEY_DUPLEX,1,color,1,cv2.LINE_AA,0)
        #cv2.putText(imagen,texto,coordenadas,fuente,tamaño,color,grueso,tipoLinea,inverso)
        aux=0
        plt.subplots()
        img_recortada=img[ymin+aux:ymax-aux,xmin+aux:xmax-aux,0:3]
        plt.imshow(img_recortada) 
        #ruta para guardar la imagen recortada
        dir_guardar=(ruta+'otrasImag/'+codigo) 
        #crea el directorio si no existe
        os.makedirs(dir_guardar, exist_ok=True)
        
        #genera una lista de los archivos existentes en la carpeta para despues agregar el siguiente en orden consecutivo 
        lista_archivos = [filename for filename in os.listdir(dir_guardar) if not filename.startswith('.')]
        #genera una lista con solo los numeros de los archivos
        lista = [int(lista_archivos[i].rstrip('.JPG').split('_')[-1]) for i in range(len(lista_archivos))] 
        lista.sort()
        if lista_archivos == [] :
            #si la carpeta esta vacia es la primera imagen que se guarda
            ruta_guardar=(dir_guardar+'/'+codigo+'_'+ '1.JPG') 
        else: 
            #si no, se extrae el numero mas alto y se guarda la nueva imagen con el siguiente numero
            ruta_guardar=(dir_guardar+'/'+codigo+'_'+ str(lista[-1]+1)+'.JPG') 
        #Guarda la imagen recortada
        cv2.imwrite(ruta_guardar,img_recortada)
    plt.subplots()
    plt.imshow(img)    
    return 


def recortar_imagenes(vias,ruta):
    #################################################################
    # recibe una lista de carpetas de los proyectos a procesar (vias)
    # recibe la ruta del archivo donde se encuentra la base de datos
    # Guarda las subimagenes en el directorio correspondiente 
    #################################################################
    #Ruta del archivo donde se encuentra la base de datos
    #ruta = os.getcwd() + '/base_datos/'
    #se recorren las carpetas de vias 
    for via in vias:
        #genera una lista de los archivos existentes en la carpeta de Imagenes 
        lista_archivos = [filename for filename in os.listdir(ruta + via+'/Imagenes') if not filename.startswith('.')]
        #se recorren los archivos dentro de la carpeta    
        for archivo in lista_archivos:
            if archivo =='.DS_Store':
                pass #si es un archivo del sistema no haga nada
            else:
                #Ruta de la imagen que se va a procesar
                ruta_img = (ruta + via+'/Imagenes/'+archivo)
                #Ruta de la etiqueta que le corresponde a esa imagen
                ruta_eti=(ruta+via+'/Etiquetas/'+archivo.rstrip('.JPG').rstrip('.jpg').rstrip('.jpeg').rstrip('.PNG').rstrip('.png')+'.xml')
                #Leer la imagen
                img = cv2.imread(ruta_img)
                #Leer el archivo xml que corresponde a la imagen
                archivo_xml = open(ruta_eti)
                arbol = ElementTree.parse(archivo_xml)
                raiz = arbol.getroot()
                #Se recorre cada objeto dentro del xml
                for obj in raiz.iter('object'):
                    codigo = obj.find('name').text
                    limites = obj.find('bndbox')
                    xmin = int(limites.find('xmin').text)
                    xmax = int(limites.find('xmax').text)
                    ymin = int(limites.find('ymin').text)
                    ymax = int(limites.find('ymax').text)
        
                    '''#Elegir color aleatorio
                    #color = [random.randint(0,255) for i in range(3)] 
                    color = [0,random.randint(0,255),random.randint(0,255)] 
                    # Agregar Rectangulo
                    cv2.rectangle(img, (xmin, ymin), (xmax, ymax), color,5,cv2.LINE_8,0)
                    #cv2.rectangle(imagen, puntoInicio,puntoFinal,color,grueso,tipoLinea,shifft)
                    # Agregar texto
                    cv2.putText(img,codigo,(xmin+10,ymin+30),cv2.FONT_HERSHEY_DUPLEX,1,color,1,cv2.LINE_AA,0)
                    #cv2.putText(imagen,texto,coordenadas,fuente,tamaño,color,grueso,tipoLinea,inverso)'''
        
                    aux=0
                    img_recortada=img[ymin+aux:ymax-aux,xmin+aux:xmax-aux,0:3]
                    #ruta para guardar la imagen recortada
                    dir_guardar=(ruta+'TotalImag/'+codigo) 
                    #crea el directorio si no existe
                    os.makedirs(dir_guardar, exist_ok=True)
        
                    #genera una lista de los archivos existentes en la carpeta 
                    lista_archivos_train = [filename for filename in os.listdir(dir_guardar) if not filename.startswith('.')]
                    #genera una lista con solo los numeros de los archivos
                    lista = [int(lista_archivos_train[i].rstrip('.JPG').split('_')[-1]) for i in range(len(lista_archivos_train))] 
                    lista.sort()
                    if lista_archivos_train == [] :
                        #si la carpeta esta vacia es la primera imagen que se guarda
                        ruta_guardar=(dir_guardar+'/'+codigo+'_'+ '1.JPG') 
                    else: 
                        #si no, se saca el numero mas alto y se guarda la nueva imagen con el siguiente numero
                        ruta_guardar=(dir_guardar+'/'+codigo+'_'+ str(lista[-1]+1)+'.JPG') 
                    #Guarda la imagen recortada
                    cv2.imwrite(ruta_guardar,img_recortada)
    return
    
    
def BorrarCarpetaConArchivos(ruta):
    #################################################################
    # Borrar la carpeta especificada en la ruta y los archivos que contiene
    #################################################################
    from shutil import rmtree
    rmtree(ruta)
    print("Eliminado：" + str(ruta))  
    return


def CopiarCarpeta(ruta1,ruta2):
    #################################################################
    # Copiar una Carpeta, con sus subcarpetas y los archivos que contiene
    #################################################################
    import shutil
    from shutil import copytree
    copytree(ruta1,ruta2)
    print("Copiado：" + str(ruta1))  
    return


def DividirImagenesParaEntrenar(ruta,limInf,pval,ptest):
    #################################################################
    # hace copias de las imagenes en la ruta especificada 
    # selecciona las carpetas que tienen mas de LimInf imagenes
    # las divide %validacion(pval) %test(ptest)  y el restante para train
    #################################################################
    from math import ceil
    from os import makedirs
    import shutil 
    #genera una lista de las carpetas existentes en la ruta
    lista_carpetas = [filename for filename in os.listdir(ruta+'TotalImag/') if not filename.startswith('.')]
    for carpeta in lista_carpetas:
        #genera una lista de los archivos existentes en la carpeta de Etiquetas
        lista_archivos = [filename for filename in os.listdir(ruta+'TotalImag/'+ carpeta) if not filename.startswith('.')]
        aux2=0;
        if len(lista_archivos)>limInf:
            #se recorren los archivos dentro de la carpeta  
            for archivo in lista_archivos:
                if archivo =='.DS_Store':
                    pass #si es un archivo del sistema no haga nada
                elif aux2<(ceil(len(lista_archivos)*pval/100)): 
                    os.makedirs(ruta+"validacion/"+carpeta, exist_ok=True) #crea los directorios si no existen
                    shutil.copy(ruta+'TotalImag/'+carpeta+'/'+archivo, ruta+"validacion/"+carpeta+'/'+archivo)                    
                    #print("moviendo"+ruta+'TotalImag/'+carpeta+'/'+archivo) 
                elif aux2>=(ceil(len(lista_archivos)*pval/100)) and aux2<(ceil(len(lista_archivos)*(pval+ptest)/100)):
                    os.makedirs(ruta+"test/"+carpeta, exist_ok=True) #crea los directorios si no existen
                    shutil.copy(ruta+'TotalImag/'+carpeta+'/'+archivo, ruta+"test/"+carpeta+'/'+archivo)                    
                else:
                    os.makedirs(ruta+"train/"+carpeta, exist_ok=True) #crea los directorios si no existen
                    shutil.copy(ruta+'TotalImag/'+carpeta+'/'+archivo, ruta+"train/"+carpeta+'/'+archivo)
                aux2=aux2+1
        else:
            #se recorren los archivos dentro de la carpeta  
            for archivo in lista_archivos:
                os.makedirs(ruta+"menos_del_limite/"+carpeta, exist_ok=True) #crea los directorios si no existen
                shutil.copy(ruta+'TotalImag/'+carpeta+'/'+archivo, ruta+"menos_del_limite/"+carpeta+'/'+archivo)
    return


def contar_Imagenes(ruta):
    #################################################################
    # para contar las imagenes con las que se va a entrenar
    # Cuenta los archivos de las subcarpetas de nivel 1 de la ruta
    # retorna el numero de archivos
    #################################################################
    import os
    total_imagenes = 0 
    #genera una lista de las carpetas existentes en la ruta
    lista_carpetas = [filename for filename in os.listdir(ruta) if not filename.startswith('.')]
    #recorre cada carpeta en la lista
    for carpeta in lista_carpetas:
        #cuenta los archivos existentes en cada carpeta y los va acumulando
        total_imagenes = total_imagenes+ len([filename for filename in os.listdir(ruta + '/'+ carpeta) if not filename.startswith('.')])
    return total_imagenes


def nombre_etiqueta(ruta):
    #################################################################
    # Retorna un arreglo con los nombres de las etiquetas del conjunto de entrenamiento
    #################################################################
    import os
    import numpy as np
    #genera una lista de las carpetas existentes en la ruta
    lista_carpetas = [filename for filename in os.listdir(ruta) if not filename.startswith('.')]
    #crea un arreglo con los nombres de las etiquetas
    CLASE_NOMBRE = np.array(lista_carpetas)
    return CLASE_NOMBRE


def TamanoImagenes(ruta):
    #################################################################
    # Retorna una lista con los tamaños de las imagenes con las que se va a entrenar
    # tiene en cuenta los archivos de las subcarpetas de nivel 1 de la ruta
    #################################################################
    import cv2
    import matplotlib.pyplot as plt
    import collections
    import os
    T=[] #variable para guardar los tamaños originales
    #genera una lista de las carpetas existentes en la ruta
    lista_carpetas = [filename for filename in os.listdir(ruta) if not filename.startswith('.')]
    #recorre cada carpeta en la lista
    for carpeta in lista_carpetas:
        #genera una lista de los archivos existentes en cada carpeta 
        lista_archivos = [filename for filename in os.listdir(ruta +'/'+carpeta) if not filename.startswith('.')]
        #se recorren los archivos dentro de la carpeta  
        for archivo in lista_archivos:
            img = cv2.imread(ruta +'/'+carpeta+'/'+archivo) #lee cada imagen 
            T.append(img.shape[:2])  #guarda los tamaños originales en la lista T
    #a=[(T[x][0]-(T[x][0]%10),T[x][1]-(T[x][1]%10)) for x in range(len(T))] #organiza el tamaño de 10 en 10
    a=[((T[x][0]//100)*100,(T[x][1]//100)*100) for x in range(len(T))] #organiza el tamaño de 100 en 100
    filas=[(a[x][0]) for x in range(len(a))] #Separa los tamaños de las filas
    columnas=[(a[x][1]) for x in range(len(a))]  #Separa los tamaños de las columnas
    filas_conteo = collections.Counter(filas) 
    columnas_conteo = collections.Counter(columnas) 
    print('Tamaño de filas: ',filas_conteo)
    print('Tamaño de columnas: ',columnas_conteo)
    return a