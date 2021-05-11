# coding=utf-8
"""A simple scene graph class and functionality"""

from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
import grafica.transformations as tr
import grafica.gpu_shape as gs

__author__ = "Daniel Calderon"
__license__ = "MIT"


class SceneGraphNode:
    """
    A simple class to handle a scene graph
    Each node represents a group of objects
    Each leaf represents a basic figure (GPUShape)
    To identify each node properly, it MUST have a unique name
    """
    def __init__(self, name):
        self.name = name
        self.transform = tr.identity()
        self.childs = []

    def clear(self):
        """Freeing GPU memory"""

        for child in self.childs:
            child.clear()

            

    
def findNode(node, name):

    # The name was not found in this path
    if isinstance(node, gs.GPUShape):
        return None

    # This is the requested node
    if node.name == name:
        return node
    
    # All childs are checked for the requested name
    for child in node.childs:
        foundNode = findNode(child, name)
        if foundNode != None:
            return foundNode

    # No child of this node had the requested name
    return None


def findTransform(node, name, parentTransform=tr.identity()):

    # The name was not found in this path
    if isinstance(node, gs.GPUShape):
        return None

    newTransform = np.matmul(parentTransform, node.transform)

    # This is the requested node
    if node.name == name:
        return newTransform
    
    # All childs are checked for the requested name
    for child in node.childs:
        foundTransform = findTransform(child, name, newTransform)
        if isinstance(foundTransform, (np.ndarray, np.generic) ):
            return foundTransform

    # No child of this node had the requested name
    return None


def findPosition(node, name, parentTransform=tr.identity()):
    foundTransform = findTransform(node, name, parentTransform)

    if isinstance(foundTransform, (np.ndarray, np.generic) ):
        zero = np.array([[0,0,0,1]], dtype=np.float32).T
        foundPosition = np.matmul(foundTransform, zero)
        return foundPosition

    return None


def drawSceneGraphNode(node, pipeline, transformName, mode=GL_TRIANGLES, parentTransform=tr.identity()):
    assert(isinstance(node, SceneGraphNode))

    # Composing the transformations through this path
    newTransform = np.matmul(parentTransform, node.transform)



    # If the child node is a leaf, it should be a GPUShape.
    # Hence, it can be drawn with drawCall
    if len(node.childs) == 1 and isinstance(node.childs[0], gs.GPUShape):
        leaf = node.childs[0]
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, transformName), 1, GL_TRUE, newTransform)
        pipeline.drawCall(leaf, mode)

    # If the child node is not a leaf, it MUST be a SceneGraphNode,
    # so this draw function is called recursively
    else:
        for child in node.childs:
            drawSceneGraphNode(child, pipeline, transformName, mode, newTransform)

class SceneGraphNodeMultiPipeline:
    """
    A simple class to handle a scene graph
    Each node represents a group of objects
    Each leaf represents a basic figure (GPUShape)
    To identify each node properly, it MUST have a unique name
    Now a some node can have diferent a list with diferent Pipeline in their childs
    But leaf only can have one pipeline
    """
    def __init__(self, name, listPipeline, status = "default"):
        self.name = name
        self.transform = tr.identity()
        self.childs = []
        self.pipeline = listPipeline
        self.status = status

    def clear(self):
        """Freeing GPU memory"""

        for child in self.childs:
            child.clear()
    def setStatus(self,s):
        # Actualiza el estado
        self.status = s

def drawSceneGraphNodeMultiPipeline(node, listPipeline, transformName, mode=GL_TRIANGLES, parentTransform=tr.identity()):
    assert(isinstance(node, SceneGraphNodeMultiPipeline))

    # Composing the transformations through this path
    newTransform = np.matmul(parentTransform, node.transform)


    # If the child node is a leaf, it should be a GPUShape.
    # Hence, it can be drawn with drawCall
    if len(node.childs) == 1 and isinstance(node.childs[0], gs.GPUShape):
        leaf = node.childs[0]
        pipeline = node.pipeline[0]
        if node.status=="default":
            glUseProgram(pipeline.shaderProgram)
        else:
            glUniform1i(glGetUniformLocation(pipeline.shaderProgram, "status"), node.status)
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, transformName), 1, GL_TRUE, newTransform)
        pipeline.drawCall(leaf, mode)

    # If the child node is not a leaf, it MUST be a SceneGraphNode,
    # so this draw function is called recursively

    else:
        for child in node.childs:
            LP= []
            for pipeline in node.pipeline:
                if pipeline in child.pipeline:
                    LP.append(pipeline)
            drawSceneGraphNodeMultiPipeline(child, LP, transformName, mode, newTransform)

