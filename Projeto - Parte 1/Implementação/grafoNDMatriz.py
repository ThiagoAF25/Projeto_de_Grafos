import networkx as nx
import matplotlib.pyplot as plt


class GrafoND:
  TAM_MAX_DEFAULT = 100
  MODELOS_DEFAULT = ()
  def __init__(self, n=TAM_MAX_DEFAULT, mapa={}):
    self.n = n  # número de vértices
    self.m = 0  # número de arestas
    self.mapa = mapa
    self.adj = [[float('inf') for i in range(n)] for j in range(n)]

  def insereV(self, sigla, nome):
    if sigla not in self.mapa:
      self.mapa[sigla] = [len(self.mapa), nome]
      self.n = len(self.mapa)
      for i in range(self.n - 1):
        self.adj[i].append(float('inf'))
      self.adj.append([float('inf') for z in range(self.n)])
      print("Vértice inserido")
      
  def removeV(self, nome):
    if nome in self.mapa:
      for i in range(self.n):
        self.adj[i].pop(self.mapa[nome][0])
      self.adj.pop(self.mapa[nome][0])
      for i in self.mapa.keys():
        if (self.mapa[nome][0] < self.mapa[i][0]):
          self.mapa[i][0] = self.mapa[i][0] - 1
      self.mapa.pop(nome, True)
      self.n = len(self.mapa)
      print("Vértice removido!")
      
  def insereA(self, v, w, dict):
    if v in self.mapa and w in self.mapa:
      if self.adj[self.mapa[v][0]][self.mapa[w][0]] == float('inf'):
        self.adj[self.mapa[v][0]][self.mapa[w][0]] = dict
        self.adj[self.mapa[w][0]][self.mapa[v][0]] = dict
        self.m += 1
        print("Aresta inserida!")

  def removeA(self, v, w):
    if v in self.mapa and w in self.mapa:
      if self.adj[self.mapa[v][0]][self.mapa[w][0]] != float('inf'):
        self.adj[self.mapa[v][0]][self.mapa[w][0]] = float('inf')
        self.adj[self.mapa[w][0]][self.mapa[v][0]] = float('inf')
        self.m -= 1
        print("Aresta removida!")


  def gravarTXT(self):
    lista =(list(self.mapa))
    with open("grafo.txt", "w") as arquivo:
      arquivo.write("2\n")
      arquivo.write(f"{self.n:2d}\n")
      for key,value in self.mapa.items():
        arquivo.write(f"{key} {self.mapa[key][1]}\n")
      arquivo.write(f"{self.m:2d}\n")
      for i in range(self.n):
        for w in range(i+1,self.n):
          if isinstance(self.adj[i][w], dict):
            arquivo.write(f"{lista[i]} {lista[w]} {self.adj[i][w]['distancia']};{self.adj[i][w]['airlines']};{self.adj[i][w]['modelos']}\n")


      print("\nGrafo salvo no arquivo.\n\n")
  
  def showMin(self):
    lista =(list(self.mapa))
    print(f"\n n: {self.n:2d} ", end="")
    print(f"m: {self.m:2d}\n")
    for i in range(self.n):
        for w in range(i+1,self.n):
          if isinstance(self.adj[i][w], dict):
            print(f"{lista[i]} {lista[w]} {self.adj[i][w]['distancia']}")
    print("\nfim da impressao do grafo.")

  def atingivelPercurso(self, s, c, lista):
    if s == c:
      return True
    elif (self.adj[s][c] != float('inf') or self.adj[c][s] != float('inf')):
      return True
    for i in range(self.n):
      if lista[i] == 0:
        if (self.adj[s][i] != float('inf')):
          lista[i] = 1
          if self.atingivelPercurso(i, c, lista):
            return True
        elif (self.adj[i][s] != float('inf')):
          lista[i] = 1
          if self.atingivelPercurso(i, c, lista):
            return True
    return False

  def conexo(self):  #C0
    bool = True
    for i in range(1,self.n):
      teste = self.atingivelPercurso(0, i, [0] * self.n)
      if not teste:
        bool = False
    return bool
  # Para funcionar e necessario instalar as bilbiotecas matplotlib, networkx e pandas
  def desenharGrafo(self):
    Grafo = nx.Graph()
    conexoes = []
    for i in self.mapa.keys():
      for j in self.mapa.keys():
        if (self.adj[self.mapa[i][0]][self.mapa[j][0]]!=float('inf')) :
          temp = [i, j]
          conexoes.append(temp)
    Grafo.add_edges_from(conexoes)
    nx.draw_networkx(Grafo)
    plt.show()