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

#sys.argv
#Z=sys.argv[1]

# We will use 32 bits data, so an integer has 4 bytes
# 1 byte = 8 bits
SIZE_IN_BYTES = 4

#Variables entregadas al enunciar el programa
Z= 2            # Zombies
H= 3            # Humanos
T= 5            # Tiempo
P= 0.5          # Probabilidad


# Clase controlador con variables para manejar el estado de ciertos botones
class Controller:
    def __init__(self):
        self.fillPolygon = True
        self.is_w_pressed = False
        self.is_s_pressed = False
        self.is_a_pressed = False
        self.is_d_pressed = False
        self.what_to_draw = 1


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
    # Pipeline encargada de dibujar shapes con texturas controladas por el jugador
    PlayableTex_pipeline = es.SimpleTextureTransform3FrameControllerShaderProgram()

    # Setting up the clear screen color
    glClearColor(0.15, 0.15, 0.15, 1.0)


    # Enabling transparencies
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    
    ######### SHAPES ######

    NPC = sg.SceneGraphNode("npc")

    background = createBackground(pipeline)
    store = createStore(tex_pipeline)
    storeSign = createAnimatedSign(animated3Tex_pipeline)
    details = createDetails(pipeline)

    hinata = createHinata(PlayableTex_pipeline)
    gpuHinata = hinata.childs[0]

    zombies = []
    humanos = []


    perfMonitor = pm.PerformanceMonitor(glfw.get_time(), 0.5)
    # glfw will swap buffers as soon as possible
    glfw.swap_interval(0)

    # Ubicación de nodos:
    hojas= sg.findNode(background, "hojas")
    arboles1 = sg.findNode(background, "arboles1")
    arboles2 = sg.findNode(background, "arboles2")
    lineas1 = sg.findNode(background, "Lineatransito1")
    lineas2 = sg.findNode(background, "Lineatransito2")
    decoracion1 = sg.findNode(details, "decoration1")
    decoracion2 = sg.findNode(details, "decoration2")

    Store = sg.findNode(store, "Store")
    Sign = sg.findNode(storeSign, "StoreSign")

    #Distinción de frames en las texturas:
    singInit = np.array([0.0, 0.34, 0.64])
    signFin = np.array([0.33, 0.63, 1])
    actual_sprite=0

    FrameInit = np.array([0, 1/3, 2/3])
    FrameFin = np.array([1/3, 2/3, 1])

    player = Player(P)
    player.setModel(hinata)
    player.setController(controller)

    lNpc=[]



    # Variables útiles para el procedimiento
    t0 = glfw.get_time()
    dx = 0
    t3=T
    dy = 0
    dy2 = 0
    # Application loop
    while not glfw.window_should_close(window):
        # Variables del tiempo
        t1 = glfw.get_time()
        delta = t1 -t0
        t0 = t1

        t3 += delta
        t4 = t1%1.5


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

        #PLAYER
        dy -= player.update(delta)
        texture = player.getTexture_index()
        if texture == 0:
            gpuHinata.texture =es.textureSimpleSetup(hinataFrontPath, GL_CLAMP_TO_EDGE, GL_CLAMP_TO_EDGE,
                                                    GL_NEAREST, GL_NEAREST)
        elif texture == 1:
            gpuHinata.texture =es.textureSimpleSetup(hinataBackPath, GL_CLAMP_TO_EDGE, GL_CLAMP_TO_EDGE,
                                                    GL_NEAREST, GL_NEAREST)
        else:
            gpuHinata.texture =es.textureSimpleSetup(hinataSidePath, GL_CLAMP_TO_EDGE, GL_CLAMP_TO_EDGE,
                                                    GL_NEAREST, GL_NEAREST)

        #NPC
        if t3 > T:
            nZ = len(zombies)
            nH = len(humanos)
            for i in range(Z):
                rand = random.rand()
                zombies.append(createZombie(PlayableTex_pipeline))
                lNpc.append(npc(rand-0.5, rand+ 1.1, 2, P, nZ+i))
                lNpc[nH + nZ + i].set_model(zombies[nZ + i])
            NPC.childs += zombies[nZ:]
            nZ = len(zombies)
            for i in range(H):
                p=0
                rand = random.rand()
                if random.rand()<P:
                    p=1
                humanos.append(createHumano(PlayableTex_pipeline))
                lNpc.append(npc(rand-0.5,rand + 1.1, p, P, nH+i))
                lNpc[nH + nZ +i].set_model(humanos[nH + i])
            NPC.childs += humanos[nH:]
            t3=0
            player.Convertirse()
    

        for ZomHum in lNpc:
            ZomHum.update(delta)
            player.collision(ZomHum)

            

        
        # Se agregan los movimientos durante escena
        dx += delta*2
        if dy2>-0.6:
            dy2 = 2 + dy
        hojas.transform = tr.matmul([tr.translate(0, 0.3, 0),tr.shearing(0.2*np.sin(dx), 0, 0, 0, 0, 0)])
        arboles1.transform = tr.translate(0, dy, 0)
        arboles2.transform = tr.translate(0, dy2, 0)
        lineas1.transform = tr.translate(0, dy, 0)
        lineas2.transform = tr.translate(0, dy2, 0)
        decoracion1.transform = tr.translate(0, dy, 0)
        decoracion2.transform = tr.translate(0, dy2, 0)
        Store.transform = tr.translate(0, dy2, 0)
        Sign.transform = tr.translate(0, dy2, 0)

        #Animación:
        if t4<0.5:
            if texture !=3:
                time=0
            else:
                time=2
        elif t4<1:
            time=1
        else:
            if texture !=3:
                time=2
            else:
                time=0

        # Se dibuja el grafo de escena.
        if player.getStatus() !=2:
            glUseProgram(pipeline.shaderProgram)
            sg.drawSceneGraphNode(background, pipeline, "transform")
            sg.drawSceneGraphNode(details, pipeline, "transform", GL_LINE_STRIP)

            glUseProgram(tex_pipeline.shaderProgram)
            sg.drawSceneGraphNode(store, tex_pipeline, "transform")

            glUseProgram(animated3Tex_pipeline.shaderProgram)
            glUniform3fv(glGetUniformLocation(animated3Tex_pipeline.shaderProgram, "spritesInit"), 1, singInit)
            glUniform3fv(glGetUniformLocation(animated3Tex_pipeline.shaderProgram, "spritesFin"), 1, signFin)
            glUniform1i(glGetUniformLocation(animated3Tex_pipeline.shaderProgram, "index"), time)
            sg.drawSceneGraphNode(storeSign, animated3Tex_pipeline, "transform")

            glUseProgram(PlayableTex_pipeline.shaderProgram)
            glUniform3fv(glGetUniformLocation(PlayableTex_pipeline.shaderProgram, "spritesInit"), 1, FrameInit)
            glUniform3fv(glGetUniformLocation(PlayableTex_pipeline.shaderProgram, "spritesFin"), 1, FrameFin)
            glUniform1i(glGetUniformLocation(PlayableTex_pipeline.shaderProgram, "index"), time)
            glUniform1i(glGetUniformLocation(PlayableTex_pipeline.shaderProgram, "move"), texture)
            sg.drawSceneGraphNode(hinata, PlayableTex_pipeline, "transform")
            glUniform1i(glGetUniformLocation(PlayableTex_pipeline.shaderProgram, "move"), 0)
            sg.drawSceneGraphNode(NPC, PlayableTex_pipeline, "transform")
        else:
            glUseProgram(animated3Tex_pipeline.shaderProgram)
            glUniform3fv(glGetUniformLocation(animated3Tex_pipeline.shaderProgram, "spritesInit"), 1, singInit)
            glUniform3fv(glGetUniformLocation(animated3Tex_pipeline.shaderProgram, "spritesFin"), 1, signFin)
            glUniform1i(glGetUniformLocation(animated3Tex_pipeline.shaderProgram, "index"), time)
            sg.drawSceneGraphNode(storeSign, animated3Tex_pipeline, "transform")

        player.setTexture_index_default()
        if dy2<=-0.6 and player.pos[0] <0-0.3 and player.pos[1] >-0.3:
            print ("Misión exitosa")

        for ZomHum in lNpc:
            if ZomHum.getPos()<-1.3:
                index = ZomHum.getIndex()
                if ZomHum.getStatus() == 2:
                    NPC.childs.remove(ZomHum.model)
                    ZomHum.model.clear()
                    zombies.remove(ZomHum.model)
                else:
                    NPC.childs.remove(ZomHum.model)
                    ZomHum.model.clear()
                    humanos.remove(ZomHum.model)
                lNpc.remove(ZomHum)

        # Once the drawing is rendered, buffers are swap so an uncomplete drawing is never seen.
        glfw.swap_buffers(window)

    # freeing GPU memory
    background.clear()
    store.clear()
    storeSign.clear()
    details.clear()
    hinata.clear()
    NPC.clear()
    
    glfw.terminate()