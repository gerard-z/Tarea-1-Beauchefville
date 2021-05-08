
# coding=utf-8
"""Vertices and indices for a variety of simple shapes"""
""" Modificado, agregando algunas otras figuras básicas y eliminando las figuras 3D"""

import math
import numpy as np

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
    assert type(N)==int, "El número de intervalos debe ser entero"
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