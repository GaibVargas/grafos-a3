from typing import TextIO
import math

class Grafo:
  def __init__(self):
    self.vertices = 0
    self.arestas = 0
    self.vetor_arestas = []
    self.rotulos: list[str] = []
    self.custo: list[list[float]]
    self.dirigido = False
    # Usados para identificação de grafos bipartidos
    self.x = set()
    self.y = set()
  
  def iniciar(self, grafo: 'Grafo', arestas: 'list[tuple[int, int]]'):
    self.vertices = grafo.qtdVertices()
    self.arestas = grafo.qtdArestas()
    self.vetor_arestas = arestas.copy()
    self.rotulos = grafo.rotulos.copy()
    self.dirigido = grafo.dirigido
    self.iniciar_matriz_custo()
    for arco in self.vetor_arestas:
      self.custo[arco[0] - 1][arco[1] - 1] = grafo.custo[arco[1] - 1][arco[0] - 1]
  
  def iniciarGrafoResidual(self, grafo: 'Grafo'):
    self.vertices = grafo.qtdVertices()
    self.arestas = grafo.qtdArestas()
    self.vetor_arestas = grafo.vetor_arestas.copy()
    self.rotulos = grafo.rotulos.copy()
    self.dirigido = grafo.dirigido
    self.iniciar_matriz_custo_residual()
    vertices_artificiais = 0
    pular_aresta = []
    for i in range(self.vertices):
      for j in range(self.vertices):
        if ((i + 1, j + 1) in grafo.vetor_arestas) and ((j + 1, i + 1) in grafo.vetor_arestas) and ((i, j) not in pular_aresta and (j, i) not in pular_aresta):
          self.custo.append([0] * (self.vertices + vertices_artificiais))
          for linha in self.custo:
            linha.append(0)
          vertices_artificiais += 1
          pular_aresta.append((j, i))
          self.custo[i][self.vertices - 1 + vertices_artificiais] = grafo.custo[i][j]
          self.custo[self.vertices - 1 + vertices_artificiais][i] = 0
          self.custo[self.vertices - 1 + vertices_artificiais][j] = grafo.custo[i][j]
          self.custo[j][self.vertices - 1 + vertices_artificiais] = 0
          self.custo[i][j] = 0
        elif grafo.custo[i][j] != math.inf:
          self.custo[i][j] = grafo.custo[i][j]
    self.vertices += vertices_artificiais

  def qtdVertices(self):
    return self.vertices
  
  def qtdArestas(self):
    return self.arestas

  def grau(self, vertice: int):
    if (vertice > self.vertices):
      raise Exception("Vértice não existe")
    if (vertice <= 0):
      raise Exception("Vértice é um número positivo")
    vizinhos = self.vizinhos(vertice)
    return len(vizinhos)

  def rotulo(self, vertice: int):
    if (vertice > self.vertices):
      raise Exception("Vértice não existe")
    if (vertice <= 0):
      raise Exception("Vértice é um número positivo")
    return self.rotulos[vertice - 1]

  def vizinhos(self, vertice: int):
    if (vertice > self.vertices):
      raise Exception("Vértice não existe")
    if (vertice <= 0):
      raise Exception("Vértice é um número positivo")
    vizinhos = []
    vertice = vertice - 1
    for i in range(self.vertices):
      if (self.custo[vertice][i] != 0 and self.custo[vertice][i] != math.inf):
        vizinhos.append(i + 1)
    return vizinhos

  def haAresta(self, origem: int, destino: int):
    if (origem > self.vertices or destino > self.vertices):
      raise Exception("Vértices inválidos")
    if (origem <= 0 or destino <= 0):
      raise Exception("Vértice é um número positivo")
    
    custo = self.custo[origem - 1][destino - 1]
    if (custo == math.inf):
      return False
    return True

  def peso(self, origem: int, destino: int):
    if (origem > self.vertices or destino > self.vertices):
      raise Exception("Vértices inválidos")
    if (origem <= 0 or destino <= 0):
      raise Exception("Vértice é um número positivo")
    return self.custo[origem - 1][destino - 1]

  def ler(self, arquivo: TextIO):
    lendo_vertices = False
    lendo_arestas = False
    while True:
      linha = arquivo.readline()
      if not linha:
        break
      
      if (linha.find("*vertices") != -1):
        [_, numero] = linha.split()
        self.vertices = int(numero)
        self.iniciar_matriz_custo()
        lendo_vertices = True
        continue

      if (linha.find("*edges") != -1):
        lendo_vertices = False
        lendo_arestas = True
        continue

      if (linha.find("*arcs") != -1):
        lendo_vertices = False
        lendo_arestas = True
        self.dirigido = True
        continue

      if (lendo_vertices):
        if (linha.find('"') != -1):
          rotulo = linha[linha.find('"'):len(linha)-1]
        else:
          [_, rotulo] = linha.split()
        self.rotulos.append(rotulo)
      elif (lendo_arestas):
        [origem, destino, custo] = linha.split()
        origem = int(origem)
        self.x.add(origem)
        destino = int(destino)
        self.y.add(destino)
        custo = float(custo)
        self.custo[origem - 1][destino - 1] = custo
        if (not self.dirigido):
          self.custo[destino - 1][origem - 1] = custo
        self.vetor_arestas.append((origem, destino))
        self.arestas += 1
  
  def iniciar_matriz_custo(self):
    self.custo = []
    for i in range(self.vertices):
      self.custo.append([math.inf] * self.vertices)
    for i in range(self.vertices):
      self.custo[i][i] = 0
  
  def iniciar_matriz_custo_residual(self):
    self.custo = []
    for i in range(self.vertices):
      self.custo.append([0] * self.vertices)