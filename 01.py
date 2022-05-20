"""
1. 假设你有一只山羊和一只狼需要在一个有向图中从一个结点s到结点t。
为了避免狼吃掉山羊，它们所走的道路不能有公共边。假定存在这样的路径，
请你描述一个在G中找出两条不相交路径的多项式算法，以帮助狼和羊顺利从s到t。
"""
# 即：
# 构造一个图
# 找到从s->t的两条不重复路径
# 假设总是有解

# 思路：
# 两次dfs即可，前一次搜索到的边在第二次搜索时不使用
# dfs在最坏情况下(退化成链表)的复杂度为 O(n), 每向下走一层需要遍历n个节点
# 因此总体最坏复杂度为O(n^2)

class Node:
    def __init__(self, key) -> None:
        self.key = key
    def __str__(self) -> str:
        return str(self.key)
    def __repr__(self) -> str:
        return self.__str__()

class Edge:
    def __init__(self, source: Node, target: Node) -> None:
        self.source = source
        self.target = target
    def __str__(self) -> str:
        return '(%s, %s)' % (self.source, self.target)
    def __repr__(self) -> str:
        return self.__str__()

class Graph:
    def __init__(self, nodes, edges) -> None:
        tmpNodes = list(map(lambda node: Node(node), nodes))
        self.nodes = tmpNodes
        nodeKeyDict = {node.key:node for node in tmpNodes}
        nodeIdxDict = {tmpNodes[idx]:idx for idx in range(len(tmpNodes))}
        self._nodeKeyDict = nodeKeyDict
        self._nodeIdxDict = nodeIdxDict
        tmpEdges = []

        nodeEdgeDict = {}
        for edge in edges:
            sourceNode = nodeKeyDict[edge[0]]
            targetNode = nodeKeyDict[edge[1]]
            tmpEdge = Edge(sourceNode, targetNode)
            nodeEdgeDict[(sourceNode, targetNode)] = tmpEdge
            tmpEdges.append(tmpEdge)
        self._nodeEdgeDict = nodeEdgeDict
        self.edges = tmpEdges
        
        nodeLen = len(nodes)
        self.graph = [
            [
                0 for j in range(nodeLen)
            ] for i in range(nodeLen)
        ]
        for edge in self.edges:
            self.graph[nodeIdxDict[edge.source]][nodeIdxDict[edge.target]] = 1
        
        # self.printGraph()

    def findPath(self, fromNodeKey: int, toNodeKey: int):
        nodeLen = len(self.nodes)
        edgeMarks = [
            [ 0 for j in range(nodeLen) ]
            for i in range(nodeLen)
        ]
        fromNode = self._nodeKeyDict[fromNodeKey]
        toNode = self._nodeKeyDict[toNodeKey]
        fromNodeIdx = self._nodeIdxDict[fromNode]
        toNodeIdx = self._nodeIdxDict[toNode]

        

        def getNextIdx(cur, nodeMarks):
            nonlocal edgeMarks
            candidates = self.graph[cur]
            for candidate in range(len(candidates)):
                if candidates[candidate] == 1 and nodeMarks[candidate] == 0 and edgeMarks[cur][candidate] == 0:
                    nodeMarks[candidate] = 1
                    edgeMarks[cur][candidate] = 1
                    return candidate
            return None

        def dfs(dfsStack, nodeMarks):
            while len(dfsStack)>0:
                curIdx = dfsStack[len(dfsStack)-1]
                if curIdx == toNodeIdx:
                    break
                nextIdx = getNextIdx(curIdx, nodeMarks)
                if nextIdx != None:
                    dfsStack.append(nextIdx)
                else:
                    dfsStack.pop()
            return dfsStack

        def initNodeMarksAndDfsStack():
            nonlocal nodeLen
            nonlocal fromNodeIdx
            nodeMarks = [0 for i in range(nodeLen)]
            nodeMarks[fromNodeIdx] = 1
            dfsStack = [fromNodeIdx]
            return (
                dfsStack,
                nodeMarks
            )
        
        dfsStack = dfs(*initNodeMarksAndDfsStack())
        dfsStack2 = dfs(*initNodeMarksAndDfsStack())
        # dfsStack3 = dfs(*initNodeMarksAndDfsStack())
        # dfsStack4 = dfs(*initNodeMarksAndDfsStack())
        res = (
            list(map(lambda x: self.nodes[x], dfsStack)),
            list(map(lambda x: self.nodes[x], dfsStack2)),
            # list(map(lambda x: self.nodes[x], dfsStack3)),
            # list(map(lambda x: self.nodes[x], dfsStack4)),
        )
        print(res)
        return res
        
    def printGraph(self):
        print(self.nodes)
        print(self.edges)
        print(self.graph)
        print(self._nodeEdgeDict)
        print(self._nodeIdxDict)
        print(self._nodeKeyDict)


def test1():
    nodes = [1,2,3,4,5,6,7,8,9,10,11,12]
    edges = [(1,2),(2,1),(1,3),(3,4),(4,1),(3,5),(1,6),(6,7),(6,8),(1,11),(11,8),(11,12),(7,9),(7,10),(8,10),(9,12),(12,10),(4,10)]
    graph = Graph(nodes, edges)
    graph.findPath(1,10)


test1()