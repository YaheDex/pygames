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
from Cubo import Cubo

filename1 = "Ejemplo8_observadorFPV_v2/Ejemplo8_observadorFPV_v2/danp.jpg"
textures = []
screen_width = 800
screen_height = 800
#vc para el obser.
FOVY=60.0
ZNEAR=1.0
ZFAR=900.0
#Variables para definir la posicion del observador
#gluLookAt(EYE_X,EYE_Y,EYE_Z,CENTER_X,CENTER_Y,CENTER_Z,UP_X,UP_Y,UP_Z)
EYE_X = 0.0
EYE_Y = 5.0
EYE_Z = 0.0
CENTER_X = 1.0
CENTER_Y = 5.0
CENTER_Z = 0.0
UP_X=0
UP_Y=1
UP_Z=0
theta = 0

is_jumping = False
jump_height = 0.0
#Variables para dibujar los ejes del sistema
X_MIN=-500
X_MAX=500
Y_MIN=-500
Y_MAX=500
Z_MIN=-500
Z_MAX=500
#Dimension del plano
DimBoard = 200
#Variable de control observador
dir = [1.0, 0.0, 0.0]

#Variables asociados a los objetos de la clase Cubo
#cubo = Cubo(DimBoard, 1.0)
cubos = []
ncubos = 2

#Variables para el control del observador
theta = 0.0
radius = 300

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
    screen = pygame.display.set_mode((screen_width, screen_height), DOUBLEBUF | OPENGL)
    pygame.display.set_caption("OpenGL: cubos")

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
    for i in range(ncubos):
        cubos.append(Cubo(DimBoard, 1.0))  
    
def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    Axis()
    #Se dibuja el plano gris
    glColor3f(0.3, 0.3, 0.3)
    glBegin(GL_QUADS)
    glVertex3d(-DimBoard, 0, -DimBoard)
    glVertex3d(-DimBoard, 0, DimBoard)
    glVertex3d(DimBoard, 0, DimBoard)
    glVertex3d(DimBoard, 0, -DimBoard)
    glEnd()
    #Se dibuja cubos
    for obj in cubos:
        obj.drawCube(textures,0)
        
def rotating(theta):
    global dir
    global CENTER_Y
    global EYE_X
    global EYE_Z
    newx = dir[0]*math.cos(math.radians(theta)) + math.sin(math.radians(theta))*dir[2]
    newz = dir[0]*math.sin(math.radians(theta)) + math.cos(math.radians(theta))*dir[2]
    newdir = [(newx),CENTER_Y,(newz)]
    return newdir

done = False
Init()
while not done:
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
            newdir = rotating(theta)
            EYE_X = EYE_X + newdir[0]
            EYE_Z = EYE_Z + newdir[2]
            CENTER_X = EYE_X + newdir[0]
            CENTER_Z = EYE_Z + newdir[2]
            glLoadIdentity()
            gluLookAt(EYE_X,EYE_Y,EYE_Z,CENTER_X,CENTER_Y,CENTER_Z,UP_X,UP_Y,UP_Z)        
    if keys[pygame.K_DOWN]:
            newdir = rotating(theta)
            EYE_X = EYE_X - newdir[0]
            EYE_Z = EYE_Z - newdir[2]
            CENTER_X = EYE_X + newdir[0]
            CENTER_Z = EYE_Z + newdir[2]
            glLoadIdentity()
            gluLookAt(EYE_X,EYE_Y,EYE_Z,CENTER_X,CENTER_Y,CENTER_Z,UP_X,UP_Y,UP_Z)
    if keys[pygame.K_RIGHT]:
            theta+=1
            newdir = rotating(theta)
            CENTER_X = EYE_X + newdir[0]
            CENTER_Z = EYE_Z + newdir[2]
            glLoadIdentity()
            gluLookAt(EYE_X,EYE_Y,EYE_Z,CENTER_X,CENTER_Y,CENTER_Z,UP_X,UP_Y,UP_Z)
    if keys[pygame.K_LEFT]:
            theta-=1
            newdir = rotating(theta)
            CENTER_X = EYE_X + newdir[0]
            CENTER_Z = EYE_Z + newdir[2]
            glLoadIdentity()
            gluLookAt(EYE_X,EYE_Y,EYE_Z,CENTER_X,CENTER_Y,CENTER_Z,UP_X,UP_Y,UP_Z)
    if keys[pygame.K_SPACE] and not is_jumping:
        is_jumping = True
        jump_height = 5.0  # Ajusta este valor según la altura que desees para el salto

    if is_jumping:
        print(jump_height)
        if jump_height > 0:
            EYE_Y += jump_height * 0.1  # Ajusta este valor para controlar la velocidad del salto
            CENTER_Y += jump_height * 0.1
            jump_height -= 0.01  # Ajusta este valor para controlar la velocidad de caída
        else:
            is_jumping = False
            EYE_Y = 5.0  # Restablece la altura original del jugador
            CENTER_Y = 5.0

           
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                done = True

    player_pos = [EYE_X, EYE_Y, EYE_Z]  # Asegúrate de actualizar esta posición según la lógica de tu jugador

    # Dentro del ciclo while not done:
    cubos[1].chase_player(player_pos, 0.1)
    if cubos[1].check_collision(player_pos):
            print("¡Has perdido!")
            done = True
            break
    
    display()

    pygame.display.flip()
    pygame.time.wait(10)

pygame.quit()