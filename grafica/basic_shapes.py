
# coding=utf-8
"""Vertices and indices for a variety of simple shapes"""
""" Modificado, agregando algunas otras figuras básicas y eliminando las figuras 3D"""

import math
import numpy as np
import grafica.transformations as tr

__author__ = "Daniel Calderon"
__license__ = "MIT"

# A simple class container to store vertices and indices that define a shape
class Shape:
    def __init__(self, vertices, indices, textureFileName=None):
        self.vertices = vertices
        self.indices = indices
        self.textureFileName = textureFileName


def merge(destinationShape, strideSize, sourceShape):

    # current vertices are an offset for indices refering to vertices of the new shape
    offset = len(destinationShape.vertices)
    destinationShape.vertices += sourceShape.vertices
    destinationShape.indices += [(offset/strideSize) + index for index in sourceShape.indices]


def applyOffset(shape, stride, offset):

    numberOfVertices = len(shape.vertices)//stride

    for i in range(numberOfVertices):
        index = i * stride
        shape.vertices[index]     += offset[0]
        shape.vertices[index + 1] += offset[1]
        shape.vertices[index + 2] += offset[2]


def scaleVertices(shape, stride, scaleFactor):

    numberOfVertices = len(shape.vertices) // stride

    for i in range(numberOfVertices):
        index = i * stride
        shape.vertices[index]     *= scaleFactor[0]
        shape.vertices[index + 1] *= scaleFactor[1]
        shape.vertices[index + 2] *= scaleFactor[2]


def createRainbowTriangle():

    # Defining the location and colors of each vertex  of the shape
    vertices = [
    #   positions        colors
        -0.5, -0.5, 0.0,  1.0, 0.0, 0.0,
         0.5, -0.5, 0.0,  0.0, 1.0, 0.0,
         0.0,  0.5, 0.0,  0.0, 0.0, 1.0]

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [0, 1, 2]

    return Shape(vertices, indices)


def createRainbowQuad():

    # Defining the location and colors of each vertex  of the shape
    vertices = [
    #   positions        colors
        -0.5, -0.5, 0.0,  1.0, 0.0, 0.0,
         0.5, -0.5, 0.0,  0.0, 1.0, 0.0,
         0.5,  0.5, 0.0,  0.0, 0.0, 1.0,
        -0.5,  0.5, 0.0,  1.0, 1.0, 1.0]

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [
        0, 1, 2,
        2, 3, 0]

    return Shape(vertices, indices)


def createColorQuad(r, g, b):

    # Defining locations and colors for each vertex of the shape    
    vertices = [
    #   positions        colors
        -0.5, -0.5, 0.0,  r, g, b,
         0.5, -0.5, 0.0,  r, g, b,
         0.5,  0.5, 0.0,  r, g, b,
        -0.5,  0.5, 0.0,  r, g, b]

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [
         0, 1, 2,
         2, 3, 0]

    return Shape(vertices, indices)


def createTextureQuad(nx, ny):

    # Defining locations and texture coordinates for each vertex of the shape    
    vertices = [
    #   positions        texture
        -0.5, -0.5, 0.0,  0, ny,
         0.5, -0.5, 0.0, nx, ny,
         0.5,  0.5, 0.0, nx, 0,
        -0.5,  0.5, 0.0,  0, 0]

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [
         0, 1, 2,
         2, 3, 0]

    return Shape(vertices, indices)


def createRainbowCircle(N):

    # First vertex at the center, white color
    vertices = [0, 0, 0, 1.0, 1.0, 1.0]
    indices = []

    dtheta = 2 * math.pi / N

    for i in range(N):
        theta = i * dtheta

        vertices += [
            # vertex coordinates
            0.5 * math.cos(theta), 0.5 * math.sin(theta), 0,

            # color generates varying between 0 and 1
                  math.sin(theta),       math.cos(theta), 0]

        # A triangle is created using the center, this and the next vertex
        indices += [0, i, i+1]

    # The final triangle connects back to the second vertex
    indices += [0, N, 1]

    return Shape(vertices, indices)


def createColorCircleLines(N, r, g, b):
    """ int float float float -> Shape()
        Recibe el número de vértices con el que se desea crear el círculo,
        también los componentes r g b para colorear el mismo círculo,
        el diámetro del círculo es de 1, con el centro en el 0.
        Dibujado con líneas
        """
    assert type(N)==int, "El número de intervalos debe ser entero"
    #vértices e índices del círculo
    vertices = np.zeros(N*6)
    indices = np.array(range(N))
    dtheta = 2 * np.pi/N

    for i in range(N):
        theta = i * dtheta
        vertices[i*6:i*6+6] = [0.5 * np.cos(theta), 0.5 * np.sin(theta), 0, r, g, b]
    
    return Shape(vertices, indices)

def createColorCircle(N, r, g, b):
    """ int float float float -> Shape()
        Recibe el número de vértices con el que se desea crear el círculo,
        también los componentes r g b para colorear el mismo círculo,
        el diámetro del círculo es de 1, con el centro en el 0.
        Dibujado con triángulos.
        """
    assert type(N)==int and N>0, "El número de intervalos debe ser entero positivo"
    #vértices e índices del círculo
    vertices = np.zeros(N*6)
    indices = np.zeros(N*3)
    dtheta = 2 * np.pi/(N-2)
    vertices[0:6] = [0, 0, 0, r, g, b]

    for i in range(N-1):
        theta = i * dtheta
        j= (i+1)*6
        vertices[j:j+6] = [0.5 * np.cos(theta), 0.5 * np.sin(theta), 0, r, g, b]
        indices[i*3:i*3+3] = [0, i, i+1]

    #indices[N-6:N] = [0, N-3, N-2, 0, N-2, N-1]
    
    return Shape(vertices, indices)

def createTextureArch(N):
    """ int -> Shape
    Crea un arco a partir de una semi circunferencia de N vértices, esta función fue hecha pensando en que la textura
    a entregar es un rectangulo largo y angosto, que corresponderá a cada triángulo de la figura."""

    assert type(N)==int and N>0, "El número de intervalos debe ser entero positivo"
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
    
    return Shape(vertices, indices)

def createSimpleQuad():
    """ -> Shape 
    Esta función está pensada para crear los vértices de posición de un cuadrado sin ningún otro componente,
    de esta manera, las coordenadas de textura y colores serán agregados después directamente en la memoria"""
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

    return Shape(vertices, indices)

def createZicZacLineStrip(N, A, r, g, b):
    """ int float float float float -> shape
    Crea una línea zic zac de N cambios de direcciones y amplitud A, permitiendo así agregar detalles a figuras.
    Si N=0, entonces es una línea recta de largo 1.
    El signo de A modifica si va primero hacia arriba o abajo en el zic zac."""
    assert type(N)==int and N>=0, "El número de intervalos debe ser entero positivo"

    vertices = np.zeros((N+2)*6)
    indices = np.array(range(N+2))
    vertices[0:6] = [-0.5, 0, 0, r, g, b]
    vertices[(N+1)*6:(N+2)*6] = [0.5, 0, 0, r, g, b]

    if N==0:
        return Shape(vertices, indices)
    
    offset = 1/(N+1)
    for i in range(1, N+1):
        vertices[i*6:(i+1)*6] = [-0.5 + i * offset, A, 0, r, g, b]
        A= -A
    
    return Shape(vertices, indices)

def createSpiralLineStrip(N, L, r, g, b):
    """ int float int float float float -> Shape
    Función que genera una espiral a través de una transformación geométrica, N es el número de vértices que tendrá
    sin incluir el centro, y L serán el número de vueltas que da alrededor del centro. El radio máximo es de 0.5.
    Utiliza transformaciones matriciales para la figura"""

    assert type(N)== int and N>0, "N debe ser un entero positivo"
    assert type(L) == int and L>0, "L debe ser un entero positivo"
    
    vertices= np.zeros((N+1)*6)
    indices = np.array(range(N+1))

    NL = (N)//L # Número de vértices por vuelta, descontando el vértice del centro
    dtheta = 2 * np.pi / NL
    R= 0.5/L  # Radio máximo que tendrá un loop

    x = np.array([1,0,0,1]) # Vector de referencia para las transformaciones

    for l in range(1,L+1):
        rl = l * R  #radio máximo
        r0= (l-1) * R #radio mínimo
        radio = rl-r0
        for i in range(NL):
            theta = i * dtheta
            dr = r0 + i * radio / NL
            transformation = tr.matmul([tr.rotation(theta), tr.uniformScale(dr)])
            xp = tr.matmul([transformation, x])
            #Se vuelve a los vértices con coordenadas originales
            position = np.array([xp[0], xp[1], xp[2]]) / xp[3] 
            vertices[((l-1) * NL + i)*6 : ((l-1) * NL + i + 1)*6] = [position[0], position[1], position[2], r, g, b]
    
    #Agregar el vértice final
    vertices[N * 6 : N * 6 + 6] = [0.5, 0, 0, r, g, b]
    
    return Shape(vertices, indices)

