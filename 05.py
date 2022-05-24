"""
5. 假设一棵根树T有n个结点，每一个结点v有权重w(v)。
对于T的结点的子集S，如果S中没有结点是S中任何其他结点的子结点或父结点
，称S为T的独立集。请设计一个求T的最大权独立集的有效算法
（一组结点的权就是这些结点权重的总和）。
"""

# 这一一道典型的树形dp问题
# 采用dfs + dp， 复杂度为O(n), n为节点个数

class TreeNode: 
    def __init__(self, key:str, weight:int, children: list) -> None:
        self.key = key
        self.weight = weight
        self.children = children

    def __str__(self) -> str:
        return "key: %s  weight: %s" % (self.key,self.weight)
    def __repr__(self) -> str:
        return "key: %s  weight: %s" % (self.key,self.weight)
    
def getTree(input: list): 
    # input = list[(self.key, self.father, self.weight),...] 
    # e.g. input = [('R',None,2),('A','R',2),('B','R',3),('C','R',5),
    # ('D','A',7),('E','A',1),('F','B',6),('G','C',3),('H','C',1),('I','C',4),
    # ('J','E',5),('K','G',1),('L','G',2),('M','I',3)]

    nodeDict = {}
    root = None
    for item in input:
        thisNode = nodeDict.get(item[0])
        if thisNode == None:
            thisNode = TreeNode(item[0],item[2],[])
            nodeDict[item[0]] = thisNode
        else:
            thisNode.value = item[2]

        if item[1] != None:
            father = nodeDict.get(item[1])
            if father == None:
                nodeDict[item[1]] = TreeNode(item[1],-1,[]) # init father
            nodeDict[item[1]].children.append(thisNode)
        else:
            root = thisNode
    return root

def findMaxWeightIndependentSet(tree: TreeNode): #  求最大权独立集
    # output = (maxWeight, maxWeightSet)
    # e.g. output = (29, {key: M  weight: 3, key: C  weight: 5, key: K  weight: 1, 
    # key: F  weight: 6, key: L  weight: 2, key: D  weight: 7, key: J  weight: 5})
    def core(tree, dp, mem):
        dp[tree] = [0, tree.weight]
        mem[tree] = [set(), set()]
        mem[tree][1].add(tree)
        if len(tree.children) > 0:
            for child in tree.children:
                core(child, dp, mem)
        for child in tree.children:
            if dp[child][0] >= dp[child][1]:
                dp[tree][0] += dp[child][0]
                mem[tree][0] = mem[tree][0].union(mem[child][0])
            else:
                dp[tree][0] += dp[child][1]
                mem[tree][0] = mem[tree][0].union(mem[child][1])
            
            dp[tree][1] += dp[child][0]
            mem[tree][1] = mem[tree][1].union(mem[child][0])

    dp = {}
    mem = {}
    core(tree, dp, mem)
    if dp[tree][0] >= dp[tree][1]:
        return (dp[tree][0], mem[tree][0])
    else:
        return (dp[tree][1], mem[tree][1])

    

tree = getTree(input = [('R',None,2),('A','R',2),('B','R',3),('C','R',5),
    ('D','A',7),('E','A',1),('F','B',6),('G','C',3),('H','C',1),('I','C',4),
    ('J','E',5),('K','G',1),('L','G',2),('M','I',3)])

print(findMaxWeightIndependentSet(tree))