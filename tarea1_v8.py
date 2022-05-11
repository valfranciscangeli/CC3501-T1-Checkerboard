""""
Tercera version completa de la tarea 1
Cambios estéticos en la escena
Realizada por Valeria Vallejos Franciscangeli
vvfranciscangeli@gmail.com

Basado en el codigo de Ivan Sipiran para la Tarea 1 del curso CC3501 de la FCFM
Semestre Primavera 2021

Comentado en español
No necesita librerias externas a glfw, OpenGL.GL, OpenGL.GL.shaders y numpy

"""

__author__ = "Valeria Vallejos Franciscangeli"
__license__ = "MIT"

# importamos librerias----------------------------------------------------------
import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy

# usamos datos de  32 bits, un entero tiene 4 bytes
# 1 byte = 8 bits
SIZE_IN_BYTES = 4


# VERTICES DE DAMAS: --------------------------------------------------------------------------
# sin modificaciones

# funcion que entrega geometria de un circulo
def crear_dama(x, y, r, g, b, radius):
    circle = []
    for angle in range(0, 360, 10):
        circle.extend([x, y, 0.0, r, g, b])
        circle.extend([x + numpy.cos(numpy.radians(angle)) * radius,
                       y + numpy.sin(numpy.radians(angle)) * radius,
                       0.0, r, g, b])
        circle.extend([x + numpy.cos(numpy.radians(angle + 10)) * radius,
                       y + numpy.sin(numpy.radians(angle + 10)) * radius,
                       0.0, r, g, b])

    return numpy.array(circle, dtype=numpy.float32)  # arreglo numpy de vertices posiciones y colores


# VERTICES DE TABLERO:-----------------------------------------------------------------------

# funcion que entrega vertices (para no usar ebo) de un cuadrado
def crear_cuadrado(x, y, r, g, b, largo):
    # x e y coordenadas del vertice abajo a la izquierda
    # largo: largo del lado del cuadrado

    cuadrado = [
        # vertices             colores
        x, y, 0.0, r, g, b,  # 0
        x + largo, y, 0.0, r, g, b,  # 1
        x + largo, y + largo, 0.0, r, g, b,  # 2
        x + largo, y + largo, 0.0, r, g, b,  # 3
        x, y + largo, 0.0, r, g, b,  # 4
        x, y, 0.0, r, g, b]  # 5

    return cuadrado  # lista de vertices posiciones y colores

# funcion que geometria vertices del tablero utilizando la funcion que calcula vertices para
# cada cuadrado del tablero
def crear_tablero(x, y, r1, g1, b1, r2, g2, b2, largo):
    # x e y coordenadas del vertice abajo a la izquierda
    # largo: largo del lado del tablero

    tablero = crear_cuadrado(x, y, r1, g1, b1, largo)  # creamos cuadrado de fondo (negro original)
    largo = largo / 8  # largo de cada casilla del tablero
    fila = 8  # dibujaremos filas del tablero de abajo hacia arriba

    # coordenadas y:
    for j in [x, x + largo, x + 2 * largo, x + 3 * largo, x + 4 * largo, x + 5 * largo, x + 6 * largo, x + 7 * largo]:

        # coordenadas x:
        if fila % 2 == 0:  # si contador (fila)  es de numero par
            coordenadasX = [x + largo, x + 3 * largo, x + 5 * largo, x + 7 * largo]
        else:  # si contador (fila)  es de numero impar
            coordenadasX = [x, x + 2 * largo, x + 4 * largo, x + 6 * largo]

        for i in coordenadasX:
            tablero.extend(crear_cuadrado(i, j, r2, g2, b2, largo))
        fila -= 1  # pasaremos a la fila siguiente

    return numpy.array(tablero, dtype=numpy.float32)  # arreglo de vertices posiciones y colores

# VERTICES MARCO:---------------------------------------------------------------------------
def marco_tablero(x, y, r1, g1, b1, r2, g2, b2, largo):
    marco_grueso=crear_cuadrado(x,y,r1,g1,b1,largo)
    marco_interior=crear_cuadrado(x+0.04, y+0.04, r2, g2, b2, largo-0.08)
    marco_grueso.extend(marco_interior)
    return numpy.array(marco_grueso, dtype=numpy.float32)  # arreglo de vertices posiciones y colores

# FUNCIONES UTILES PARA EL RESTO DEL CODIGO:-------------------------------------------------

# funcion para unir geometrias a su vbo correspondiente
def unir_bufferVBO(geometria, vboN):
    # for i in range (0,24):
    glBindBuffer(GL_ARRAY_BUFFER, vboN)
    glBufferData(GL_ARRAY_BUFFER, len(geometria) * SIZE_IN_BYTES, geometria, GL_STATIC_DRAW)

# funcion para dibujar las figuras
def dibujo_figura(geometria, vboN):
    # sin modificaciones del original mas que cambiar algunos argumentos para que utilice
    # los que se les diga al llamarla (geometria y vbo de cada figura)

    glBindBuffer(GL_ARRAY_BUFFER, vboN)  # unir buffer y vbo de la figura

    position = glGetAttribLocation(shaderProgram, "position")
    glVertexAttribPointer(position, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(0))
    glEnableVertexAttribArray(position)

    color = glGetAttribLocation(shaderProgram, "color")
    glVertexAttribPointer(color, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(12))
    glEnableVertexAttribArray(color)

    glDrawArrays(GL_TRIANGLES, 0, int(len(geometria) / 6))
    # renderizando la geometria usando el shader program (pipeline) activo y el VAO (shapes) activo


# MAIN: seccion principal---------------------------------------------------------------------

if __name__ == "__main__":
    # inicializando glfw
    if not glfw.init():
        glfw.set_window_should_close(window, True)

    width = 600
    height = 600

    window = glfw.create_window(width, height, "Tarea 1", None, None) #configuracion de ventana

    if not window:
        glfw.terminate()
        glfw.set_window_should_close(window, True)

    glfw.make_context_current(window)

    # SHADER PROGRAM: --------------------------------------------------------------------
    # sin modificaciones

    # definiendo shaders para el pipeline
    vertex_shader = """
    #version 330
    in vec3 position;
    in vec3 color;

    out vec3 newColor;
    void main()
    {
        gl_Position = vec4(position, 1.0f);
        newColor = color;
    }
    """

    fragment_shader = """
    #version 330
    in vec3 newColor;

    out vec4 outColor;
    void main()
    {
        outColor = vec4(newColor, 1.0f);
    }
    """

    # Binding artificial vertex array object for validation
    VAO = glGenVertexArrays(1)
    glBindVertexArray(VAO)

    # Assembling the shader program (pipeline) with both shaders
    shaderProgram = OpenGL.GL.shaders.compileProgram(
        OpenGL.GL.shaders.compileShader(vertex_shader, GL_VERTEX_SHADER),
        OpenGL.GL.shaders.compileShader(fragment_shader, GL_FRAGMENT_SHADER))

    # ---------------------------------------------------------------------------------------

    # avisar a  OpenGL que use shader program
    glUseProgram(shaderProgram)

    # borramos la pantalla, seteando fondo color gris-verdoso (mas oscuro que el original)
    glClearColor(0.145, 0.221, 0.113, 1.0)
    glClear(GL_COLOR_BUFFER_BIT)

    # GEOMETRIAS PARA LA ESCENA:-------------------------------------------------------------
    """
    La escena finalmente creada consta de un cambio de color de fondo de la ventana,
    simulando el color de una mesa de pool. Además, se agrega un marco al tablero 
    que busca simular madera. Adicionalmente, se crean luces y sombras para las damas 
    utilizando la geometria de dama con un radio menor a las fichas y colores con altos
    y bajos rgb, respectivamente.
    Para mantener el orden, se decidió hacer cada tipo de figura en distinta sección.
    """
    # MARCO TABLERO:----------------------------------------------------------
    # creamos un marco al tablero tablero cuyo vertice izquiero inferior es (-0.86, -0.86),
    # es de 2 colores (exterior e interior) y largo 1.72
    marco = marco_tablero(-0.86, -0.86, 0.247, 0.074, 0.007, 0.564, 0.490, 0.419, 1.72)
    # vbo para la figura tablero
    vboMarco = glGenBuffers(1)
    # unir tablero a su buffer
    unir_bufferVBO(marco, vboMarco)
    # dibujo tablero
    dibujo_figura(marco, vboMarco)

    # TABLERO:--------------------------------------------------------------
    # creamos un tablero cuyo vertice izquiero inferior es (-0.8, -0.8),
    # es de colores blanco y negro y largo 1.6
    tablero = crear_tablero(-0.8, -0.8, 0.517, 0.247, 0.007, 0.854, 0.749, 0.501, 1.6)
    # vbo para la figura tablero
    vboTablero = glGenBuffers(1)
    # unir tablero a su buffer
    unir_bufferVBO(tablero, vboTablero)
    # dibujo tablero
    dibujo_figura(tablero, vboTablero)

    # LUZ DAMAS:-----------------------------------------------------------------
    radioDamas = 0.080
    color = (0.980, 0.968, 0.929)
    fila = 1

    for j in [0.7025, 0.5025, 0.3025, -0.2975, -0.4975, -0.6975]:
        if fila % 2 == 1:
            coordenadas = [-0.71, -0.31, 0.09, 0.49]
        else:
            coordenadas = [-0.51, -0.11, 0.29, 0.69]
        for i in coordenadas:
            # creamos una luz para dama con las el centro y color correspondiente
            ldama = crear_dama(i, j, color[0], color[1], color[2], radioDamas)
            # vbo para la figura dama
            vboLDama = glGenBuffers(1)
            # unir dama a su buffer
            unir_bufferVBO(ldama, vboLDama)
            # dibujo dama
            dibujo_figura(ldama, vboLDama)
        fila += 1

    # SOMBRA DAMAS:-----------------------------------------------------------------
    radioDamas = 0.080
    color = (0.329, 0.298, 0.231)
    fila = 1

    for j in [0.69, 0.49, 0.29, -0.31, -0.51, -0.71]:
        if fila % 2 == 1:
            coordenadas = [-0.693, -0.293, 0.107, 0.507]
        else:
            coordenadas = [-0.493, -0.093, 0.307, 0.707]
        for i in coordenadas:
            # creamos una dama con las el centro y color correspondiente
            sdama = crear_dama(i, j, color[0], color[1], color[2], radioDamas)
            # vbo para la figura dama
            vboSDama = glGenBuffers(1)
            # unir dama a su buffer
            unir_bufferVBO(sdama, vboSDama)
            # dibujo dama
            dibujo_figura(sdama, vboSDama)
        fila += 1

    # DAMAS:--------------------------------------------------------------------
    radioDamas= 0.085
    color1 = (0.117, 0.333, 0.423)  # originalmente rojo puro
    color2 = (0.878, 0.219, 0.109)  # originalmente azul puro
    fila=1

    for j in [0.7, 0.5, 0.3, -0.3, -0.5, -0.7]:
        if j>0:
            color = color1
        else:
            color = color2
        if fila%2 == 1:
            coordenadas = [-0.7, -0.3, 0.1, 0.5]
        else:
            coordenadas = [-0.5, -0.1, 0.3, 0.7]
        for i in coordenadas:
            # creamos una dama con las el centro y color correspondiente
            dama = crear_dama(i, j, color[0], color[1], color[2], radioDamas)
            # vbo para la figura dama
            vboDama = glGenBuffers(1)
            # unir dama a su buffer
            unir_bufferVBO(dama, vboDama)
            # dibujo dama
            dibujo_figura(dama, vboDama)
        fila += 1

    # FINAL DEL CODIGO NO TOCAR----------------------------------------------------------------------
    # sin modificaciones

    # Moving our draw to the active color buffer
    glfw.swap_buffers(window)

    # Waiting to close the window
    while not glfw.window_should_close(window):
        # Getting events from GLFW
        glfw.poll_events()

    glfw.terminate()