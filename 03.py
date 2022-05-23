"""
3. 一家专车公司每天必须处理客户的接送请求，将客户从他们的家（不同地方）接到当地机场。
假设现在有n个位置的接送请求，并且有n辆专车，其中第i辆车到位置j的距离dij是给定的。
请你描述一个派遣n辆专车到n个地点的有效算法，使得n个专车的总行程最小。
"""

# 实在是想不出多项式复杂度的解法，但是能想到一个阶乘复杂度的方法。
# 题目换个描述： 现在所有的dij组成一个n*n的矩阵，从中挑选n个值，值与值之间不能在相同行和相同列。
# 上面的描述明显是一个排列问题， 不考虑优化，复杂度为O(n!)
# 考虑到对每个排列求和的复杂度为O(n), 最终复杂度为O(n * n!) 即 O(n!)

# 在网上看到了上述问题可以转化成“带权二分图求最佳匹配“的问题， 使用KM算法来解决
# KM算法是一种计算机算法，功能是求完备匹配下的最大权匹配



# 下面是简单的排列算法
def findMinPath(distanceMatrix):
    arr = [i for i in range(0, len(distanceMatrix))]
    result = [float('inf')]
    dfs(arr, 0, result, distanceMatrix)
    return result[0]

def dfs(arr, depth, result, distanceMatrix):
    if depth == len(arr):
        result[0] = min(result[0], mysum(arr, distanceMatrix))        
        return 

    for i in range(depth, len(arr)):
        arr[i], arr[depth] = arr[depth], arr[i]
        dfs(arr, depth + 1, result, distanceMatrix)
        arr[i], arr[depth] = arr[depth], arr[i]

def mysum(arr,distanceMatrix):
    res = 0
    for i in range(len(arr)):
        res += distanceMatrix[i][arr[i]]
    return res


print(findMinPath([
    [7,9,6],
    [1,2,3],
    [1,2,5]
]))