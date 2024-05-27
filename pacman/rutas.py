# import the library
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
from PIL import Image

# HOLA TILINES !!!
#holaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
# mejor q replit
#rojo

# okei pero cómo se corren los códigos
# menea tu chapa
# hoy es 12 de abril
# hoy se celebra el dia mundial contra el alonso

import os
import numpy as np
import pandas as pd


BASE_PATH = os.path.abspath(os.path.dirname(__file__))
CSV_FILE = os.path.join(BASE_PATH, 'csv_file.csv')

path = []
grid = []

# navigation map

matrix = [
  [1, 1, 1, 0, 1, 1],
  [1, 0, 1, 1, 1, 1],
  [1, 1, 1, 0, 1, 1]]


def finding(matrix, nstart, nend): 
    global path
    global grid
    # 1. create the grid with the nodes 
    grid = Grid(matrix=matrix)
    # get start and end point 
    start = grid.node(nstart[0], nstart[1])
    end = grid.node(nend[0], nend[1])
    # create a finder with A* algorithm
    finder = AStarFinder() 
    # returns a list with the path and the amount of times the finder had to run to get the path 
    path, runs = finder.find_path(start, end, grid)


def cargar_imagen_como_matriz(ruta):
    imagen = Image.open(ruta)
    # Convierte la imagen en escala de grises y luego en una matriz NumPy
    matriz = np.array(imagen.convert('L'))
    # Normaliza los valores de la matriz para que estén en el rango de 0 a 1
    matriz = matriz / 255.0
    return matriz

# Carga la imagen como una matriz
matriz_tablero = cargar_imagen_como_matriz("tablero.bmp")

print("Dimensiones de la matriz del tablero:", matriz_tablero.shape)
print("Matriz del tablero:")
print(matriz_tablero)

#main program ---------------------------------------
finding(matrix, (0,0), (5,2))
# print result 
for point in path:
    x = point.x
    y = point.y
    print(x," ", y)

path = []
grid = []

# reading a csv file
matrix2 = np.array(pd.io.parsers.read_csv(CSV_FILE, header=None)).astype("int")
print(matrix2)
finding(matrix2, (0,0), (3, 4))
# print result 
for point in path:
    x = point.x
    y = point.y
    print(x," ", y)


  
