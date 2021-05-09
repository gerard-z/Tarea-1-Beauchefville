""" Funciones para crear las distintas figuras de la escena """

import numpy as np
import math
from OpenGL.GL import *
import grafica.basic_shapes as bs
import grafica.easy_shaders as es
import grafica.transformations as tr
import grafica.scene_graph as sg
import sys, os.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

#Directorio de sprites
thisFilePath = os.path.abspath(__file__)
thisFolderPath = os.path.dirname(thisFilePath)
spritesDirectory = os.path.join(thisFolderPath,"sprites")

def createGPUShape(shape, pipeline):
    # Funcion Conveniente para facilitar la inicializacion de un GPUShape
    gpuShape = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuShape)
    gpuShape.fillBuffers(shape.vertices, shape.indices, GL_STATIC_DRAW)
    return gpuShape

def createTextureGPUShape(shape, pipeline, path,
                        sWrapMode=GL_CLAMP_TO_EDGE, tWrapMode=GL_CLAMP_TO_EDGE, minFilterMode=GL_NEAREST, maxFilterMode=GL_NEAREST,
                        boolMipmap=False):
    # Funcion Conveniente para facilitar la inicializacion de un GPUShape con texturas
    gpuShape = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuShape)
    gpuShape.fillBuffers(shape.vertices, shape.indices, GL_STATIC_DRAW)
    gpuShape.texture = es.textureSimpleSetup(
        path, sWrapMode, tWrapMode, minFilterMode, maxFilterMode)
    if boolMipmap:
        glGenerateMipmap(GL_TEXTURE_2D)
    return gpuShape

def createTree(pipeline):
    # se crea un tronco
    vertices = np.array([-0.5, -0.5, 0, 139/255, 69/255, 19/255,
                -0.3,  0.5, 0, 139/255, 69/255, 19/255,
                 0.3,  0.5, 0, 139/255, 69/255, 19/255,
                 0.5, -0.5, 0, 139/255, 69/255, 19/255,])
    indices = np.array([0, 1, 2, 0, 2, 3])

    dibujo = bs.Shape(vertices, indices)

    gpuTronco= createGPUShape(dibujo, pipeline)

    #Circulo verde
    circuloVerde = bs.createColorCircle(33, 0 , 0.8, 0)
    gpuCirculo = createGPUShape(circuloVerde, pipeline)

    #Tronco
    tronco = sg.SceneGraphNode("tronco")
    tronco.transform = tr.translate(0, -0.5, 0)
    tronco.childs += [gpuTronco]

    #Circulo 1
    circulo1 = sg.SceneGraphNode("circulo")
    circulo1.transform = tr.translate(0, 0.3, 0)
    circulo1.childs += [gpuCirculo]

    #Circulo 2
    circulo2 = sg.SceneGraphNode("circulo")
    circulo2.transform = tr.translate(-0.3, 0, 0)
    circulo2.childs += [gpuCirculo]

    #Circulo 3
    circulo3 = sg.SceneGraphNode("circulo")
    circulo3.transform = tr.translate(0.3, 0, 0)
    circulo3.childs += [gpuCirculo]

    #Hojas
    hojas = sg.SceneGraphNode("hojas")
    hojas.transform = tr.translate(0, 0.3, 0)
    hojas.childs += [circulo2, circulo3, circulo1]

    #Arbol
    tree = sg.SceneGraphNode("arbol")
    tree.transform = tr.uniformScale(0.5)
    tree.childs += [tronco, hojas]

    return tree

def createStreet(pipeline):
    cuadradoPlomo = bs.createColorQuad(0.2 , 0.2, 0.2)
    gpuCuadradoPlomo = createGPUShape(cuadradoPlomo, pipeline)

    franja = bs.createColorQuad(1, 1, 1)
    gpuFranja = createGPUShape(franja, pipeline)

    #Concreto
    concreto = sg.SceneGraphNode("concreto")
    concreto.transform = tr.scale(1, 2, 1)
    concreto.childs += [gpuCuadradoPlomo]

    #segmentos
    segmento = sg.SceneGraphNode("segmento")
    segmento.transform = tr.scale(0.05, 0.4, 1)
    segmento.childs += [gpuFranja]

    #vereda
    vereda = sg.SceneGraphNode("vereda")
    vereda.transform = tr.scale(0.1, 2, 1)
    vereda.childs += [gpuFranja]

    #Linea segmentada
    lineaSegmentada1 = sg.SceneGraphNode("linea segmentada")
    lineaSegmentada1.transform = tr.translate(0,-0.5,0)
    lineaSegmentada1.childs += [segmento]

    lineaSegmentada2 = sg.SceneGraphNode("linea segmentada")
    lineaSegmentada2.transform = tr.translate(0,0.5,0)
    lineaSegmentada2.childs += [segmento]

    #Linea de tránsito
    lineaTransito1 = sg.SceneGraphNode("Lineatransito1")
    lineaTransito1.transform = tr.identity()
    lineaTransito1.childs += [lineaSegmentada1, lineaSegmentada2]

    lineaTransito2 = sg.SceneGraphNode("Lineatransito2")
    lineaTransito2.transform = tr.identity()
    lineaTransito2.childs += [lineaSegmentada1, lineaSegmentada2]


    #vereda izquierda
    veredaIzq = sg.SceneGraphNode("vereda izquierda")
    veredaIzq.transform = tr.translate(-0.5, 0, 0)
    veredaIzq.childs += [vereda]

    #vereda derecha
    veredaDer = sg.SceneGraphNode("vereda derecha")
    veredaDer.transform = tr.translate(0.5, 0, 0)
    veredaDer.childs += [vereda]

    #Calle
    calle = sg.SceneGraphNode("calle")
    calle.transform= tr.identity()
    calle.childs +=[concreto, veredaIzq, veredaDer, lineaTransito1, lineaTransito2]

    return calle

def createBackground(pipeline):
    cuadradoVerde = bs.createColorQuad(0.2, 1, 0.2)
    gpuCuadradoVerde = createGPUShape(cuadradoVerde, pipeline)

    #arbol
    arbol = createTree(pipeline)

    #Calle
    calle = createStreet(pipeline)

    #arboles
    arbol1 = sg.SceneGraphNode("arbol1")
    arbol1.transform = tr.matmul([tr.translate(0, -0.65 , 0),tr.uniformScale(0.3)])
    arbol1.childs += [arbol]

    arbol2 = sg.SceneGraphNode("arbol3")
    arbol2.transform = tr.matmul([tr.translate(0, 0 , 0),tr.uniformScale(0.3)])
    arbol2.childs += [arbol]

    arbol3 = sg.SceneGraphNode("arbol5")
    arbol3.transform = tr.matmul([tr.translate(0, 0.65, 0),tr.uniformScale(0.3)])
    arbol3.childs += [arbol]

    #Hilera de arboles
    hilera = sg.SceneGraphNode("hilera")
    hilera.transform = tr.identity()
    hilera.childs += [arbol1, arbol2, arbol3]

    #fondo
    fondo = sg.SceneGraphNode("fondo")
    fondo.transform = tr.uniformScale(2)
    fondo.childs += [gpuCuadradoVerde]

    #Hileras de arboles
    hileraIzq = sg.SceneGraphNode("hileraIzq")
    hileraIzq.transform = tr.translate(-0.75,0,0)
    hileraIzq.childs += [hilera]

    hileraDer = sg.SceneGraphNode("hileraDer")
    hileraDer.transform = tr.translate(0.75,0,0)
    hileraDer.childs += [hilera]

    #Arboles
    arboles1 = sg.SceneGraphNode("arboles1")
    arboles1.transform = tr.identity()
    arboles1.childs += [hileraIzq, hileraDer]

    arboles2 = sg.SceneGraphNode("arboles2")
    arboles2.transform = tr.identity()
    arboles2.childs += [hileraIzq, hileraDer]

    #Background
    background = sg.SceneGraphNode("background")
    background.transform = tr.identity()
    background.childs = [fondo, arboles1, arboles2, calle]

    return background

def createTextureDoor():
    #Creating the door with vertices and index
    vertices = [
    #   positions        texture
        -0.3, -0.5, 0.0,  0, 1,
           0, -0.5, 0.0,  1, 1,
           0,  0.5, 0.0,  1, 0,
        -0.3,  0.5, 0.0,  0, 0,
         0.3,  0.5, 0.0,  0, 0,
         0.3, -0.5, 0.0,  0, 1] #Se aprovecha la simetría para crear una puerta doble a la tienda

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [
         0, 1, 2,
         2, 3, 0,
         2, 1, 4,
         1, 4, 5]
        
    return bs.Shape(vertices, indices)

def createTextureArch(N):
    """ int -> Shape
        Create a arch by a semi circle with N vertices, this function was maded thinking that the texture
        its a thin and long rectangle"""

    assert type(N)==int, "El número de intervalos debe ser entero"
    #vértices e índices del círculo
    vertices = np.zeros(N*5)
    indices = np.zeros(N*3)
    dtheta = np.pi/(N-2)
    vertices[0:5] = [0, 0, 0, 1, 0.5]

    for i in range(0, N-1, 2):
        theta = i * dtheta
        theta2 = (i+1) * dtheta
        j= (i+1)*5
        vertices[j:j+5] = [0.5 * np.cos(theta), 0.5 * np.sin(theta), 0, 0, 1]
        vertices[j+5:j+10] = [0.5 * np.cos(theta2), 0.5 * np.sin(theta2), 0, 0, 0]
        indices[i*3:i*3+6] = [0, i, i+1, 0, i+1, i+2]
    
    return bs.Shape(vertices, indices)

def createStore(pipeline):
    doorPath = os.path.join(spritesDirectory, "door.png")
    wallPath = os.path.join(spritesDirectory, "wood.png")
    windowPath = os.path.join(spritesDirectory, "window.png")
    lampPath = os.path.join(spritesDirectory, "lamp.png")
    ceilPath = os.path.join(spritesDirectory, "ceil.png")
    ceilBPath = os.path.join(spritesDirectory, "ceilb.png")
    signPath = os.path.join(spritesDirectory, "sign.png")

    
    doorTex = createTextureDoor()
    gpuDoorTex = createTextureGPUShape(doorTex, pipeline, doorPath, 
                                       GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)

    wallQuad = bs.createTextureQuad(3,1)
    gpuWallQuad = createTextureGPUShape(wallQuad, pipeline, wallPath,
                                        sWrapMode=GL_REPEAT, tWrapMode=GL_REPEAT)
    
    windowTex = bs.createTextureQuad(1,1)
    gpuWindowTex = createTextureGPUShape(windowTex, pipeline, windowPath)

    lampTex = bs.createTextureQuad(1,1)
    gpuLampTex = createTextureGPUShape(lampTex, pipeline, lampPath)

    ceilTex = bs.createTextureQuad(1,1)
    gpuCeilTex = createTextureGPUShape(ceilTex, pipeline, ceilPath,
                                       minFilterMode=GL_NEAREST, maxFilterMode=GL_NEAREST,
                                       boolMipmap=False)

    archTex = createTextureArch(27)
    gpuArchTex = createTextureGPUShape(archTex, pipeline, ceilBPath)

    signTex = bs.createTextureQuad(1,1)
    gpuSignTex = createTextureGPUShape(signTex, pipeline, signPath)

    #wall
    wall = sg.SceneGraphNode("wall")
    wall.transform = tr.scale(1.8,1,1)
    wall.childs += [gpuWallQuad]

    #door
    door = sg.SceneGraphNode("door")
    door.transform = tr.matmul([tr.translate(0.55, -0.25 ,0), tr.uniformScale(0.5)])
    door.childs += [gpuDoorTex]

    #window
    window1 = sg.SceneGraphNode("window")
    window1.transform = tr.matmul([tr.translate(-0.6,-0.1,0), tr.uniformScale(0.25)])
    window1.childs += [gpuWindowTex]

    window2 = sg.SceneGraphNode("window")
    window2.transform = tr.matmul([tr.translate(0.0,-0.1,0), tr.uniformScale(0.25)])
    window2.childs += [gpuWindowTex]

    #lamp
    lamp = sg.SceneGraphNode("lamp")
    lamp.transform = tr.matmul([tr.translate(0.55, 0.1, 0),tr.uniformScale(0.25)])
    lamp.childs += [gpuLampTex]

    #ceil
    ceil = sg.SceneGraphNode("ceil")
    ceil.transform = tr.matmul([tr.translate(0, 0.35, 0), tr.scale(2.2, 0.4, 1)])
    ceil.childs += [gpuCeilTex]

    #arch
    arch = sg.SceneGraphNode("arch")
    arch.transform = tr.matmul([tr.translate(0, 0.5, 0), tr.scale(1.8, 0.5, 1)])
    arch.childs += [gpuArchTex]

    #sign
    sign = sg.SceneGraphNode("sign")
    sign.transform = tr.matmul([tr.translate(0, 0.5, 0), tr.scale(0.9, 0.36, 1)])
    sign.childs += [gpuSignTex]

    #store
    store = sg.SceneGraphNode("store")
    store.transform = tr.matmul([tr.translate(-0.7,0.6,0), tr.rotation(np.pi/2), tr.uniformScale(0.4)])
    store.childs += [wall, door, window1, window2, lamp, ceil, arch, sign]


    return store

def createAnimatedSign(pipeline):
    storeSignPath = os.path.join(spritesDirectory, "Store sign.png")

    #Vertices
    vertices = [
    #   positions      
        -0.5, -0.5, 0.0,
         0.5, -0.5, 0.0,
         0.5,  0.5, 0.0,
        -0.5,  0.5, 0.0]

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [
         0, 1, 2,
         2, 3, 0]

    storeSignTex = bs.Shape(vertices, indices)
    gpuStoreSignTex = createTextureGPUShape(storeSignTex, pipeline, storeSignPath,
                                            sWrapMode=GL_CLAMP_TO_EDGE, tWrapMode=GL_CLAMP_TO_EDGE,
                                            minFilterMode=GL_LINEAR_MIPMAP_NEAREST, maxFilterMode=GL_NEAREST,
                                            boolMipmap=True)

    #store sign
    storeSign = sg.SceneGraphNode("storeSign")
    storeSign.transform = tr.matmul([tr.translate(-0.9, 0.61, 0), tr.rotation(np.pi/2), tr.scale(0.3, 0.12, 1)])
    storeSign.childs += [gpuStoreSignTex]

    return storeSign