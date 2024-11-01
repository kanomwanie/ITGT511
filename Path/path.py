
# Using a Python dictionary to act as an adjacency list
#g= {
  #0 : [2,1,3],
 # 1 : [0, 3],
 # 2 : [0,3],
 # 3 : [1,2],
 # 4: []
#}
class DFS:
    def __init__(self, graph,R,C,sr,sc,er,ec) -> None:
        #DFS
        self.n = R #number of nodes in the graph 
        self.count = 0 
        self.components = []#empty integer array # size n 
        self.visited = [] # size n 
        self.g = graph
        self.R = R
        self.C =C
        self.m = [[0 for _ in range(C)] for _ in range(R)]
        self.sr = sr
        self.sc =sc # ’S’ symbol row and column values 
        self.er = er
        self.ec =ec

    def tomap(self):
        for i in range(self.R):
            if self.g[i]!= None:
                for j in range(self.C):
                    self.m[i][j] = "#"
                    if len(self.g[i])!= 0 and j in self.g[i]:
                        if i==self.sr and j==self.sc:
                             self.m[i][j] = "S"
                        elif i==self.er and j==self.ec:
                            self.m[i][j] = "E"
                        elif self.visited[i]:
                           self.m[i][j] = "x"
                        else:    
                            self.m[i][j] = "."

    def printmap(self,map):
        print("----------------")
        for i in map:
              print(' '.join(i))
        print("----------------")

    def DFSinit(self):
        for i in range(self.n):
            self.visited.append(False)
            self.components.append(0)

    def start(self):
       self.DFSinit()
       self.tomap()
       self.printmap(self.m)
       self.findComponents()

    def findComponents(self): 
        for i in range(self.n): 
            if not self.visited[i]: 
                self.count +=1
                A = self.dfs(i) 
                if A==0:
                   print("Count "+ str(self.count))
                   return 0
        return (self.count, self.components) 

    def dfs(self,at): 
        print("visit "+str(at))
        self.visited[at] = True 
        self.components[at] = self.count 
        self.tomap()
        self.printmap(self.m)
        if 'E' in self.m[at]:
           print("Exit Found!")
           return 0
        for next in self.g[at]: 
            if not self.visited[next]: 
                self.dfs(next)
    

class BFS:
    def __init__(self, sr,sc,er,ec,R,C,graph) -> None:
        # Global/class scope variables 
        self.R = R
        self.C = C# R = number of rows, C = number of columns 
        self.m = [[0 for _ in range(C)] for _ in range(R)]    # Input character matrix of size R x C 
        self.sr = sr
        self.sc =sc # ’S’ symbol row and column values 
        self.er = er
        self.ec =ec
        self.g =graph
        self.rq = []
        self.cq =[] # Empty Row Queue (RQ) and Column Queue (CQ) 
        self.visited = [[False for _ in range(C)] for _ in range(R)]  
        # Variables used to track the number of steps taken. 
        self.move_count = 0 
        self.nodes_left_in_layer = 1 
        self.nodes_in_next_layer = 0 
        # Variable used to track whether the ‘E’ character 
        # ever gets reached during the BFS. 
        self.reached_end = False 
        # R x C matrix of false values used to track whether  
        # the node at position (i, j) has been visited. 
        #visited = … 
        # North, south, east, west direction vectors. 
        self.dr = [-1, +1,  0,  0] 
        self.dc = [ 0,  0, +1, -1]

    def start(self):
        self.BFSinit()
       # print(self.m)
        self.tomap()
        print(self.solve())

    def BFSinit(self):
        for i in range(self.R):
            if self.g[i]!= None:
                for j in range(self.C):
                    self.m[i][j] = "#"
                    if i==self.sr and j==self.sc:
                        self.m[i][j] = "S"
                    elif i==self.er and j==self.ec:
                        self.m[i][j] = "E"
                    elif len(self.g[i])!= 0 and j in self.g[i]:
                        self.m[i][j] = "."

    def printmap(self,map):
        print("----------------")
        for i in map:
              print(' '.join(i))
        print("----------------")

    def tomap(self):
        A = [[0 for _ in range(self.C)] for _ in range(self.R)]
        for i in range(self.R):
            if self.g[i]!= None:
                for j in range(self.C):
                    A[i][j] = "#"
                    if len(self.g[i])!= 0 and j in self.g[i]:
                        if i==self.sr and j==self.sc:
                             A[i][j] = "S"
                        elif i==self.er and j==self.ec:
                            A[i][j] = "E"
                        elif self.visited[i][j]:
                           A[i][j] = "x"
                        else:    
                            A[i][j] = "."
        self.printmap(A)

    def solve(self): 
        self.rq.append(self.sr) 
        self.cq.append(self.sc) 
        self.visited[self.sr][self.sc] = True 
        while len(self.rq) > 0: # or cq.size() > 0 
            r = self.rq.pop(0)
            c = self.cq.pop(0)
            if self.m[r][c] == "E": 
                self.reached_end = True 
                print("Exit Found!")
                break 
            self.explore_neighbours(r, c) 
            self.nodes_left_in_layer -=1
            if self.nodes_left_in_layer == 0: 
                self.nodes_left_in_layer = self.nodes_in_next_layer 
                self.nodes_in_next_layer = 0 
                self.move_count+=1
        if self.reached_end: 
            return self.move_count 
        return -1 

    def explore_neighbours(self,r, c): 
        for i in range(4): 
            rr = r + self.dr[i] 
            cc = c + self.dc[i] 
            # Skip out of bounds locations 
            if rr < 0 or cc < 0: continue 
            if rr >= self.R or cc >= self.C: continue 
            # Skip visited locations or blocked cells 
            if self.visited[rr][cc]: continue 
            if self.m[rr][cc] == "#": continue 
            self.rq.append(rr) 
            self.cq.append(cc) 
            self.visited[rr][cc] = True 
            self.tomap()
            self.nodes_in_next_layer +=1


class Edge:

     def __init__(self,to,cost) -> None:
        self.cost = cost
        self.to = to

class Dijkstra:
    def __init__(self,n) -> None:
        self.n = n
        self.edgeCount=0
        self.dist=[]
        self.prev=[]
        self.graph= self.createEmptyGraph()

    def createEmptyGraph(self):
        A = [None] * self.n
        #for i in range(self.n):
           # A.append([])
        return A
    
    def addEdge(self,fromm, to, cost):
        self.edgeCount+=1
        self.graph[fromm]= Edge(to, cost)

    def dijkstra(self, start, end):

    # Keep an Indexed Priority Queue (ipq) of the next most promising node to visit.
        degree = self.edgeCount / self.n
        ipq =  MinIndexedDHeap()
        ipq.MinIndexedDHeap(degree, self.n)
        ipq.insert(start, 0.0)

        # Maintain an array of the minimum distance to each node.
        dist = [float('inf') for _ in range(self.n)]
       # Arrays.fill(dist, float('inf'))
        dist[start] = 0.0

        visited = []*self.n
        prev =[]*self.n
        print(ipq.size)
        while not ipq.size !=0 :
            nodeId = ipq.peekMinKeyIndex()

            visited[nodeId] = True
            minValue = ipq.pollMinValue()

        #We already found a better path before we got to processing this node so we can ignore it.
            if (minValue > self.dist[nodeId]):
                continue

            for edge in self.graph.index(nodeId) :

               # We cannot get a shorter path by revisiting a node we have already visited before.
                if (visited[edge.to]) :
                    continue

                # Relax edge by updating minimum cost if applicable.
                newDist = self.dist[nodeId] + edge.cost
                if (newDist < dist[edge.to]) :
                    self.prev[edge.to] = nodeId
                    self.dist[edge.to] = newDist
                    # Insert the cost of going to a node for the first time in the PQ, or try and update it to a better value by calling decrease.
                    if not ipq in edge.to:
                         ipq.insert(edge.to, newDist)
                    else:
                          ipq.decrease(edge.to, newDist)
           
      
        #// Once we've processed the end node we can return early (without
        #// necessarily visiting the whole graph) because we know we cannot get a
        #// shorter path by routing through any other nodes since Dijkstra's is // greedy and there are no negative edge weights.
        if (nodeId == end):
            return dist[end]

        #// End node is unreachable.
        return float('inf')
    
    def reconstructPath(self, start,end) :
        if (end < 0 or end >= self.n) :
            raise Exception("Invalid node index")
            #throw new IllegalArgumentException("Invalid node index")
        if (start < 0 or start >= self.n) :
            raise Exception("Invalid node index")
            #throw new IllegalArgumentException("Invalid node index")
        path = []
        dist = self.dijkstra(start, end)
        if (dist == float('inf')) :
            return path
        for at in range(end, -1, -1):
            if at is not None:
                path.append(at)
                at =  self.prev[at]
        path.reverse()
        return path
    
class MinIndexedDHeap:

    def __init__(self) -> None:
        self.sz=0
        self.N=0
        self.D=0
        self.child=[]
        self.parent=[]
        self.pm =[]
        self.im =[]
        self.values=[]

  #  // Initializes a D-ary heap with a maximum capacity of maxSize.
    def MinIndexedDHeap(self, degree, maxSize) :
      if (maxSize <= 0):
        raise Exception("maxSize <= 0")

      self.D = max(2, degree)
      self.N = max(self.D + 1, maxSize)

      self.im = [0 for _ in range(self.N)]
      self.pm = [0 for _ in range(self.N)]
      self.child = [0 for _ in range(self.N)]
      self.parent = [0 for _ in range(self.N)]
      self.values = [0 for _ in range(self.N)]
      for i in range(self.N) :
        self.parent[i] = (i - 1) / self.D
        self.child[i] = i * self.D + 1
        self.pm[i] = self.im[i] = -1
      
    

    def size(self) :
      return self.sz
    

    def isEmpty(self) :
      return self.sz == 0
    

    def contains(self, ki) :
      self.keyInBoundsOrThrow(ki)
      print(ki)
      return self.pm[ki] != -1
    

    def peekMinKeyIndex(self) :
      self.isNotEmptyOrThrow(self.im)
      return self.im[0]
    

    def pollMinKeyIndex(self) :
      minki = self.peekMinKeyIndex()
      self.delete(minki)
      return minki
    

    def peekMinValue(self) :
      self.isNotEmptyOrThrow()
      return self.im[0]
    

    def pollMinValue(self) :
      minValue = self.peekMinValue()
      self.delete(self.peekMinKeyIndex())
      return minValue
    
    def insert(self, ki, value):
      if self.contains(ki) :
        raise Exception("index already exists; received: " + str(ki))
      self.valueNotNullOrThrow(value)
      self.pm[ki] = self.sz
      self.im[self.sz] = ki
      self.values[ki] = value
      self.sz +=1
      print(self.sz)
      self.swim(self.sz)

    def valueOf(self, ki) :
      self.keyExistsOrThrow(ki,self.values)
      return self.values[ki]

    def delete(self, ki) :
      self.keyExistsOrThrow(ki,self.pm)
      i = self.pm[ki]
      self.sz-=1
      print(self.sz)
      self.swap(i,self.sz)
      self.sink(i)
      self.swim(i)
      value = self.values[ki]
      self.values[ki] = None
      self.pm[ki] = -1
      self.im[self.sz] = -1
      return value
    

    def update(self,ki, value) :
      self.keyExistsAndValueNotNullOrThrow(ki, value,self.pm)
      i = self.pm[ki]
      oldValue = self.values[ki]
      self.values[ki] = value
      self.sink(i)
      self.swim(i)
      return oldValue
    

    #// Strictly decreases the value associated with 'ki' to 'value'
    def decrease(self,ki, value) :
      self.keyExistsAndValueNotNullOrThrow(ki, value,self.values)
      if (self.less(value, self.values[ki])) :
        self.values[ki] = value
        self.swim(self.pm[ki])
      
    

   # // Strictly increases the value associated with 'ki' to 'value'
    def increase(self, ki, value) :
      self.keyExistsAndValueNotNullOrThrow(ki, value,self.values)
      if (self.less(self.values[ki], value)) :
        self.values[ki] = value
        self.sink(self.pm[ki])
      
    

    #/* Helper functions */

    def sink(self, i) :
      j = self.minChild(i)
      while j != -1:
        self.swap(i, j)
        i = j
        j = self.minChild(i)
      
    

    def swim(self, i) :
      while (self.less(i, self.parent[i])):
        self.swap(i, self.parent[i])
        i = self.parent[i]
      
    

    #// From the parent node at index i find the minimum child below it
    def minChild(self, i) :
      index = -1
      fromm = self.child[i]
      to = min(self.sz, fromm + self.D)
      for j in range(fromm, to): 
        if (self.less(j, i)):
            index = i = j
      return index
    

    def swap(self, i, j) :
      self.pm[self.im[j]] = i
      self.pm[self.im[i]] = j
      tmp = self.im[i]
      self.im[i] = self.im[j]
      self.im[j] = tmp
    

    #// Tests if the value of node i < node j
   # @SuppressWarnings("unchecked")
    def less(self, i, j) :
      return ( self.values[ self.im[int(i)]]- self.values[ self.im[int(j)]]) < 0
      #return ((Comparable<? super T>) values[im[i]]).compareTo((T) values[im[j]]) < 0
    

    #@SuppressWarnings("unchecked")
    #def less(self, obj1, obj2) :
     # return ((Comparable<? super T>) obj1).compareTo((T) obj2) < 0
    

   # @Override
    def toString( self) :
      lst = []* self.sz
      for i in range( self.sz):
          lst.append( self.im[i])
      return " ".join(lst)
    

    #/* Helper functions to make the code more readable. */

    def isNotEmptyOrThrow(self, IM) :
      if len(IM)==0 :
        raise Exception("Priority queue underflow")
        #throw new NoSuchElementException("Priority queue underflow");
    

    def keyExistsAndValueNotNullOrThrow(self,ki,  value,PM) :
      self.keyExistsOrThrow(ki,PM)
      self.valueNotNullOrThrow(value)
    

    def keyExistsOrThrow(self, ki,PM) :
      if not( ki in PM) :
         raise Exception("Index does not exist; received: " + str(ki))
       # throw new NoSuchElementException("Index does not exist; received: " + ki);
    

    def valueNotNullOrThrow(self,value) :
      if (value == None):
         raise Exception("value cannot be null")
         #throw new IllegalArgumentException("value cannot be null");
    

    def keyInBoundsOrThrow(self, ki) :
      if (ki < 0 or ki >= self.N):
         raise Exception("Key index out of bounds; received: " + str(ki))
        #throw new IllegalArgumentException("Key index out of bounds; received: " + ki);
    






