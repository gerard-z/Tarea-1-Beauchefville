""" Funciones para crear las distintas figuras de la escena """

import numpy as np
import math
from OpenGL.GL import *
import grafica.basic_shapes as bs
import grafica.easy_shaders as es
import grafica.transformations as tr
import grafica.scene_graph as sg

def createGPUShape(shape, pipeline):
    # Funcion Conveniente para facilitar la inicializacion de un GPUShape
    gpuShape = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuShape)
    gpuShape.fillBuffers(shape.vertices, shape.indices, GL_STATIC_DRAW)
    return gpuShape

def createTextureGPUShape(shape, pipeline, path):
    # Funcion Conveniente para facilitar la inicializacion de un GPUShape con texturas
    gpuShape = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuShape)
    gpuShape.fillBuffers(shape.vertices, shape.indices, GL_STATIC_DRAW)
    gpuShape.texture = es.textureSimpleSetup(
        path, GL_CLAMP_TO_EDGE, GL_CLAMP_TO_EDGE, GL_NEAREST, GL_NEAREST)
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


