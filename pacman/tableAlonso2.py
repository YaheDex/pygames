import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math
import csv

# Screen dimensions
screen_width = 500
screen_height = 500

# Observer parameters
FOVY = 60.0
ZNEAR = 0.01
ZFAR = 1000
EYE_X = 500
EYE_Y = 250
EYE_Z = 500.0
CENTER_X = 200
CENTER_Y = 0
CENTER_Z = 206
UP_X = 0
UP_Y = 1
UP_Z = 0

# Maze control matrix
control_matrix = [
    [10, 0, 14, 0, 11, 10, 0, 14, 0, 11],
    [17, 0, 18, 14, 16, 16, 14, 18, 0, 15],
    [12, 0, 15, 12, 11, 10, 13, 17, 0, 13],
    [0, 0, 0, 10, 16, 16, 11, 0, 0, 0],
    [19, 0, 18, 15, 0, 0, 17, 18, 0, 20],
    [0, 0, 0, 17, 0, 0, 15, 0, 0, 0],
    [10, 0, 18, 16, 11, 10, 16, 18, 0, 11],
    [12, 11, 17, 14, 16, 16, 14, 15, 10, 13],
    [10, 16, 13, 12, 11, 10, 13, 12, 16, 11],
    [12, 0, 0, 0, 16, 16, 0, 0, 0, 13]
]

# Initialize Pygame
pygame.init()

# Function to load textures
def load_texture(filepath):
    textures = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, textures)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    image = pygame.image.load(filepath).convert()
    w, h = image.get_rect().size
    image_data = pygame.image.tostring(image, "RGBA")
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, w, h, 0, GL_RGBA, GL_UNSIGNED_BYTE, image_data)
    glGenerateMipmap(GL_TEXTURE_2D)
    return textures

# Function to get directions at an intersection
def get_directions(row, column):
    intersection = control_matrix[row][column]
    directions = []
    if intersection == 10:
        directions.extend(['down', 'right'])
    elif intersection == 11:
        directions.extend(['down', 'left'])
    elif intersection == 12:
        directions.extend(['up', 'right'])
    elif intersection == 13:
        directions.extend(['up', 'left'])
    elif intersection == 14:
        directions.extend(['down', 'left', 'right'])
    elif intersection == 15:
        directions.extend(['up', 'down', 'left'])
    elif intersection == 16:
        directions.extend(['up', 'left', 'right'])
    elif intersection == 17:
        directions.extend(['up', 'down', 'right'])
    elif intersection == 18:
        directions.extend(['up', 'down', 'left', 'right'])
    elif intersection == 19:
        directions.append('right')
    elif intersection == 20:
        directions.append('left')
    return directions

# Initial position
current_position = (0, 0)

# Function to move Pac-Man
def move_pacman(direction):
    global current_position
    row, column = current_position
    if direction == 'up' and 'up' in get_directions(row, column):
        row -= 1
    elif direction == 'down' and 'down' in get_directions(row, column):
        row += 1
    elif direction == 'left' and 'left' in get_directions(row, column):
        column -= 1
    elif direction == 'right' and 'right' in get_directions(row, column):
        column += 1
    current_position = (row, column)

# Function to draw the coordinate axes
def draw_axes():
    glShadeModel(GL_FLAT)
    glLineWidth(3.0)
    # X axis in red
    glColor3f(1.0, 0.0, 0.0)
    glBegin(GL_LINES)
    glVertex3f(-500, 0.0, 0.0)
    glVertex3f(500, 0.0, 0.0)
    glEnd()
    # Y axis in green
    glColor3f(0.0, 1.0, 0.0)
    glBegin(GL_LINES)
    glVertex3f(0.0, -500, 0.0)
    glVertex3f(0.0, 500, 0.0)
    glEnd()
    # Z axis in blue
    glColor3f(0.0, 0.0, 1.0)
    glBegin(GL_LINES)
    glVertex3f(0.0, 0.0, -500)
    glVertex3f(0.0, 0.0, 500)
    glEnd()
    glLineWidth(1.0)

# Function to draw the textured plane
def draw_textured_plane():
    glPushMatrix()
    glTranslatef(200, 0, 206)
    # Activate textures
    glEnable(GL_TEXTURE_2D)
    # Front face
    glBindTexture(GL_TEXTURE_2D, texture_board)
    glBegin(GL_QUADS)
    # Dimensions of the board: 400, 0, 412
    glTexCoord2f(0.0, 0.0)
    glVertex3d(-200, 0, -206)
    glTexCoord2f(0.0, 1.0)
    glVertex3d(-200, 0, 206)
    glTexCoord2f(1.0, 1.0)
    glVertex3d(200, 0, 206)
    glTexCoord2f(1.0, 0.0)
    glVertex3d(200, 0, -206)
    glEnd()
    glPopMatrix()
    glDisable(GL_TEXTURE_2D)

# Initialize OpenGL
screen = pygame.display.set_mode((screen_width, screen_height), DOUBLEBUF | OPENGL)
pygame.display.set_caption("OpenGL: Pac-Man")
glMatrixMode(GL_PROJECTION)
glLoadIdentity()
gluPerspective(FOVY, screen_width / screen_height, ZNEAR, ZFAR)
glMatrixMode(GL_MODELVIEW)
glLoadIdentity()
gluLookAt(EYE_X, EYE_Y, EYE_Z, CENTER_X, CENTER_Y, CENTER_Z, UP_X, UP_Y, UP_Z)
glClearColor(0, 0, 0, 0)
glEnable(GL_DEPTH_TEST)
glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
texture_board = load_texture("pacman/tablero.bmp")

# Main loop
done = False
dir = "na"
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                dir = "right"
            elif event.key == pygame.K_LEFT:
                dir = "left"
            elif event.key == pygame.K_UP:
                dir = "up"
            elif event.key == pygame.K_DOWN:
                dir = "down"
            elif event.key == pygame.K_ESCAPE:
                done = True

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    draw_axes()
    draw_textured_plane()
    move_pacman(dir)
    pygame.display.flip()
    pygame.time.wait(5)

pygame.quit()
