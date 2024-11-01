from path import DFS as dfs
from path import BFS as bfs
from path import Dijkstra as dij
graph = {
  0: [0,1, 2, 3, 4],
1:[1, 4],
2:[1, 4],
3: [1, 2, 3, 4],
4: [1 ,2, 3],
5:[3],
6: [3, 4],
7: [0, 1 ,2, 4],
8: [0, 1, 2, 3 ,4],
9: [3, 4],
}
# o =1 0=2 O = 3
A = dfs(graph,10,5,0,0,9,4)
B = bfs(0,0,9,4,10,5,graph)
C = dij(10)
#A.start()
C.createEmptyGraph()
C.addEdge(0,0,0)
C.addEdge(0,1,0)
C.addEdge(0,2,0)
C.addEdge(0,3,0)
C.addEdge(0,4,1)
C.addEdge(1,4,0)
C.addEdge(1,1,0)
C.addEdge(2,1,1)
C.addEdge(2,4,1)
C.addEdge(3,1,2)
C.addEdge(3,2,0)
C.addEdge(3,3,0)
C.addEdge(3,4,0)
C.addEdge(4,1,0)
C.addEdge(4,2,3)
C.addEdge(4,3,2)
C.addEdge(5,3,0)
C.addEdge(6,3,1)
C.addEdge(6,4,1)
C.addEdge(7,0,0)
C.addEdge(7,1,3)
C.addEdge(7,2,0)
C.addEdge(7,4,3)
C.addEdge(8,0,3)
C.addEdge(8,1,0)
C.addEdge(8,2,1)
C.addEdge(8,3,0)
C.addEdge(8,4,0)
C.addEdge(9,3,1)
C.addEdge(9,4,0)
C.dijkstra(0,9)

