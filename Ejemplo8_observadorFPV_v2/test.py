from __future__ import division
import pygame
import numpy as np
from pygame.constants import *
from OpenGL.GL import *
from OpenGL.GL import shaders
from OpenGL.GLU import *
from OpenGL.arrays import vbo

pygame.init()
pygame.display.set_mode((800, 600), DOUBLEBUF | OPENGL)

# Initialize OpenGL settings for 3D
glClearColor(0.1, 0.1, 0.1, 1)
glEnable(GL_DEPTH_TEST)

# Define some basic shaders for 3D rendering
vertex_shader = """
#version 330
layout(location = 0) in vec3 position;
uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;
void main()
{
    gl_Position = projection * view * model * vec4(position, 1.0);
}
"""
fragment_shader = """
#version 330
out vec4 FragColor;
void main()
{
    FragColor = vec4(1.0, 0.5, 0.2, 1.0);
}
"""

shader_program = shaders.compileProgram(
    shaders.compileShader(vertex_shader, GL_VERTEX_SHADER),
    shaders.compileShader(fragment_shader, GL_FRAGMENT_SHADER)
)

# Define a simple cube
vertices = np.array([
    -0.5, -0.5, -0.5,
     0.5, -0.5, -0.5,
     0.5,  0.5, -0.5,
    -0.5,  0.5, -0.5,
    -0.5, -0.5,  0.5,
     0.5, -0.5,  0.5,
     0.5,  0.5,  0.5,
    -0.5,  0.5,  0.5,
], dtype=np.float32)

indices = np.array([
    0, 1, 2, 2, 3, 0,  # Back face
    4, 5, 6, 6, 7, 4,  # Front face
    0, 1, 5, 5, 4, 0,  # Bottom face
    2, 3, 7, 7, 6, 2,  # Top face
    0, 3, 7, 7, 4, 0,  # Left face
    1, 2, 6, 6, 5, 1   # Right face
], dtype=np.uint32)

vbo = vbo.VBO(vertices)
ebo = vbo.VBO(indices, target=GL_ELEMENT_ARRAY_BUFFER)

# Create a texture for the text
texture = glGenTextures(1)

# Main game loop
cont = 0
playing = True
while playing:
    for event in pygame.event.get():
        if event.type in (MOUSEBUTTONDOWN, KEYDOWN):
            playing = False

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # Render the 3D cube
    glUseProgram(shader_program)
    model = np.identity(4, dtype=np.float32)
    view = np.identity(4, dtype=np.float32)
    projection = np.identity(4, dtype=np.float32)
    glUniformMatrix4fv(glGetUniformLocation(shader_program, "model"), 1, GL_FALSE, model)
    glUniformMatrix4fv(glGetUniformLocation(shader_program, "view"), 1, GL_FALSE, view)
    glUniformMatrix4fv(glGetUniformLocation(shader_program, "projection"), 1, GL_FALSE, projection)

    vbo.bind()
    glEnableVertexAttribArray(0)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)
    ebo.bind()
    glDrawElements(GL_TRIANGLES, len(indices), GL_UNSIGNED_INT, None)
    vbo.unbind()
    ebo.unbind()
    glDisableVertexAttribArray(0)
    glUseProgram(0)

    # Render the 2D text
    img = pygame.font.Font(None, 50).render(f"Balas: {cont//100}", True, (255, 255, 255))
    w, h = img.get_size()
    glBindTexture(GL_TEXTURE_2D, texture)
    glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, w, h, 0, GL_RGBA, GL_UNSIGNED_BYTE, pygame.image.tostring(img, "RGBA", 1))
    glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, 800, 0, 600, -1, 1)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glEnable(GL_TEXTURE_2D)
    glDisable(GL_DEPTH_TEST)
    glDisable(GL_CULL_FACE)
    glDisable(GL_LIGHTING)

    glBegin(GL_QUADS)
    x0, y0 = 10, 10
    for dx, dy in [(0, 0), (0, 1), (1, 1), (1, 0)]:
        glTexCoord2f(dx, dy)
        glVertex2f(x0 + dx * w, y0 + dy * h)
    glEnd()

    cont += 1

    pygame.display.flip()

pygame.quit()
