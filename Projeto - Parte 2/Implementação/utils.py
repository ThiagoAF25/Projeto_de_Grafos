from grafoNDMatriz import GrafoND
import pandas as pd
import numpy as np

def lerCSV():
  tabela = pd.read_csv("voos.csv")
  #CRIANDO TUPLAS COM SIGLA,NOME_AEROPORTO
  sigla_saida = tabela["Saida Sigla"]
  aeroporto_saida = tabela["Saida Nome Aeroporto"]
  saida1 = list(set(zip(sigla_saida, aeroporto_saida)))
  sigla_chegada = tabela["Chegada"]
  aeroporto_chegada = tabela["Chegada Nome Aeroporto"]
  chegada1 = list(set(zip(sigla_chegada, aeroporto_chegada)))
  aeroportos1= list(sorted(set(saida1 + chegada1)))
  
  mapa = {}
  for i, item in enumerate(aeroportos1):
      mapa[item[0]] = [i,item[1]]
  
  #criando grafo
  n = len(mapa)
  g1 = GrafoND(n, mapa)
  
  #criando arestas
  for index, row in tabela.iterrows():
    origem = row["Saida Sigla"]
    destino = row["Chegada"]
    distancia = row["Distancia (Km)"]
    modelos = row["ModelosAvioes"]
    comp = row["Airline"]
    dict = {
      "distancia": distancia,
      "modelos":modelos.split("-"),
      "airlines":comp.split("-")
    }
    
    g1.insereA(origem, destino, dict)
  return g1
  
def showTXT():
  with open("grafo.txt", "r") as arquivo:
    Linhas = arquivo.readlines()
    for linha in Linhas:
      print("{}".format(linha.strip()))


def leituraTXT():
  mapa = {}
  with open("grafo.txt", "r") as arquivo:
    tipo = arquivo.readline().strip('\n')
    n = int(arquivo.readline())
    for i in range(n):
      linha = arquivo.readline().strip('\n')
      linha = linha.split(" ",1)
      mapa[linha[0]] = [i,linha[1]]
    Grafo = GrafoND(n,mapa)
    m = int(arquivo.readline())
    for w in range(m):
      linha = arquivo.readline().strip('\n')
      linha = linha.split(" ",2)
      linha[2] = linha[2].replace("'", '')
      linha[2] = linha[2].strip("'")
      linha[2] = linha[2].split(';')
      linha[2][1]=linha[2][1].replace("[", "")
      linha[2][1]=linha[2][1].replace("]", "")
      linha[2][2]=linha[2][2].replace("]", "")
      linha[2][2]=linha[2][2].replace("[", "")
      dict = {
        "distancia": linha[2][0],
        "modelos": linha[2][2].strip().split(", "),
        "airlines": linha[2][1].strip().split(", ")
      }
      Grafo.insereA(linha[0],linha[1],dict)
    for i in range(n):
      Grafo.bloqueios[i] = int(arquivo.readline())
  return tipo, Grafo

def menu():
  g1 =GrafoND(0,{})
  resp = 0
  tipo = 0
  while(resp != 15):
    print('\n')
    print("\n-------------- GRAFO PRINCIPAIS ROTAS AEREAS INTERNACIONAIS --------------\n")
    print("1 - Ler dados do arquivo grafo.txt .")
    print("2 - Gravar dados no arquivo grafo.txt .")
    print("3 - Inserir vértice.")
    print("4 - Inserir aresta.")
    print("5 - Remove vértice.")
    print("6 - Remove aresta.")
    print("7 - Mostrar conteúdo do arquivo.")
    print("8 - Mostrar grafo.")
    print("9 - Conexidade do grafo.")
    print("10 - Caminho Minimo por Dijkstra.")
    print("11 - Adicionar Bloqueio.")
    print("12 - Remover Bloqueio.")
    print("13 - Verificar Grau dos vertices.")
    print("14 - Coloracao por Classe dos vertices.")
    print("15 - Encerrar a aplicação.")
    resp = int(input("/> ").strip())

    match resp:
      case 1:
        tipo, g1 = leituraTXT()
      case 2:
        g1.gravarTXT()
      case 3:
        sigla = input("Sigla do aeroporto: ").strip().upper()
        nome = input("Nome do aeroporto: ").strip()
        g1.insereV(sigla, nome)
        
      case 4:
        sigla_saida = input("Sigla de saida: ").strip().upper()
        sigla_chegada = input("Sigla de chegada: ").strip().upper()
        distancia = float(input("Distancia: "))
        qtdModelos = int(input("Quantidade Modelos: ").strip())
        modelos = []
        for i in range(qtdModelos):
          modelos.append((input("Modelos: ")).strip())
        qtdAirlines = int(input("Quantidade de Airlines: ").strip())
        Airlines = []
        for i in range(qtdAirlines):
          Airlines.append((input("Airline: ")).strip())
        dict = {
          "distancia": distancia,
          "modelos":modelos,
          "airlines":Airlines
        }
        g1.insereA(sigla_saida,sigla_chegada, dict)
      case 5:
        nome = input("Sigla do aeroporto: ").strip().upper()
        g1.removeV(nome)
      case 6: 
        saida = input("Sigla do aeroporto de saida: ").strip().upper()
        chegada = input("Sigla do aeroporto de chegada: ").strip().upper()
        g1.removeA(saida, chegada)
      case 7: 
        showTXT()
      case 8:
        g1.showMin()
      case 9:
        if g1.conexo():
          print("Conexo")
        else:
          print("Desconexo")
      case 10:
        nome = input("Sigla do aeroporto: ").strip().upper()
        g1.dijkstra(nome)
      case 11:
        g1.addBloqueio(input("Sigla do aeroporto a ser bloqueado:"))
      case 12:
        g1.removeBloqueio(input("Sigla do aeroporto a ser desbloqueado: "))
      case 13:
          g1.ConexoesAeroportos()
      case 14:
          g1.coloracaoClasse()
      case 15:
        continue
