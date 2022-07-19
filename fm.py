import sys
from typing import TextIO
from Grafo import Grafo

def obterCapacidadeMinima(gf: Grafo, p: list[int]):
  minimo: int
  for idx in range(len(p) - 1):
    custo = gf.custo[p[idx]][p[idx + 1]]
    if idx == 0:
      minimo = custo
    else:
      if custo < minimo:
        minimo = custo
  return minimo

def caminhoAumentante(gf: Grafo, s: int, t: int):
  C = [False] * gf.qtdVertices()
  A = [None] * gf.qtdVertices()
  C[s] = True
  Q = [s]
  while len(Q) > 0:
    u = Q.pop(0)
    for v in gf.vizinhos(u + 1):
      v -= 1
      if (not C[v]) and (gf.custo[u][v] > 0):
        C[v] = True
        A[v] = u
        if v == t:
          p = [t]
          w = t
          while w != s:
            w = A[w]
            p.insert(0, w)
          return p
        Q.append(v)
  return None

def edmondsKarp(gf: Grafo, s: int, t: int):
  s -= 1
  t -= 1
  F = 0
  p = caminhoAumentante(gf, s, t)
  while p != None:
    minimo = obterCapacidadeMinima(gf, p)
    for i in range(len(p) - 1):
      gf.custo[p[i]][p[i + 1]] = gf.custo[p[i]][p[i + 1]] - minimo
      gf.custo[p[i + 1]][p[i]] = gf.custo[p[i + 1]][p[i]] + minimo
    F += minimo
    p = caminhoAumentante(gf, s, t)
  return F

def main():
  grafo = Grafo()
  if (len(sys.argv) < 3):
    print("É necessário indicar um arquivo e dois vértices como argumento do programa\npython fm.py [arquivo] [vértice origem] [vértice destino]")
    return

  try:
    s = int(sys.argv[2])
    t = int(sys.argv[3])
  except:
    print("Os vértices precisam ser números inteiros")
    return

  file_name = sys.argv[1]
  file: TextIO = None

  try:
    file = open(file_name, 'r')
  except:
    print("Erro ao abrir o arquivo. Verifique se o nome do arquivo informado está correto")
    return
  
  grafo.ler(file)

  if (s - 1 < 0) or (s > grafo.qtdVertices()) or (t - 1 < 0) or (t > grafo.qtdVertices()):
    print(f"Os vértices precisam estar dentro do intervalo [1, {grafo.qtdVertices()}]")
    return

  gf = Grafo()
  gf.iniciarGrafoResidual(grafo)
  print(f'Fluxo máximo do vértice de origem {s} ao vértice de destino {t}: ', end="")
  print(edmondsKarp(gf, s, t))
  
main()