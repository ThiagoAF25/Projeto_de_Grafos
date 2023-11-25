# Bibliotecas utilizadas para gerar grafo
#import matplotlib.pyplot as plt
#import networkx as nx
'''
Membros do grupo:
Leonardo Pinheiro de Souza      -   32127391
Lucas Paulo da Rocha            -   32196628
Luiz Octavio Tassinari Saraiva  -   32030411
Thiago Aidar Figueiredo         -   32144547
'''

class GrafoND:
  TAM_MAX_DEFAULT = 100
  MODELOS_DEFAULT = ()

  def __init__(self, n=TAM_MAX_DEFAULT, mapa={}):
    self.n = n  # número de vértices
    self.m = 0  # número de arestas
    self.mapa = mapa
    self.adj = [[float('inf') for i in range(n)] for j in range(n)]
    self.bloqueios = [0 for i in range(n)]

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
      #print("Vértice removido!")

  def insereA(self, v, w, dict):
    if v in self.mapa and w in self.mapa:
      if self.adj[self.mapa[v][0]][self.mapa[w][0]] == float('inf'):
        self.adj[self.mapa[v][0]][self.mapa[w][0]] = dict
        self.adj[self.mapa[w][0]][self.mapa[v][0]] = dict
        self.m += 1
        #print("Aresta inserida!")

  def removeA(self, v, w):
    if v in self.mapa and w in self.mapa:
      if self.adj[self.mapa[v][0]][self.mapa[w][0]] != float('inf'):
        self.adj[self.mapa[v][0]][self.mapa[w][0]] = float('inf')
        self.adj[self.mapa[w][0]][self.mapa[v][0]] = float('inf')
        self.m -= 1
        print("Aresta removida!")

  def dijkstra(self, inicio):
    if self.bloqueios[self.mapa[inicio][0]] == 0:
      #print(self.mapa)
      #print(self.adj)
      distanciaVoo = [float('inf') for i in range(self.n)]
      distanciaVoo[self.mapa[inicio][0]] = 0
      A = []
      for i in range(self.n):
        if self.bloqueios[i] == 0:
          A.append(i + 1)
      S = [self.mapa[inicio][0]]
      F = []
      rota = [0 for i in range(self.n)]
      k = 0
      while len(A) != 0:
        k += 1
        min = float('inf')
        r = 0
        # print(f"A = {A}")
        # print(f"distanciaVoo = {distanciaVoo}")
        for i in A:
          if distanciaVoo[i - 1] < min:
            min = distanciaVoo[i - 1]
            r = i
        F.append(r)
        # print(f"F={F}")
        # print(f"r={r}")
        A.remove(r)
  
        S.clear()
        for i in range(1, self.n + 1):
          if self.adj[r - 1][i - 1] != float('inf') and (i) in A:
            S.append(i)
  
        for s in S:
          p = distanciaVoo[s - 1]
          if (distanciaVoo[r - 1] +
              float(self.adj[r - 1][s - 1]["distancia"])) < p:
            p = distanciaVoo[r - 1] + float(self.adj[r - 1][s - 1]["distancia"])
            distanciaVoo[s - 1] = p
            rota[s - 1] = r
  
      # print(f"distanciaVoo = {distanciaVoo}")
      for i in self.mapa.keys():
        if self.bloqueios[self.mapa[i][0]] == 0:
          total = 0
          IndexInicio = self.mapa[inicio][0]
          atual = self.mapa[i][0]
          prox = rota[atual] - 1
          while (atual != IndexInicio):
            total += float(self.adj[atual][prox]["distancia"])
            atual = prox
            prox = rota[atual] - 1
          print(f"{inicio} -> {i} : {total}")
  
      # print(f"rota = {rota}")
      # print(len(rota) == self.n)
    else:
      print("O aeroport de origem está bloqueado! Remova o bloqueio para executar.")
  def gravarTXT(self):
    lista = (list(self.mapa))
    with open("grafo.txt", "w") as arquivo:
      arquivo.write("2\n")
      arquivo.write(f"{self.n:2d}\n")
      for key, value in self.mapa.items():
        arquivo.write(f"{key} {self.mapa[key][1]}\n")
      arquivo.write(f"{self.m:2d}\n")
      for i in range(self.n):
        for w in range(i + 1, self.n):
          if isinstance(self.adj[i][w], dict):
            arquivo.write(
                f"{lista[i]} {lista[w]} {self.adj[i][w]['distancia']};{self.adj[i][w]['airlines']};{self.adj[i][w]['modelos']}\n"
            )
      for i in range(self.n):
        arquivo.write(str(self.bloqueios[i]) + "\n")

      print("\nGrafo salvo no arquivo.\n\n")

  def showMin(self):
    lista = (list(self.mapa))
    print(f"\n n: {self.n:2d} ", end="")
    print(f"m: {self.m:2d}\n")
    for i in range(self.n):
      for w in range(i + 1, self.n):
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
    for i in range(1, self.n):
      teste = self.atingivelPercurso(0, i, [0] * self.n)
      if not teste:
        bool = False
    return bool

  def addBloqueio(self, s):
    if s in self.mapa:
      self.bloqueios[self.mapa[s][0]] = 1
      print(f"Bloqueio para {s} adicionado com sucesso!")

  def removeBloqueio(self, s):
    if s in self.mapa:
      self.bloqueios[self.mapa[s][0]] = 0
      print(f"Bloqueio para {s} removido com sucesso!")

  def ConexoesAeroportos (self):
    for key in self.mapa.keys():
      index = self.mapa[key][0]
      grau = 0
      for i in range (self.n):
        if self.adj[index][i] != float("inf"):
          grau += 1
      print(f"\n{key}: {grau}")
    
  def coloracaoClasse(self):
      C = [[] for i in range(self.n)]
      W = list(range(self.n))
      k = 0
      N = []
      while (len(W) > 0):
        for i in W:
          N.clear()
          for j in range(self.n):
            if self.adj[i][j] != float("inf"):
              N.append(j)
          intersecao = [x for x in C[k] if x in N]
          if len(intersecao) == 0:
            C[k].append(i)
        for y in range(len(C[k])):
          W.remove(C[k][y])
        k += 1
      for i in range(k):
        listaAux = []
        for j in C[i]:
          for chave, valor in self.mapa.items():
            if valor[0] == j:
              listaAux.append(chave)
        print(f"Coloração {i}: {listaAux}")
