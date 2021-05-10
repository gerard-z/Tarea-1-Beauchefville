"""Clases y objetos que corresponden a los distintos modelos dentro del juego"""
import glfw
import numpy as np
import grafica.transformations as tr
from numpy import random

#### IDEA1: Agregar la "vacuna" con una textura y alguna forma de estrella que cambia dinámicamente sus vertices

### Sign : 0.2 - 0.5 - 1

class Player:
    #Clase que tendrá las características para el jugador
    def __init__(self, p):
        self.pos = np.array([0,-0.8])
        #self.vel = [1,1]
        self.model = None
        self.controller = None
        self.texture_index = 0
        self.status = 0 # Estado, explicado en la clase npc
        self.prob = p #Probabilidad de volverse zombie, una vez infectada
        self.hitbox = 0.05
    
    def setModel(self, node):
        # Se indexa a un nodo
        self.model = node

    def setController(self, controller):
        # Se le asocia el controlador
        self.controller = controller
    
    def setTexture_index_default(self):
        # Se devuelve al sprite default
        self.texture_index = 0
    
    def setStatus(self,s):
        # Se modifica el estado actual
        self.status = s
    
    def getStatus(self):
        # Retorna el estado actual
        return self.status
    
    def getTexture_index(self):
        # Retoran el id actual del sprite
        return self.texture_index
    
    def Convertirse(self):
        if self.getStatus() == 1:
            n=random.rand()
            if n < self.prob:
                self.setStatus(2)
            pass
    
    
    def update(self, delta):
        #Se actualiza la posición del auto y la textura a utilizar
        dy=0
        delta = delta/4
        #Si se presiona W
        if self.controller.is_w_pressed:
            if self.pos[1]<=0:
                self.pos[1] += delta
            else:
                dy = delta
            self.texture_index = 1

        #Si se presiona S
        if self.controller.is_s_pressed and self.pos[1]>=-0.9:
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
        return dy
    
    def collision(self, npc):
        # Funcion para detectar el contacto entre el jugador y los npc

        # si la distancia entre el npc y el jugador es menor a la distancia del hitbox
        if (self.hitbox+npc.hitbox)**2 > ((self.pos[0]- npc.pos[0])**2 + (self.pos[1]-npc.pos[1])**2):
            if npc.getStatus() == 0:
                #colisión con un humano limpio, nada
                pass
            elif npc.getStatus() == 1:
                #colisión con un humano contagiado, ahora estamos contagiado
                self.setStatus(1)
            else:
                #colisión con un zombie, se pierde
                pass
class npc():
    # Clase que tendrá las características de un npc
    def __init__(self, posx, posy, status, p, index):
        self.pos = [posx, posy]
        self.model = None
        self.status = status        # El estado determinará si es humano (0), contagiado (1) y zombie (2)
        self.hitbox = 0.05
        self.prob = p               # La probabilidad de volverse zombie una vez contagiado
        self.index = index          # El índice donde está guardado la escena en la lista de los elementos

    def getPos(self):
        # Entrega la posición y del npc
        return self.pos[1]

    def getIndex(self):
        # Entrega el índice en donde está guardado el modelo
        return self.index
    
    def getStatus(self):
        # Entrega el estado del npc
        return self.status

    def setStatus(self, s):
        # Actualiza el estado del npc
        self.status = s
    
    def set_model(self, new_model):
        self.model = new_model

    def update(self,delta):
        #Actualiza la posición del npc
        k= random.randint(21)
        dist = delta/40

        self.pos[1]-= dist * 2 * k

        if self.pos[0] <=0.5 and k>10:
            self.pos[0]+= dist * k 
        if self.pos[0] >= -0.5 and k<10:
            self.pos[0]-= dist * (k+10)

        # Se posiciona el nodo referenciado
        self.model.transform = tr.translate(self.pos[0], self.pos[1], 0)