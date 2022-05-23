"""
4. 假设给出电话网络图G，其顶点是交换中心，边表示两个交换中心之间的通信线路。
边的权重表示带宽大小。G中任意两个交换中心之间路径的带宽是路径上最低带宽。
请描述一个算法，用于计算任意两个交换中心a和b之间路径的最大带宽
（从多个路径中选择一个最大的）。
"""

# 采用类似Dijkstra的算法求最大带宽路径
# Dijkstra算法中更新的是s到任意顶点u的最短路径，
# 该算法中需要更新s到u的最大带宽

# 算法大致描述如下：
# 已知： 源点s， 目标点t。
# 算法维护两个顶点集合S和U。
# 集合S保留所有已知实际最大带宽路径的顶点，
# 而集合U则保留其他所有顶点。
# 集合S初始状态为空，而后每一步都有一个顶点从移动到S。
# 这个被选择的顶点是U中拥有最大的带宽值的顶点。
# 当一个顶点u从中转移到了S中，算法对u的每条外接边进行松弛。
# 松弛： 我们用s->u的带宽， 来对跟u相邻的未选中顶点u'（u'属于U）进行更新。
# 即 Bandwidth_new(s->u') = max { Bandwidth_old(s->u'), min{ Bandwidth(s->u) , Bandwidth(u->u') } }

# input: 
# points: "A,B,C,D,E"
# edges: {"A,B": 4, "A,D":2, "B,D":1, "B,C":4, "C,D":1, "C,E":3, "D,E":7}
# source: "A"
# target: "E"

# output:
# 3


# 下面的算法复杂度为O(n^2)


def findMaxBandwidth(points:str, edges:dict, source:str, target:str):
    pList = points.split(",")
    pLen = len(pList)
    pDict = {}
    for i in range(pLen):
        pDict[pList[i]] = i
    graph = [
        [
            -1 for j in range(pLen)
        ] for i in range(pLen)
    ]
    for k, v in edges.items():
        p1, p2 = k.split(",")
        p1Idx = pDict[p1]
        p2Idx = pDict[p2]
        # print(p1,p1Idx ,p2, p2Idx)
        graph[p1Idx][p2Idx] = v
        graph[p2Idx][p1Idx] = v
    
    visited = [0 for _ in range(pLen)]
    visited[pDict[source]] = 1

    S = {
        source + "," + source : 0
    }
    U = {}
    for i in range(pLen):
        if visited[i]==0:
            U[source+","+pList[i]] = graph[pDict[source]][i]

    def findAndDelMax(U: dict):
        nonlocal visited
        nonlocal pDict
        tmpv = -1
        tmpk = None
        for k,v in U.items():
            if v > tmpv:
                tmpk = k
                tmpv = v
        U.pop(tmpk)
        visited[pDict[tmpk.split(",")[1]]] = 1
        return (tmpk, tmpv)

    def insertOne(S: dict , maxItem: tuple):
        S[maxItem[0]] = maxItem[1]
    
    def updateU(U: dict, maxItem: tuple):
        nonlocal graph
        nonlocal visited
        nonlocal pDict
        nonlocal pLen
        nonlocal pList
        nonlocal source
        u = maxItem[0].split(",")[1]
        uIdx = pDict[u]
        for i in range(pLen):
            if visited[i] == 0 and graph[uIdx][i] >= 0:
                u1 = pList[i]
                prevBandwidth = U[source+","+u1]
                curBandwidth = min(maxItem[1], graph[uIdx][i])
                if curBandwidth > prevBandwidth:
                    U[source+","+u1] = curBandwidth

    while len(U) > 0:
        maxItem = findAndDelMax(U) # e.g. ("AA", 0)
        insertOne(S, maxItem)
        updateU(U, maxItem)
    
    print(S)
    return S[source + "," + target]


print(
    findMaxBandwidth("A,B,C,D,E", 
    {"A,B": 4, "A,D":2, "B,D":1, "B,C":4, "C,D":1, "C,E":3, "D,E":7}, 
    "A", "E"
    )
)