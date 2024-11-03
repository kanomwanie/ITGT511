from collections import  deque
import heapq
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
            A=-1
            if not self.visited[i]: 
                self.count +=1
                A = self.dfs(i) 
            if A==0:
                   
                   return 0
        print("Count "+ str(self.count))
        print("Components "+ str(self.components))
        return (self.count, self.components) 

    def dfs(self,at): 
        print("visit "+str(at))
        self.visited[at] = True 
        self.components[at] = self.count 
        self.tomap()
        self.printmap(self.m)
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
        self.tomap()
        self.solve()

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
            self.explore_neighbours(r, c) 
            if self.m[r][c] == "E": 
                self.reached_end = True 
                print("Exit Found!")
                print("Move Count "+ str(self.move_count))
                break 
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

class  dijkstra:
  def __init__(self,node,edg,) -> None:
        self.edges = edg
        self.nodes = node

  def checkedge(self, E,N):
      for i in range(len(N)):
        if N[i][0] == E:
            return True
      return False
  def checkcost(self,r,c):
      for i in range(len(self.edges[r])):
          if self.edges[r][i][0]==c:
            return self.edges[r][i][1]

  def tomap(self,S,E,visited):
        R = len(self.nodes)
        C = len(self.nodes)
        m = [[0 for _ in range(C)] for _ in range(R)]
        for i in range(R):
            if self.edges[i]!= None:
                for j in range(C):
                    m[i][j] = "#"
                    if len(self.edges[i])!= 0 and  self.checkedge(j,self.edges[i]):
                        if i==S and j==S:
                             m[i][j] = "S"
                        elif i==E and j==E:
                           m[i][j] = "E"
                        elif visited[i]:
                           m[i][j] = "x"
                        else:    
                            cost = self.checkcost(i,j)
                            if cost == 1:
                              m[i][j] = "o"  
                            elif cost == 2:
                              m[i][j] = "0" 
                            elif cost == 3:
                              m[i][j] = "O" 
                            else:
                              m[i][j] = "."
        self.printmap(m)

  def printmap(self,map):
        print("----------------")
        for i in map:
              print(' '.join(i))
        print("----------------")


  def dijkstra(self,start, end):
      dist = {node: float('inf') for node in self.nodes}
      dist[start] = 0
      pq = [(0, start)]
      visited_dijkstra = set()
      v = [False for _ in range(len(self.nodes))]
      print(". = 0   o = 1   0 = 2   O = 3")
      self.tomap(start,end,v)

      while pq:
          current_dist, node = heapq.heappop(pq)
          if node in visited_dijkstra:
            continue
          print("visit "+str(node))
          visited_dijkstra.add(node)
          v[node] = True
          self.tomap(start,end,v)
          
         # draw_node(node, 'Orange')
          #pygame.display.update()
          #pygame.time.delay(500)
          
          for neighbor, weight in self.edges.get(node, []):
              new_dist = current_dist + weight
              if new_dist < dist[neighbor]:
                  dist[neighbor] = new_dist
                  heapq.heappush(pq, (new_dist, neighbor))
                  #draw_edge(node, neighbor, 'Orange', weight) 
          
          #draw_node(node, 'Gray')
          #pygame.display.update()
          #pygame.time.delay(500)
          
         # pygame.draw.rect(screen, (50, 55, 50), (10, height - 30, width, 30))
          
          # dist array
        #  dist_text = "Dist: " + ", ".join(f"{n}:{dist[n]}" for n in dist)
         # dist_surface = font.render(dist_text, True, (255, 255, 255))  
         # screen.blit(dist_surface, (10, height - 30))
         # pygame.display.update()






