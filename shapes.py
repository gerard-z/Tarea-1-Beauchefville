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

