# This is a sample Python script.
import random

import numpy as np
from random import randint, seed
from collections import defaultdict
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from graph import Graph
def generateARandomPermutation(n):
    perm = [random.randint(0,n-1) for i in range(n)]
    # pos1 = randint(0, n - 1)
    # pos2 = randint(0, n - 1)
    # perm[pos1], perm[pos2] = perm[pos2], perm[pos1]
    return perm

def printVector(path,mat):
    cnt = len(path)
    for i in range(0, cnt, 2):
        print(mat[path[i]][path[i + 1]], end=" ")

    print("")


# Function to find all the paths recursively
def fitness(chromosome,matrx):
    source=chromosome[0]
    sum=0
    for i in range(len(chromosome)-1):
        sum+=matrx[source][chromosome[i]]
        source=chromosome[i]
    return sum

def initialize(matrix,s,d):
    paths=matrix.printAllPaths(s,d)
    return paths
def read_graph(filename):
  f=open(filename,"r");
  mat=[]

  n=int(f.readline())
  graph=Graph(n)
  for i in range(n):
      mat.append([])
      line=f.readline()
      elems=line.split(",")
      for j in range(n):
          graph.addEdge(i,int(elems[j]))
  s=int(f.readline())
  d=int(f.readline())
  return graph,s,d

def crossOver(chromosome_x,chromosome_y):
    common=[]
    for node_x in chromosome_x[0:len(chromosome_x)]:
        if node_x in chromosome_y:
            common.append(node_x)
    if len(common)>0:
        point=np.random.choice(common)
    else :
        return chromosome_x,chromosome_y
    poz_x=chromosome_x.index(point)
    poz_y=chromosome_y.index(point)
    first_x=chromosome_x[:poz_x]
    first_y=chromosome_y[:poz_y]
    last_x=chromosome_x[poz_x:]
    last_y=chromosome_y[poz_y:]
    return first_x+last_y,first_y+last_x


def calculate_distance(graph,chromosome):
    source=chromosome[0]
    sum=0
    for node in chromosome[1:]:

        if graph.graph[source][node]==0:
            sum+=1000000
        else:
            sum+=graph.graph[source][node]
        source=node
    return sum

def initilize_population(graph,source,destination, nr_of_chroms):
    # visited=np.zeros((graph.V,graph.V))
    chromosomes=[]
    i=0
    while i < nr_of_chroms:
        chromosome=[source]
        cp_source=source
        new = np.random.randint(0, graph.V-1)
        while new!=destination:
            while not(graph.graph[cp_source][new]!=0 ):
                # and visited[cp_source][new] == 0
                new=np.random.randint(0,graph.V)
            chromosome.append(new)
            # visited[cp_source][new] = 1
            cp_source=new
        # chromosome.append(destination)
        if chromosome not in chromosomes:
            if len(chromosome)>1:
                chromosomes.append(chromosome)
                i+=1

        # visited = np.zeros((graph.V, graph.V))
    return chromosomes

def initialize_2(graph,source,destination, nr_of_chroms):
    chromosomes = []
    for j in range(nr_of_chroms):
        chromosome=[source]
        i=0
        lungime=np.random.randint(graph.V)
        while i < lungime:
            new=random.randint(0,graph.V-1)
            if new!=chromosome[i]:
                chromosome.append(new)
                i+=1

        chromosome.append(destination)
        chromosomes.append(chromosome)
    return chromosomes
def create_tuple(chromosomes,matrix):
    tuples=[]
    for chromosme in chromosomes:
        tuples.append((calculate_distance(matrix,chromosme),chromosme))
    return tuples

def selection(chromosomes):
    chromosomes.sort( key=lambda c: c[0])
    return chromosomes[0],chromosomes[1]

def mutation(chromosomes,graph):
    positio_1=random.randint(0,len(chromosomes)-1)
    new = random.randint(0,int((graph.V - 1)))
    position=random.randint(0,len(chromosomes[positio_1][1])-1)
    chromosomes[positio_1][1][position] = new

def shortest_path(matrix,source,destination,nr_of_generations):
    nr_of_chroms=40
    chromosomes=initialize_2(matrix,source,destination,nr_of_chroms)
    chromosomes=create_tuple(chromosomes,matrix)
    chromosomes.sort(key=lambda c:c[0])

    for j in range(nr_of_generations):
        for i in range(int(nr_of_chroms/2)):
            # ch_x,ch_y=selection(chromosomes)
            ch_x=chromosomes[np.random.randint(int(nr_of_chroms/2))]
            ch_y = chromosomes[np.random.randint(int(nr_of_chroms/2))]
            child_1,child_2=crossOver(ch_x[1],ch_y[1])
            chromosomes.append((calculate_distance(matrix,child_1),child_1))
            chromosomes.append((calculate_distance(matrix, child_2), child_2))
            mutation(chromosomes,matrix)
        chromosomes=chromosomes[:int(nr_of_chroms/2)]

    chromosomes.sort( key=lambda c: c[0])
    return chromosomes[0]



grp,s,d=read_graph('hard.txt')
# print(initilize_population(grp,2-1,4-1,5))
print(shortest_path(grp,s-1,d-1,30))
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
