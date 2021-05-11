"""Clases y objetos que corresponden a los distintos modelos dentro del juego"""
import glfw
import numpy as np
import grafica.transformations as tr
import grafica.easy_shaders as es
from shapes import *
from numpy import random

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
        self.hitbox = 0.06
    
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
        # Calcula la probabilidad de convertirse en zombie si está contagiado
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
                self.model.setStatus(1)
            else:
                #colisión con un zombie, se pierde
                self.setStatus(2)
                pass
class npc():
    # Clase que tendrá las características de un npc
    def __init__(self, posx, posy, status, p):
        self.pos = [posx, posy]
        self.model = None
        self.status = status        # El estado determinará si es humano (0), contagiado (1) y zombie (2)
        self.hitbox = 0.06
        self.prob = p               # La probabilidad de volverse zombie una vez contagiado

    def getPos(self):
        # Entrega la posición y del npc
        return self.pos[1]
    
    def getStatus(self):
        # Entrega el estado del npc
        return self.status

    def setStatus(self, s):
        # Actualiza el estado del npc
        self.status = s

    def Convertirse(self):
        # Calcula probabilidad de convertirse un zombie si está contagiado
        if self.getStatus() == 1:
            n=random.rand()
            if n < self.prob:
                self.setStatus(2)
                self.model.childs[0].texture = es.textureSimpleSetup(zombiePath, GL_CLAMP_TO_EDGE, GL_CLAMP_TO_EDGE,
                                                                GL_NEAREST, GL_NEAREST)
                return True
        return False
    
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

    def collision(self, Lista):
        # Funcion para detectar el contacto entre npc y el resto de npcs.
        if len(Lista) == 0:
            return False
        
        #Recibe una lista con los npc que se compara
        status = self.getStatus()
        npclist = []
        for npc in Lista:
            dx = (self.pos[0] - npc.pos[0])**2
            dy = (self.pos[1] - npc.pos[1])**2
            Distancia = (self.hitbox + npc.hitbox)**2
            # Se analiza cada caso en donde cuál es el estado original del npc y de los que se compara
            if Distancia > dx + dy:
                npcStatus = npc.getStatus()
                if status == 0:
                    self.setStatus(npcStatus)
                elif status == 1:
                    if npcStatus ==2:
                        self.setStatus(npcStatus)
                    else:
                        npc.setStatus(status)
                else:
                    if npcStatus != 2:
                        npc.setStatus(status)
                        npc.model.childs[0].texture = es.textureSimpleSetup(zombiePath, GL_CLAMP_TO_EDGE, GL_CLAMP_TO_EDGE,
                                                                GL_NEAREST, GL_NEAREST)
                        npclist.append(npc)
        statusv2 = self.getStatus()
        self.model.setStatus(statusv2)

        if status <2 and statusv2 == 2:
            self.model.childs[0].texture = es.textureSimpleSetup(zombiePath, GL_CLAMP_TO_EDGE, GL_CLAMP_TO_EDGE,
                                                                GL_NEAREST, GL_NEAREST)
            return True
        elif len(npclist)!=0:
            return npclist
        return False
