# Survival

from OpenGL.GL import *
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
        self.what_to_draw = 0


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

    # Caso de detectar la tecla [0], actualiza que se dibuja
    if key == glfw.KEY_0 and action == glfw.PRESS:
        controller.what_to_draw = 0
    
    # Caso de detectar la tecla [1], actualiza que se dibuja
    if key == glfw.KEY_1 and action == glfw.PRESS:
        controller.what_to_draw = 1

    # Caso de detectar la tecla [2], actualiza que se dibuja
    if key == glfw.KEY_2 and action == glfw.PRESS:
        controller.what_to_draw = 2

    # Caso de detectar la tecla [3], actualiza que se dibuja
    if key == glfw.KEY_3 and action == glfw.PRESS:
        controller.what_to_draw = 3

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
    width = 600
    height = 600
    title = "Survival"
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
    # Pipeline para dibujar shapes con texturas animadas (3 fotogramas)
    animated3Tex_pipeline = es.SimpleTextureTransform3FrameAnimationShaderProgram()

    # Setting up the clear screen color
    glClearColor(0.15, 0.15, 0.15, 1.0)


    # Enabling transparencies
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    
    ######### SHAPES ######

    background = createBackground(pipeline)
    store = createStore(tex_pipeline)
    storeSign = createAnimatedSign(animated3Tex_pipeline)

    perfMonitor = pm.PerformanceMonitor(glfw.get_time(), 0.5)
    # glfw will swap buffers as soon as possible
    glfw.swap_interval(0)

    # Ubicación de nodos:
    hojas= sg.findNode(background, "hojas")
    arboles1 = sg.findNode(background, "arboles1")
    arboles2 = sg.findNode(background, "arboles2")
    lineas1 = sg.findNode(background, "Lineatransito1")
    lineas2 = sg.findNode(background, "Lineatransito2")

    #Distinción de frames en las texturas:
    storeSignFrame = np.array([0.18, 0.5, 1])
    actual_sprite=0


    # Variables útiles para el procedimiento
    t0 = glfw.get_time()
    dx = 0
    desplazamiento = 0
    dy = 2
    dy2 = 0
    # Application loop
    while not glfw.window_should_close(window):
        # Variables del tiempo
        t1 = glfw.get_time()
        delta = t1 -t0
        t0 = t1

        t3= glfw.get_time()%3


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

        # Se agregan los movimientos durante escena
        dx += delta*2
        desplazamiento = (desplazamiento + delta)%4
        desplazamiento2 = (desplazamiento + 2 + delta)%4
        dy = 2 - desplazamiento
        dy2 = 2 - desplazamiento2
        hojas.transform = tr.matmul([tr.translate(0, 0.3, 0),tr.shearing(0.2*np.sin(dx), 0, 0, 0, 0, 0)])
        arboles1.transform = tr.translate(0, dy, 0)
        arboles2.transform = tr.translate(0, dy2, 0)
        lineas1.transform = tr.translate(0, dy, 0)
        lineas2.transform = tr.translate(0, dy2, 0)

        #Animación:
        if t3>=0 and t3<1:
            actual_sprite=0
        elif t3>=1 and t3<2:
            actual_sprite=1
        else:
            actual_sprite=2


        # Se dibuja el grafo de escena que se selecciona. (Sirve para probar que tal estaban los dibujos)
        if controller.what_to_draw == 1:
            glUseProgram(pipeline.shaderProgram)
            sg.drawSceneGraphNode(background, pipeline, "transform")
        elif controller.what_to_draw == 2:
            glUseProgram(tex_pipeline.shaderProgram)
            sg.drawSceneGraphNode(store, tex_pipeline, "transform")

            glUseProgram(animated3Tex_pipeline.shaderProgram)
            glUniform3fv(glGetUniformLocation(animated3Tex_pipeline.shaderProgram, "spritesInit"), 1, np.array([0, 0, 0.5]))
            glUniform3fv(glGetUniformLocation(animated3Tex_pipeline.shaderProgram, "spritesFin"), 1, storeSignFrame)
            glUniform1i(glGetUniformLocation(animated3Tex_pipeline.shaderProgram, "index"), actual_sprite)

            sg.drawSceneGraphNode(storeSign, animated3Tex_pipeline, "transform")

        # Se dibuja el grafo de escena con texturas
        #glUseProgram(tex_pipeline.shaderProgram)
        #sg.drawSceneGraphNode(tex_scene, tex_pipeline, "transform")

        # Once the drawing is rendered, buffers are swap so an uncomplete drawing is never seen.
        glfw.swap_buffers(window)

    # freeing GPU memory
    background.clear()
    store.clear()
    
    glfw.terminate()