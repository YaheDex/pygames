import pygame
from pygame.locals import *

# Cargamos las bibliotecas de OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import math

# Se carga el archivo de la clase Cubo
import sys
sys.path.append('..')
from Pacman import Pacman

screen_width = 500
screen_height = 500
#vc para el obser.
FOVY=60.0
ZNEAR=0.01
ZFAR=1000
#Variables para definir la posicion del observador
EYE_X = 500
EYE_Y = 250
EYE_Z = 500.0
CENTER_X = 200
CENTER_Y = 0
CENTER_Z = 206
UP_X=0
UP_Y=1
UP_Z=0
gluLookAt(EYE_X,EYE_Y,EYE_Z,CENTER_X,CENTER_Y,CENTER_Z,UP_X,UP_Y,UP_Z)
#Variables para dibujar los ejes del sistema
X_MIN=-500
X_MAX=500
Y_MIN=-500
Y_MAX=500
Z_MIN=-500
Z_MAX=500

#Variables para el control del observador
theta = 0.0
radius = 300

#Arreglo para el manejo de texturas
textures = []
filename1 = "pacman/tablero.bmp"
filename2 = "pacman/pacman.bmp"

pygame.init()

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

def Texturas(filepath):
    textures.append(glGenTextures(1))
    id = len(textures) - 1
    glBindTexture(GL_TEXTURE_2D, textures[id])
    glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_WRAP_S, GL_CLAMP)
    glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_WRAP_T, GL_CLAMP)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    image = pygame.image.load(filepath).convert()
    w, h = image.get_rect().size
    image_data = pygame.image.tostring(image,"RGBA")
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, w, h, 0, GL_RGBA, GL_UNSIGNED_BYTE, image_data)
    glGenerateMipmap(GL_TEXTURE_2D) 

def Init():
    screen = pygame.display.set_mode(
        (screen_width, screen_height), DOUBLEBUF | OPENGL)
    pygame.display.set_caption("OpenGL: Pac-Man :v")

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(FOVY, screen_width/screen_height, ZNEAR, ZFAR)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(EYE_X,EYE_Y,EYE_Z,CENTER_X,CENTER_Y,CENTER_Z,UP_X,UP_Y,UP_Z)
    glClearColor(0,0,0,0)
    glEnable(GL_DEPTH_TEST)
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
    
    Texturas(filename1)
    Texturas(filename2)
    
    # CONSTRUCCIÓN DE OBJETO PACMAN
    global pacman
    pacman = Pacman(52, 376, 385, 1)


#Se mueve al observador circularmente al rededor del plano XZ a una altura fija (EYE_Y)
def lookat():
    global EYE_X
    global EYE_Z
    global radius
    EYE_X = (radius * (math.cos(math.radians(theta)) + math.sin(math.radians(theta)))) + 200
    EYE_Z = (radius * (-math.sin(math.radians(theta)) + math.cos(math.radians(theta)))) + 206
    glLoadIdentity()
    gluLookAt(EYE_X,EYE_Y,EYE_Z,CENTER_X,CENTER_Y,CENTER_Z,UP_X,UP_Y,UP_Z)
    

def PlanoTexturizado():
    #Activate textures
    glColor3f(255,255,255)
    glEnable(GL_TEXTURE_2D)
    #front face
    glBindTexture(GL_TEXTURE_2D, textures[0])    
    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 0.0)
    glVertex3d(0, 0, 0)
    glTexCoord2f(0.0, 1.0)
    
    # Dimensiones del tablero: 400, 0, 412
    
    glVertex3d(0, 0, 412)
    glTexCoord2f(1.0, 1.0)
    glVertex3d(400, 0, 412)
    glTexCoord2f(1.0, 0.0)
    glVertex3d(400, 0, 0)
    glEnd()              
    glDisable(GL_TEXTURE_2D)
    
    
def display(dir):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    Axis()
    PlanoTexturizado()
    # Pacman
    pacman.drawCube(textures,1)
    pacman.update(dir)
    
done = False
dir = "na"
Init()
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
           done = True
        # ------------- SECCIÓN PARA EL MOVIMIENTO DEL PACMAN -----------
        if event.type == pygame.KEYDOWN:            
            if event.key == pygame.K_d:
                dir = "right"
            if event.key == pygame.K_a:
                dir = "left"
            if event.key == pygame.K_w:
                dir = "up"
            if event.key == pygame.K_s:
                dir = "down"
                
            # ------------- FIN DE SECCIÓN PARA EL MOVIMIENTO DEL PACMAN -----------
            if event.key == pygame.K_ESCAPE:
                done = True

    display(dir)

    pygame.display.flip()
    pygame.time.wait(5)

pygame.quit()