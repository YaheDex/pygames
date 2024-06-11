import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import sys
sys.path.append('..')
from Cubo import Cubo
from Player import Player
from bala import Bala

filename1 = "danp.jpg"
textures = []
screen_width = 800
screen_height = 800
FOVY = 60.0
ZNEAR = 1.0
ZFAR = 900.0
EYE_X = 0.0
EYE_Y = 5.0
EYE_Z = 0.0
CENTER_X = 1.0
CENTER_Y = 5.0
CENTER_Z = 0.0
UP_X = 0
UP_Y = 1
UP_Z = 0
theta = 0
is_jumping = False
jump_height = 0.0
X_MIN = -500
X_MAX = 500
Y_MIN = -500
Y_MAX = 500
Z_MIN = -500
Z_MAX = 500
DimBoard = 200
# cubos = [Cubo(DimBoard, 1, 200, 5, 0), Cubo(DimBoard, 0, DimBoard, 2.5, DimBoard), Cubo(DimBoard, 0, DimBoard-10, 2, DimBoard)]
dansito = Cubo(DimBoard, 1.0, 11)
jugador = Player()
pygame.init()
pygame.mixer.init()

plataforma = Cubo(5, 0.0, 6)  # Ajusta los parámetros según sea necesario
plataforma.Position = [10, 0, 20]  # Posición de la plataforma en el mundo
plataforma2 = Cubo(5, 0.0, 11)  # Ajusta los parámetros según sea necesario
plataforma2.Position = [20, 6, 30]  # Posición de la plataforma en el mundo
listacubos = [plataforma, plataforma2]


cooldown = 10
global contar
contar = False

def Axis():
    glShadeModel(GL_FLAT)
    glLineWidth(3.0)
    glColor3f(1.0, 0.0, 0.0)
    glBegin(GL_LINES)
    glVertex3f(X_MIN, 0.0, 0.0)
    glVertex3f(X_MAX, 0.0, 0.0)
    glEnd()
    glColor3f(0.0, 1.0, 0.0)
    glBegin(GL_LINES)
    glVertex3f(0.0, Y_MIN, 0.0)
    glVertex3f(0.0, Y_MAX, 0.0)
    glEnd()
    glColor3f(0.0, 0.0, 1.0)
    glBegin(GL_LINES)
    glVertex3f(0.0, 0.0, Z_MIN)
    glVertex3f(0.0, 0.0, Z_MAX)
    glEnd()
    glLineWidth(1.0)

def Texturas(filepath):
    textures.append(glGenTextures(1))
    id = len(textures) - 1
    glBindTexture(GL_TEXTURE_2D, textures[id])
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    image = pygame.image.load(filepath).convert()
    w, h = image.get_rect().size
    image_data = pygame.image.tostring(image, "RGBA")
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, w, h, 0, GL_RGBA, GL_UNSIGNED_BYTE, image_data)
    glGenerateMipmap(GL_TEXTURE_2D)

def Init():
    screen = pygame.display.set_mode((screen_width, screen_height), DOUBLEBUF | OPENGL)
    pygame.display.set_caption("OpenGL: cubos")
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(FOVY, screen_width / screen_height, ZNEAR, ZFAR)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(EYE_X, EYE_Y, EYE_Z, CENTER_X, CENTER_Y, CENTER_Z, UP_X, UP_Y, UP_Z)
    glClearColor(0, 0, 0, 0)
    glEnable(GL_DEPTH_TEST)
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
    Texturas(filename1)

def display():
    global contar
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    Axis()
    glColor3f(0.3, 0.3, 0.3)
    glBegin(GL_QUADS)
    glVertex3d(-DimBoard, 0, -DimBoard)
    glVertex3d(-DimBoard, 0, DimBoard)
    glVertex3d(DimBoard, 0, DimBoard)
    glVertex3d(DimBoard, 0, -DimBoard)
    glEnd()
    jugador.update()
    jugador.checkCol(listacubos)
    for plataforma in listacubos:
        plataforma.drawCube(textures, 0, [255, 255, 255])
    
    if not contar:
        dansito.drawCube(textures, 0, [255, 255, 255])
    else:
        dansito.drawCube(textures, 0, [255, 0, 0])
    
    
    for obj in balas:
        obj.drawBala()
        obj.update()
        if obj.checkCol(dansito):
            print("le pegaste a dan")
            contar = True
            hit.play()
            obj.vive = False

done = False
Init()
global balas
balas = []
boom = pygame.mixer.Sound("disparo.mp3")
hit = pygame.mixer.Sound("hitmarker.mp3")



while not done:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                done = True
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                boom.play()
                balas.append(Bala(2.5, jugador.Position, jugador.newDir))
        
                
    # voy a hacer un for para verificar las balas q siguen vivas equisdé
    for obj in balas:
        if not obj.vive:
            balas.remove(obj)    
    
    if contar:
        cooldown -= 1
        
    if not cooldown:
        cooldown = 10
        contar = False    
            
    glLoadIdentity()
    verX = jugador.Position[0] + jugador.newDir[0]
    verZ = jugador.Position[2] + jugador.newDir[2]
    gluLookAt(jugador.Position[0], jugador.Position[1], jugador.Position[2], verX, jugador.Position[1], verZ, UP_X, UP_Y, UP_Z)
    dansito.chase_player(jugador.Position, 0.7)
    if dansito:
        if dansito.check_collision(jugador.Position):
                print("¡Has perdido!")
                done = True
                break
    
    display()
    pygame.display.flip()
    pygame.time.wait(10)

pygame.quit()
