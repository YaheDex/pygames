import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

# Vertices de la pirámide
vertices = [
    [0, 4, 0],  # Punto superior
    [-5, 0, 5],  # Base: esquina inferior izquierda
    [5, 0, 5],   # Base: esquina inferior derecha
    [5, 0, -5],  # Base: esquina superior derecha
    [-5, 0, -5]  # Base: esquina superior izquierda
]

# Aristas de la pirámide
edges = [
    (0, 1),
    (0, 2),
    (0, 3),
    (0, 4),
    (1, 2),
    (2, 3),
    (3, 4),
    (4, 1)
]

def Piramide():
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()

def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
    gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -10)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        glRotatef(1, 3, 1, 1)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        Piramide()
        pygame.display.flip()
        pygame.time.wait(10)

main()
