import math
import sys
from typing import TextIO
from Grafo import Grafo

def BFS(grafo: Grafo, mate: list[int], D: dict[int, int]):
  Q = []
  for x in grafo.x:
    x -= 1
    if mate[x] == None:
      D[x] = 0
      Q.append(x)
    else:
      D[x] = math.inf
  D[None] = math.inf
  while len(Q) > 0:
    x = Q.pop(0)
    if D[x] < D[None]:
      for y in grafo.vizinhos(x + 1):
        y -= 1
        if D[mate[y]] == math.inf:
          D[mate[y]] = D[x] + 1
          Q.append(mate[y])
  return D[None] != math.inf

def DFS(grafo: Grafo, mate: list[int], x: int, D: dict[int, int]):
  if x == None:
    return True
  for y in grafo.vizinhos(x + 1):
    y -= 1
    if D[mate[y]] == D[x] + 1:
      if DFS(grafo, mate, mate[y], D):
        mate[y] = x
        mate[x] = y
        return True
  D[x] = math.inf
  return False

def hopcroftKarp(grafo: Grafo):
  m = 0
  mate = [None] * grafo.qtdVertices()
  D = {}
  for v in range(grafo.qtdVertices()):
    D[v] = math.inf
  while BFS(grafo, mate, D):
    for x in grafo.x:
      x -= 1
      if mate[x] == None:
        if DFS(grafo, mate, x, D):
          m += 1
  return (m, mate)

def printArestas(mate: list[int]):
  arestas = set()
  for x, y in enumerate(mate):
    if x < y:
      arestas.add((x + 1, y + 1))
    else:
      arestas.add((y + 1, x + 1))
  for idx, aresta in enumerate(arestas):
    print('{{{0}, {1}}}'.format(aresta[0], aresta[1]), end=', ' if idx != len(arestas) - 1 else '\n')

def main():
  grafo = Grafo()
  if (len(sys.argv) < 2):
    print("É necessário indicar um arquivo como argumento do programa\npython emparelhamento.py [arquivo]")
    return

  file_name = sys.argv[1]
  file: TextIO = None

  try:
    file = open(file_name, 'r')
  except:
    print("Erro ao abrir o arquivo. Verifique se o nome do arquivo informado está correto")
    return
  
  grafo.ler(file)
  tamanho, mate = hopcroftKarp(grafo)
  print(f'Número de arestas: {tamanho}')
  print('Arestas: ', end='')
  printArestas(mate)
  
main()