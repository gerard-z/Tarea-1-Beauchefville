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

storeSpritesDirectory = os.path.join(spritesDirectory, "store")

doorPath = os.path.join(storeSpritesDirectory, "door.png")
wallPath = os.path.join(storeSpritesDirectory, "wood.png")
windowPath = os.path.join(storeSpritesDirectory, "window.png")
lampPath = os.path.join(storeSpritesDirectory, "lamp.png")
ceilPath = os.path.join(storeSpritesDirectory, "ceil.png")
ceilBPath = os.path.join(storeSpritesDirectory, "ceilb.png")
signPath = os.path.join(storeSpritesDirectory, "sign.png")
storeSignPath = os.path.join(storeSpritesDirectory, "Store sign.png")

hinataSpritesDirectory = os.path.join(spritesDirectory, "hinata")

hinataFrontPath = os.path.join(hinataSpritesDirectory, "hinataFront.png")
hinataBackPath = os.path.join(hinataSpritesDirectory, "hinataBack.png")
hinataSidePath = os.path.join(hinataSpritesDirectory, "hinataSide.png")

zombieSpritesDirectory = os.path.join(spritesDirectory, "zombie")
zombiePath = os.path.join(zombieSpritesDirectory, "zombie.png")

humanoSpritesDirectory = os.path.join(spritesDirectory, "humano")
humanoPath = os.path.join(humanoSpritesDirectory, "humano.png")

def createGPUShape(shape, pipeline):
    # Funcion Conveniente para facilitar la inicializacion de un GPUShape
    gpuShape = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuShape)
    gpuShape.fillBuffers(shape.vertices, shape.indices, GL_STATIC_DRAW)
    return gpuShape

def createGPUShapeStream(shape, pipeline):
    # Función conveniente para facilitar la inicialización de un GPUShape con vértices dinámicos
    gpuShape = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuShape)
    gpuShape.fillBuffers(shape.vertices, shape.indices, GL_STREAM_DRAW)
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

def createHinata(pipeline):
    hinataShape = bs.createSimpleQuad()
    bs.scaleVertices(hinataShape, 3, np.array([0.2,0.2,0.2]))
    gpuHinata = createTextureGPUShape(hinataShape, pipeline, hinataFrontPath)

    hinata = sg.SceneGraphNodeMultiPipeline("hinata", [pipeline], 0)
    hinata.childs += [gpuHinata]

    return hinata

def createZombie(pipeline):
    zombieShape = bs.createSimpleQuad()
    bs.scaleVertices(zombieShape, 3, np.array([0.2,0.2,0.2]))
    gpuZombie = createTextureGPUShape(zombieShape, pipeline, zombiePath)

    zombie = sg.SceneGraphNodeMultiPipeline("zombie", [pipeline], 2)
    zombie.childs += [gpuZombie]

    return zombie

def createHumano(pipeline, status):
    humanoShape = bs.createSimpleQuad()
    bs.scaleVertices(humanoShape, 3, np.array([0.2,0.2,0.2]))
    gpuHumano = createTextureGPUShape(humanoShape, pipeline, humanoPath)

    humano = sg.SceneGraphNodeMultiPipeline("humano", [pipeline], status)
    humano.childs += [gpuHumano]

    return humano

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

    lineaSegmentada2 = sg.SceneGraphNode("linea segmentada2")
    lineaSegmentada2.transform = tr.translate(0,0.5,0)
    lineaSegmentada2.childs += [segmento]

    lineaSegmentada3 = sg.SceneGraphNode("linea segmentada3")
    lineaSegmentada3.transform = tr.translate(0,1.5,0)
    lineaSegmentada3.childs += [segmento]

    #Linea de tránsito
    lineaTransito1 = sg.SceneGraphNode("Lineatransito1")
    lineaTransito1.transform = tr.identity()
    lineaTransito1.childs += [lineaSegmentada1, lineaSegmentada2]

    lineaTransito2 = sg.SceneGraphNode("Lineatransito2")
    lineaTransito2.transform = tr.identity()
    lineaTransito2.childs += [lineaSegmentada1, lineaSegmentada2, lineaSegmentada3]


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

    arbol2 = sg.SceneGraphNode("arbol2")
    arbol2.transform = tr.matmul([tr.translate(0, 0 , 0),tr.uniformScale(0.3)])
    arbol2.childs += [arbol]

    arbol3 = sg.SceneGraphNode("arbol3")
    arbol3.transform = tr.matmul([tr.translate(0, 0.65, 0),tr.uniformScale(0.3)])
    arbol3.childs += [arbol]

    arbol4 = sg.SceneGraphNode("arbol4")
    arbol4.transform = tr.matmul([tr.translate(0.75, 1.15, 0),tr.uniformScale(0.3)])
    arbol4.childs += [arbol]

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
    arboles2.childs += [hileraIzq, hileraDer, arbol4]

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

def createStore(pipeline):
    
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

    archTex = bs.createTextureArch(27)
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
    
    Store = sg.SceneGraphNode("Store")
    Store.transform = tr.identity()
    Store.childs += [store]


    return Store

def createAnimatedSign(pipeline):

    storeSignTex = bs.createSimpleQuad()
    gpuStoreSignTex = createTextureGPUShape(storeSignTex, pipeline, storeSignPath,
                                            sWrapMode=GL_CLAMP_TO_EDGE, tWrapMode=GL_CLAMP_TO_EDGE,
                                            minFilterMode=GL_LINEAR_MIPMAP_NEAREST, maxFilterMode=GL_NEAREST,
                                            boolMipmap=True)

    #store sign
    storeSign = sg.SceneGraphNode("storeSign")
    storeSign.transform = tr.matmul([tr.translate(-0.9, 0.61, 0), tr.rotation(np.pi/2), tr.scale(0.3, 0.12, 1)])
    storeSign.childs += [gpuStoreSignTex]

    StoreSign = sg.SceneGraphNode("StoreSign")
    StoreSign.transform = tr.identity()
    StoreSign.childs += [storeSign]

    return StoreSign

def createDetails(pipeline):
    greenLine = bs.createZicZacLineStrip(5, 0.2, 0, 0.5, 0)
    gpuGreenLine = createGPUShape(greenLine, pipeline)

    brownLine = bs.createZicZacLineStrip(20, 0.05, 169/255, 99/255, 49/255)
    gpuBrownLine = createGPUShape(brownLine, pipeline)

    blackSpiral = bs.createSpiralLineStrip(30, 3, 0, 0, 0)
    gpuBlackSpiral = createGPUShape(blackSpiral, pipeline)

    #Grass
    grass = sg.SceneGraphNode("grass")
    grass.transform = tr.uniformScale(0.1)
    grass.childs += [gpuGreenLine]

    grass1 = sg.SceneGraphNode("grass1")
    grass1.transform = tr.translate(-0.05, -0.75 , 0)
    grass1.childs += [grass]

    grass2 = sg.SceneGraphNode("grass2")
    grass2.transform = tr.translate(-0.05, -0.1 , 0)
    grass2.childs += [grass]

    grass3 = sg.SceneGraphNode("grass3")
    grass3.transform = tr.translate(-0.05, 0.55 , 0)
    grass3.childs += [grass]

    #Grass group
    grassGroup = sg.SceneGraphNode("grassGroup")
    grassGroup.transform = tr.identity()
    grassGroup.childs += [grass1, grass2, grass3]

    grassGroup1 = sg.SceneGraphNode("grassGroup1")
    grassGroup1.transform = tr.translate(0.1, 0.05, 0)
    grassGroup1.childs += [grass1, grass2, grass3]

    grassGroup2 = sg.SceneGraphNode("grassGroup1")
    grassGroup2.transform = tr.translate(0.05, -0.1, 0)
    grassGroup2.childs += [grass1, grass2, grass3]

    GrassGroup1 = sg.SceneGraphNode("grassGroup2")
    GrassGroup1.transform = tr.translate(-0.75, -0.2, 0)
    GrassGroup1.childs += [grassGroup, grassGroup1, grassGroup2]

    GrassGroup2 = sg.SceneGraphNode("grassGroup3")
    GrassGroup2.transform = tr.translate(0.75, -0.2, 0)
    GrassGroup2.childs += [grassGroup, grassGroup1, grassGroup2]

    #Log
    log1 = sg.SceneGraphNode("log1")
    log1.transform = tr.matmul([tr.rotation(np.pi/2-0.1), tr.uniformScale(0.5)])
    log1.childs += [gpuBrownLine]

    log2 = sg.SceneGraphNode("log2")
    log2.transform = tr.matmul([tr.translate(0.2, 0, 0), tr.reflectionY()])
    log2.childs += [log1]

    log = sg.SceneGraphNode("log")
    log.transform = tr.matmul([tr.translate(-0.1, 0, 0), tr.uniformScale(0.2)])
    log.childs += [log1, log2]

    Log1 = sg.SceneGraphNode("Log1")
    Log1.transform = tr.translate(0, -0.7, 0)
    Log1.childs += [log]

    Log2 = sg.SceneGraphNode("Log2")
    Log2.transform = tr.translate(0, -0.05, 0)
    Log2.childs += [log]

    Log3 = sg.SceneGraphNode("Log3")
    Log3.transform = tr.translate(0, 0.6, 0)
    Log3.childs += [log]

    Log4 = sg.SceneGraphNode("Log4")
    Log4.transform = tr.translate(0.83, 1.07, 0)
    Log4.childs += [log]

    #Log group
    logGroup1 = sg.SceneGraphNode("logGroup")
    logGroup1.transform = tr.translate(-0.67,-0.03,0)
    logGroup1.childs = [Log1, Log2, Log3]

    logGroup2 = sg.SceneGraphNode("logGroup")
    logGroup2.transform = tr.translate(0.83,-0.03,0)
    logGroup2.childs = [Log1, Log2, Log3]

    #scratch
    scratch1 = sg.SceneGraphNode("scratch")
    scratch1.transform = tr.matmul([tr.translate(0.4,0.3,0), tr.uniformScale(0.1)])
    scratch1.childs += [gpuBlackSpiral]

    scratch2 = sg.SceneGraphNode("scratch")
    scratch2.transform = tr.matmul([tr.translate(-0.2,0.6,0), tr.uniformScale(0.1)])
    scratch2.childs += [gpuBlackSpiral]

    #decorations
    decoration1 = sg.SceneGraphNode("decoration1")
    decoration1.transform = tr.identity()
    decoration1.childs += [GrassGroup1, GrassGroup2, logGroup1, logGroup2, scratch1]

    decoration2 = sg.SceneGraphNode("decoration2")
    decoration2.transform = tr.identity()
    decoration2.childs += [GrassGroup1, GrassGroup2, logGroup1, logGroup2, scratch2, Log4]

    decorations = sg.SceneGraphNode("decorations")
    decorations.transform = tr.identity()
    decorations.childs += [decoration1, decoration2]


    return decorations

def YouWingpu(pipeline):
    """ pipeline - > gpuShape 
    Crea la figura que corresponderá a las letras YOU WIN"""
    # Primero escribimos los vértices fijos de las letras y el cuado borde
    # Y amarillo
    (r, g, b) = (0, 1, 1)
    Yv = [-0.5, 0.35, 0, r, g, b,
        -0.45, 0.4, 0, r, g, b,
        -0.4, 0.3, 0, r, g, b,
        -0.45, 0.1, 0, r, g, b,
        -0.35, 0.1, 0, r, g, b,
        -0.35, 0.4, 0, r, g, b,
        -0.3, 0.35, 0, r, g, b]

    Yi = [0, 1, 2,
        3, 4, 2,
        5, 6, 2]

    # 7 vertices para Y, índice hata el 6
    # Letra O
    (r, g, b) = (0, 1, 0)
    Ov = [-0.2, 0.4, 0, r, g, b,
        -0.2, 0.1, 0, r, g, b,
        -0.1, 0.1, 0, r, g, b,
        -0.1, 0.4, 0, r, g, b,
        -0.1, 0.3, 0, r, g, b,
        0.1, 0.4, 0, r, g, b,
        0.1, 0.3, 0, r, g, b,
        0, 0.3, 0, r, g, b,
        0.1, 0.1, 0, r, g, b,
        0, 0.1, 0, r, g, b,
        0, 0.2, 0, r, g, b,
        -0.1, 0.2, 0, r, g, b]


    Oi = [7, 8, 9,
        7, 9, 10,
        10, 11, 12,
        11, 12, 13,
        13, 14, 15,
        14, 15, 16,
        16, 17, 18,
        16, 18, 9]
    # 12 vértices para O, 19 vértices en total, índice máximo 18
    # Letra U
    (r, g, b) = (0, 0, 1)
    Uv = [0.2, 0.4, 0, r, g, b,
        0.3, 0.4, 0, r, g, b,
        0.2, 0.1, 0, r, g, b,
        0.3, 0.1, 0, r, g, b,
        0.3, 0.2, 0, r, g, b,
        0.5, 0.1, 0, r, g, b,
        0.5, 0.2, 0, r, g, b,
        0.4, 0.2, 0, r, g, b,
        0.5, 0.4, 0, r, g, b,
        0.4, 0.4, 0, r, g, b]

    Ui = [19, 20, 21,
        20, 21, 22,
        22, 23, 24,
        23, 24, 25,
        25, 26, 27,
        26, 27, 28]
    # 10 vértices para U, 29 vértices en total, índice máximo 28
    # Letra W
    (r, g, b) = (1, 0, 0)
    Wv = [-0.5, -0.05, 0, r, g, b,
        -0.4, 0, 0, r, g, b,
        -0.3, -0.3, 0, r, g, b,
        -0.35, -0.25, 0, r, g, b,
        -0.35, -0.3, 0, r, g, b,
        -0.25, -0.25, 0, r, g, b,
        -0.25, -0.3, 0, r, g, b,
        -0.35, -0.3, 0, r, g, b,
        -0.25, -0.3, 0, r, g, b,
        -0.3, -0.1, 0, r, g, b,
        -0.2, 0, 0, r, g, b,
        -0.1, -0.05, 0, r, g, b]

    Wi = [29, 30, 31,
    32, 33, 34,
    33, 34, 35,
    36, 37, 38,
    39, 40, 31]
    #12 vértices para W, 41 vértices en total. Índice máximo es 40
    #Letra I
    (r,g,b) = (0, 1, 1)
    Iv = [0.05, -0.15, 0, r, g, b,
        0, -0.3, 0, r, g, b,
        0.1, -0.3, 0, r, g, b]
    
    Ii = [41, 42, 43]
    #3 vértices para I, 44 vértices en total. Índice máximo es 43
    # Letra N
    (r,g,b) = (1, 1, 0)
    Nv = [0.2, -0.3, 0, r, g, b,
        0.2, 0, 0, r, g, b,
        0.3, -0.3, 0, r, g, b,
        0.3, 0, 0, r, g, b,
        0.3, -0.1, 0, r, g, b,
        0.4, -0.3, 0, r, g, b,
        0.4, -0.2, 0, r, g, b,
        0.5, -0.3, 0, r, g, b,
        0.4, 0, 0, r, g, b,
        0.5, 0, 0, r, g, b]

    Ni = [44, 45, 46,
    45, 46, 47,
    47, 48, 49,
    47, 49, 50,
    51, 52, 49,
    51, 52, 53]
    # 10 vértices para N, 54 vértices en total, índice máximo 53

    vertices = Yv + Ov + Uv + Wv+ Iv + Nv
    indices = Yi + Oi + Ui + Wi + Ii + Ni
    Shape = bs.Shape(vertices, indices)
    gpu = createGPUShape(Shape, pipeline)
    return gpu

def VerticesYouwin(time):
    # La figura que rodea el texto cambia forma según el tiempo sucedido
    verticesCuadrado = [
#   posición          colores
    -0.5, -0.5, 0.0,  1.0, 0.0, 0.0,
     0.5, -0.5, 0.0,  0.0, 1.0, 0.0,
     0.5,  0.5, 0.0,  0.0, 0.0, 1.0,
    -0.5,  0.5, 0.0,  1.0, 1.0, 1.0]

    # Copia del rainbow quad en el centro
    t1 = np.sin(time)
    t2 = np.sin(time + np.pi /2)
    t3 = np.sin(time + np.pi)
    t4 = np.sin(time + np.pi * 3 / 2)

    tx1 = np.cos(time)
    tx2 = np.cos(time + np.pi /2)
    tx3 = np.cos(time + np.pi)
    tx4 = np.cos(time + np.pi * 3 / 2)

    verticesDinamic = [
        #posición                  colores
        0, -0.75 - (0.25 * t1), 0, t1, t2, t3,
        0.75 + (0.25 * t3), 0,  0, t2, t3, t1,
        0, 0.75 + (0.25 * t1),  0, t3, t1, t2,
        -0.75 - (0.25 * t3), 0, 0, t1, t3, tx4,
        0.05 + 0.05*tx1 , -0.05  + 0.05*t1  ,  0, tx1, tx2, tx3,
        0.05 + 0.05*tx2 , -0.05  + 0.05*t2  ,  0, tx2, tx3, tx1,
        0.05 + 0.05*tx3 , -0.05  + 0.05*t3  ,  0, tx3, tx1, tx2,
        0.05 + 0.05*tx4 , -0.05  + 0.05*t4  ,  0, tx1, tx3, t4
    ]

    return verticesCuadrado + verticesDinamic

def indicesYouWin():
    # Definimos la conexión entre los índices
    indicesCuadrado = [
        0, 1, 2,
        2, 3, 0]
    indicesDinamic = [
        0, 1, 4,
        1, 2, 5,
        2, 3, 6,
        3, 0, 7,
        8, 9, 10,
        8, 10, 11
    ]

    return indicesCuadrado + indicesDinamic
