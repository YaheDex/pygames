import pygame
from pygame.locals import *

# Cargamos las bibliotecas de OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import numpy as np

pygame.init()

screen_width = 900
screen_height = 600
#vc para el obser.
FOVY=60.0
ZNEAR=0.01
ZFAR=500.0
#Variables para definir la posicion del observador
#gluLookAt(EYE_X,EYE_Y,EYE_Z,CENTER_X,CENTER_Y,CENTER_Z,UP_X,UP_Y,UP_Z)
EYE_X=10.0
EYE_Y=10.0
EYE_Z=10.0
CENTER_X=0
CENTER_Y=0
CENTER_Z=0
UP_X=0
UP_Y=1
UP_Z=0
#Variables para dibujar los ejes del sistema
X_MIN=-500
X_MAX=500
Y_MIN=-500
Y_MAX=500
Z_MIN=-500
Z_MAX=500


def Axis():
    glShadeModel(GL_FLAT)
    glLineWidth(3.0)
    #X axis in red
    glColor3f(1.0,0.0,0.0)
    glBegin(GL_LINES)
    glVertex3f(X_MIN,0.0,0.0)
    glVertex3f(X_MAX,0.0,0.0)
    glEnd()
    #Y axis in green
    glColor3f(0.0,1.0,0.0)
    glBegin(GL_LINES)
    glVertex3f(0.0,Y_MIN,0.0)
    glVertex3f(0.0,Y_MAX,0.0)
    glEnd()
    #Z axis in blue
    glColor3f(0.0,0.0,1.0)
    glBegin(GL_LINES)
    glVertex3f(0.0,0.0,Z_MIN)
    glVertex3f(0.0,0.0,Z_MAX)
    glEnd()
    glLineWidth(1.0)

def Init():
    screen = pygame.display.set_mode(
        (screen_width, screen_height), DOUBLEBUF | OPENGL)
    pygame.display.set_caption("OpenGL: ejes 3D")

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(FOVY, screen_width/screen_height, ZNEAR, ZFAR)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(EYE_X,EYE_Y,EYE_Z,CENTER_X,CENTER_Y,CENTER_Z,UP_X,UP_Y,UP_Z)
    glClearColor(0,0,0,0)
    glEnable(GL_DEPTH_TEST)

    glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
    glShadeModel(GL_FLAT)  

v_piramide = np.array([[-1.0, 0.0, 1.0], [1.0, 0.0, 1.0], [1.0, 0.0, -1.0], [-1.0, 0.0, -1.0], [0.0, 2.0, 0.0]])
    
def piramide():
    glColor3f(1.0, 1.0, 1.0)
    glBegin(GL_QUADS)
    glVertex3fv(v_piramide[0])
    glVertex3fv(v_piramide[1])
    glVertex3fv(v_piramide[2])
    glVertex3fv(v_piramide[3])
    glEnd()
    glBegin(GL_LINES)
    glVertex3fv(v_piramide[0])
    glVertex3fv(v_piramide[4])
    glEnd()
    glBegin(GL_LINES)
    glVertex3fv(v_piramide[1])
    glVertex3fv(v_piramide[4])
    glEnd()
    glBegin(GL_LINES)
    glVertex3fv(v_piramide[2])
    glVertex3fv(v_piramide[4])
    glEnd()
    glBegin(GL_LINES)
    glVertex3fv(v_piramide[3])
    glVertex3fv(v_piramide[4])
    glEnd()
r = 0
r1 = 0
r2 = 0
Init()
done = False
while not done:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    # Guardar e0, a partir de aquí se dibuja el primer sistema de referencia junto con la pirámide
    glPushMatrix()
    # e0 -> e1 y así sucesivamente
    Axis()
    # e0 
    piramide() 
    # e1
    glRotate(r,0.0,1.0,0.0)
    glTranslatef(5.0,0.0,5.0)
    # e2
    glScalef(0.70,0.70,0.70)
    piramide()
    glPopMatrix()
    # e0
    glPushMatrix()
    # e3
    glTranslatef(-5.0, 0.0, 0.0)
    # e4
    glRotatef(r,0.0,1.0,0.0)
    # e5
    glScalef(3.0,3.0,3.0)
    # dibujo
    piramide()
    glPopMatrix()
    
    r+=1
    if r1 < 3:
        r1+=1
        r2+=1
        
    else:
        r1-=1
        r2-=1
    
    pygame.display.flip()
    pygame.time.wait(10)

pygame.quit()