import sys
from typing import TextIO
from Grafo import Grafo

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
  gf = Grafo()
  gf.iniciarGrafoResidual(grafo)
  print(gf.qtdVertices())
  print(gf.custo)
  
main()