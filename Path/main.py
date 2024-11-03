from path import DFS as dfs
from path import BFS as bfs
from path import dijkstra as dij
#5x5
graph = {
  0: [0,1, 2, 3, 4],
1:[0,2, 4],
2:[1, 4],
3: [1, 2, 3, 4],
4: [3,4],
}

nodes = [0,1,2,3,4]

# Edges and Weights 
edges = {
   0: [(0, 0), (1, 1), (2, 2), (3, 0), (4, 0)],
    1: [(0, 0), (1, 1), (4, 1)],
    2: [(1, 0), (4, 1)],
   3: [(1, 2), (2, 0), (3, 0), (4, 0)],
    4: [(3, 3), (4, 3)]}


# o =1 0=2 O = 3
A = dfs(graph,5,5,0,0,4,4)
B = bfs(0,0,4,4,5,5,graph)
C = dij(nodes,edges)
print("depth first search")
A.start()
print("**************")
print("breadth first search")
B.start()
print("**************")
print("dijkstra algorithm")
C.dijkstra(0,4)



