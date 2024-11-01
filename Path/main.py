from path import DFS as dfs
from path import BFS as bfs
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

A = dfs(graph,10,5,0,0,9,4)
B = bfs(0,0,9,4,10,5,graph)
A.start()