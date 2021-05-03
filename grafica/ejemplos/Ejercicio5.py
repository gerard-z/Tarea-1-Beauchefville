""" P3 [Drive simulator] """

import glfw
import OpenGL.GL.shaders
import numpy as np
import grafica.basic_shapes as bs
import grafica.easy_shaders as es
import grafica.transformations as tr
import grafica.performance_monitor as pm
import grafica.scene_graph as sg
from shapes import *
from model import *
from numpy import random
import sys, os.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# We will use 32 bits data, so an integer has 4 bytes
# 1 byte = 8 bits
SIZE_IN_BYTES = 4


# Clase controlador con variables para manejar el estado de ciertos botones
class Controller:
    def __init__(self):
        self.fillPolygon = True
        self.is_w_pressed = False
        self.is_s_pressed = False
        self.is_a_pressed = False
        self.is_d_pressed = False


# we will use the global controller as communication with the callback function
controller = Controller()

# This function will be executed whenever a key is pressed or released
def on_key(window, key, scancode, action, mods):
    
    global controller
    
    # Caso de detectar la tecla [W], actualiza estado de variable
    if key == glfw.KEY_W:
        if action ==glfw.PRESS:
            controller.is_w_pressed = True
        elif action == glfw.RELEASE:
            controller.is_w_pressed = False

    # Caso de detectar la tecla [S], actualiza estado de variable
    if key == glfw.KEY_S:
        if action ==glfw.PRESS:
            controller.is_s_pressed = True
        elif action == glfw.RELEASE:
            controller.is_s_pressed = False

    # Caso de detectar la tecla [A], actualiza estado de variable
    if key == glfw.KEY_A:
        if action ==glfw.PRESS:
            controller.is_a_pressed = True
        elif action == glfw.RELEASE:
            controller.is_a_pressed = False

    # Caso de detectar la tecla [D], actualiza estado de variable
    if key == glfw.KEY_D:
        if action ==glfw.PRESS:
            controller.is_d_pressed = True
        elif action == glfw.RELEASE:
            controller.is_d_pressed = False

    # Caso de detecar la barra espaciadora, se cambia el metodo de dibujo
    if key == glfw.KEY_SPACE and action ==glfw.PRESS:
        controller.fillPolygon = not controller.fillPolygon

    # Caso en que se cierra la ventana
    elif key == glfw.KEY_ESCAPE and action ==glfw.PRESS:
        glfw.set_window_should_close(window, True)



if __name__ == "__main__":

    # Initialize glfw
    if not glfw.init():
        glfw.set_window_should_close(window, True)

    # Creating a glfw window
    width = 800
    height = 800
    title = "P3 - Drive simulator"
    window = glfw.create_window(width, height, title, None, None)

    if not window:
        glfw.terminate()
        glfw.set_window_should_close(window, True)

    glfw.make_context_current(window)

    # Connecting the callback function 'on_key' to handle keyboard events
    glfw.set_key_callback(window, on_key)

    # Pipeline para dibujar shapes con colores interpolados
    pipeline = es.SimpleTransformShaderProgram()
    # Pipeline para dibujar shapes con texturas
    tex_pipeline = es.SimpleTextureTransformShaderProgram()

    # Setting up the clear screen color
    glClearColor(0.15, 0.15, 0.15, 1.0)

    # Enabling transparencies
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    # Grafo de escena del auto
    car = createCar(pipeline) 
    # Grafo de escena del background
    mainScene = createScene(pipeline)
    # Se añade el auto a la escena principal
    mainScene.childs += [car]

    # Se instancia el modelo del auto
    player = Player(0.3)
    # Se indican las referencias del nodo y el controller al modelo
    player.set_model(car)
    player.set_controller(controller)

    # Dirección de sprites
    thisFilePath = os.path.abspath(__file__)
    thisFolderPath = os.path.dirname(thisFilePath)
    spritesDirectory = os.path.join(thisFolderPath,"sprites")

    # Shape con textura de la carga
    garbage = createTextureGPUShape(bs.createTextureQuad(1,1), tex_pipeline, os.path.join(spritesDirectory,"bag.png"))

    # Se crean tres nodos de carga
    garbage1Node = sg.SceneGraphNode("garbage1")
    garbage1Node.childs = [garbage]

    garbage2Node = sg.SceneGraphNode("garbage2")
    garbage2Node.childs = [garbage]

    garbage3Node = sg.SceneGraphNode("garbage3")
    garbage3Node.childs = [garbage]

    # Se crean el grafo de escena con textura y se agregan las cargas
    tex_scene = sg.SceneGraphNode("textureScene")
    tex_scene.childs = [garbage1Node, garbage2Node, garbage3Node]

 

    # Se duplican los nodos de molinos y montañas para la sensación de movimiento.
    windMillGroupNode = sg.findNode(mainScene, "windMills") # Se encuentra el nodo de los molinos
    mountainsNode = sg.findNode(mainScene, "mountains")     # Se encuentra el nodo de las montañas
    windMillGroupNode2 = sg.SceneGraphNode("windMills2")    # Se crea una copia del nodo de los molinos
    windMillGroupNode2.childs = windMillGroupNode.childs    # Se agregan los mismos hijos a la copia
    mountainsNode2 = sg.SceneGraphNode("mountains2")        # Se crea una copia del nodo de las montañas
    mountainsNode2.childs = mountainsNode.childs            # Se agregan los mismos hijos a la copia

    # Las copias generadas se agregan a la escena principal
    backGround = sg.findNode(mainScene, "background")           # Se encuentra el nodo del fondo
    backGround.childs = backGround.childs[0:3]+[mountainsNode2, windMillGroupNode2] + backGround.childs[3:]   # Se agregan los nodos copiados al fondo


    perfMonitor = pm.PerformanceMonitor(glfw.get_time(), 0.5)
    # glfw will swap buffers as soon as possible
    glfw.swap_interval(0)
    t0 = glfw.get_time()
    xRandom1=0.5
    xRandom2=0.25
    xRandom3=0
    yRandom1=-0.5
    yRandom2=-0.8
    yRandom3=-0.65
    invulnerable= False
    t_invulnerable=0
    # Application loop
    while not glfw.window_should_close(window):
        # Variables del tiempo
        t1 = glfw.get_time()
        delta = t1 -t0
        t0 = t1

        # Measuring performance
        perfMonitor.update(glfw.get_time())
        glfw.set_window_title(window, title + str(perfMonitor))
        # Using GLFW to check for input events
        glfw.poll_events()

        # Filling or not the shapes depending on the controller state
        if (controller.fillPolygon):
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

        # Clearing the screen
        glClear(GL_COLOR_BUFFER_BIT)

        x= (2-t1%5)
        xCarga1=x-xRandom1
        xCarga2=x-0.25+xRandom2
        xCarga3=x+0.5+xRandom3

        if xCarga1<-2:
            xRandom1=random.rand()
            yRandom1=-0.5-random.randint(30)/100
        if xCarga2<-2:
            xRandom2=random.rand()
            yRandom2=-0.5-random.randint(30)/100
        if xCarga3<-2:
            xRandom3=random.rand()
            yRandom3=-0.5-random.randint(30)/100

        # Se crean los modelos de la carga, se indican su nodo y se actualiza la posicion fija
        carga1 = Carga(xCarga1, yRandom1, 0.1)
        carga1.set_model(garbage1Node)
        carga1.update()

        carga2 = Carga(xCarga2, yRandom2, 0.1)
        carga2.set_model(garbage2Node)
        carga2.update()

        carga3 = Carga(xCarga3, yRandom3, 0.1)
        carga3.set_model(garbage3Node)
        carga3.update()

        # Lista con todas las cargas
        cargas = [carga1, carga2, carga3]

        # Se llama al metodo del player para detectar colisiones
        if not player.is_crashed and not invulnerable:
            player.collision(cargas)
        # Se llama al metodo del player para actualizar su posicion
        player.update(delta)

        if player.is_crashed:
            print("chocado")
            invulnerable = True
            t_invulnerable= glfw.get_time()
            player.is_crashed = False

        if glfw.get_time()-t_invulnerable>1:
            invulnerable =False
        
        if invulnerable:
            print("Eres invulnerable")

        # Se crea el movimiento de giro del rotor
        rotor = sg.findNode(mainScene, "rtRotor")
        rotor.transform = tr.rotationZ(t1)

        # Se crea el movimiento del fondo.
        dx= 2-(t1)%4                # Variable de desplazamiento para el fondo 1
        dx2= 2-((t1+2)%4)           # Variable de desplazamiento para el fondo 2
        windMillGroupNode.transform = tr.translate(dx,0,0)
        windMillGroupNode2.transform = tr.translate(dx2,-0.05,0)
        mountainsNode.transform = tr.translate(dx,-0.3,0)
        mountainsNode2.transform = tr.translate(dx2,-0.4,0)

        # Se dibuja el grafo de escena principal
        glUseProgram(pipeline.shaderProgram)
        sg.drawSceneGraphNode(mainScene, pipeline, "transform")

        # Se dibuja el grafo de escena con texturas
        glUseProgram(tex_pipeline.shaderProgram)
        sg.drawSceneGraphNode(tex_scene, tex_pipeline, "transform")

        # Once the drawing is rendered, buffers are swap so an uncomplete drawing is never seen.
        glfw.swap_buffers(window)

    # freeing GPU memory
    mainScene.clear()
    tex_scene.clear()
    
    glfw.terminate()