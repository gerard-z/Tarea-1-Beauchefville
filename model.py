"""Clases y objetos que corresponden a los distintos modelos dentro del juego"""
import glfw
import numpy as np
import grafica.transformations as tr

#### IDEA1: Agregar la "vacuna" con una textura y alguna forma de estrella que cambia dinámicamente sus vertices

### Sign : 0.2 - 0.5 - 1

class Player:
    def __init__(self):
        self.pos = np.array([0,-0.8])
        #self.vel = [1,1]
        self.model = None
        self.controller = None
        self.texture_index = 0
        self.hitbox = 0.1
    
    def setModel(self, node):
        # Se indexa a un nodo
        self.model = node

    def setController(self, controller):
        # Se le asocia el controlador
        self.controller = controller
    
    def getTexture_index(self):
        return self.texture_index
    
    def update(self, delta):
        #Se actualiza la posición del auto y la textura a utilizar
        dx=0
        #Si se presiona W
        if self.controller.is_w_pressed:
            if self.pos[0]<=-0.5:
                self.pos[1] += delta
            else:
                dx = delta
            self.texture_index = 1

        #Si se presiona S
        if self.controller.is_s_pressed and self.pos[1]>=-1:
            self.pos[1] -= delta
            self.texture_index = 0
        
        #Si se presiona D
        if self.controller.is_d_pressed and self.pos[0]<=0.5:
            self.pos[0] += delta
            self.texture_index = 2
        
        #Si se presiona A
        if self.controller.is_a_pressed and self.pos[0]>=-0.5:
            self.pos[0] -= delta
            self.texture_index = 3
        
        self.model.transform = tr.translate(self.pos[0],self.pos[1],0)

        #Da la información de que si hay que avanzar la escena o no.
        return dx
