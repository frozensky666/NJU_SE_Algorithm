"""
6. 在体育比赛中，给定n个队的集合P，每两个队之间都进行一场比赛则称为一个循环赛。
这样的循环赛经常用于为随后的单淘汰或双淘汰赛建立参赛队的次序和它们的种子队。
请为n个队的集合P设计一种构建循环赛的有效算法，保证最短时间内完成循环赛
（每一个队伍每一天只能参加一场比赛），假设n是2的幂。
"""

# 考虑采用分治法
# 假设有八个队伍（1，2，3，4，5，6，7，8），先将他们分为两个团体，每个团体四人。
# 先是团体之间比赛，团体之间赛完之后团体内部进行比赛。
# 这样一来，前四天的比赛如下：
# Day1: 1-5，2-6，3-7，4-8
# Day2: 1-6，2-7，3-8，4-5
# Day3: 1-7，2-8，3-5，4-6
# Day4: 1-8，2-5，3-6，4-7
# 之后， 团体内部进行比赛
# 即（1，2，3，4）和（5，6，7，8）内部比赛
# 自此开始进行分治
# Day5: 1-3，2-4，5-7，6-8
# Day6: 1-4，2-3，5-8，6-7
# 之后，继续往下拆分，（1，2），（3，4），（5，6），（7，8）内部比赛
# Day7: 1-2，3-4，5-6，7-8
# 比赛结束。
# 可以看到n个队伍只需要进行n-1天比赛
# 算法复杂度为 O(n^2)

def roundRobin(n: int):
    res = [[] for i in range(n-1)]
    def inner(start: int, end: int, res: list):
        if start == end:
            return
        middle = (start + end) // 2
        team1 = [i for i in range(start, middle+1)]
        team2 = [i for i in range(middle+1, end+1)]
        gap = 0
        currentDayBase = n + 1 - (end - start + 1)
        while gap < len(team1):
            for i in range(len(team1)):
                res[currentDayBase + gap - 1].append("%s-%s" % (team1[i],team2[(i+gap)%len(team1)]))
            gap += 1
        inner(start, middle, res)
        inner(middle+1, end, res)
    
    def myPrint(res):
        for i in range(len(res)):
            print("Day%s: %s" % (i+1, ", ".join(res[i])))
    inner(1, n, res)
    myPrint(res)
    return res

roundRobin(16)