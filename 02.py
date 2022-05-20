"""
2. 假设在平面中给出n个点，并且希望这些点分成A和B两组，
使得A中的每一个点到A中另一个点都比到B中任意一个点近，反之亦然。
请描述一个有效的算法能够做到这种划分。
"""

# 在点集中找出两个距离最远的点的中垂线l
# l将集合划分为A'和B'，显然， 如果A'和B'满足题意， 即为所求的集合
# 不可能出现其他的情况

# 证明如下：
# 如果距离最远的点a和b在同一个集合中（不妨设为集合A）
# 那么对于任意一个集合B中的点c， 都一定有ab >= ac，不合题意。除非B为空集。
# 因此a和b需要分开在两个不同集合A和B中
# 对于ab中垂线l左边的任意一点p，都有pa < pb，是题设的必要不充分条件
# 同理， 对于l右边的任意一点q，都有qb < qa，是题设的必要不充分条件
# 将A中的任意一点放在B中， 或者将B的任意点放回A中， 都将违反上述两个必要条件
# 所以现在只需要验证l划分出来的点均满足题意即可。 …… （1）
# 若存在不满足题意的点，那么将所有点划分到A集合。B集合为空集。
# 对于（1），我们可以任取A、B集合中两点作中垂线，
# 若划分均不发生变化，说明划分l是一个满足题意的划分
# 该算法的复杂度主要体现在（1）中， 是O(n^3) 的复杂度


import math
from typing import Set


class Point:
    def __init__(self,x,y) -> None:
        self.x = x
        self.y = y
    def distant(self, p):
        return math.sqrt((self.x-p.x)**2 + (self.y-p.y)**2)
    def __str__(self):
        return '(%s, %s)' % (self.x, self.y)
    def __repr__(self):
        return '(%s, %s)' % (self.x, self.y)
    def __add__(self, p):
        return Point(self.x+p.x,self.y+p.y)
    def __truediv__(self, num):
        return Point(self.x/num, self.y/num)
    def __mul__(self, num):
        return Point(self.x*num, self.y*num)

class Line:
    def __init__(self,a=0,b=0,c=0) -> None:
        self.a = a
        self.b = b
        self.c = c
    def __str__(self):
        return '%sx + %sy + %s = 0' % (self.a, self.b, self.c)
    def __repr__(self):
        return '%sx + %sy + %s = 0' % (self.a, self.b, self.c)
    def compute(self, point): # 计算点落在线哪一边
        return self.a * point.x + self.b*point.y + self.c
    def buildByPointAndSlope(self, point, slope): # 通过点与斜率构建
        if slope == None: # 表示斜率无穷大
            self.a = 1
            self.b = 0
            self.c = -point.x
        elif slope == 0:
            self.a = 0
            self.b = 1
            self.c = -point.y
        else:
            self.a = slope
            self.b = -1
            self.c = point.y-slope*point.x

class Flat:
    def __init__(self, points) -> None:
        self.points = list(map(lambda x: Point(*x), points))
    
    def getDivision(self):
        pointsLen = len(self.points)
        if pointsLen < 2:
                A = set(self.points)
                B = set()
                return { "A": A, "B": B }

        distanceMatrix = [
            [0 for j in range(pointsLen)]
            for i in range(pointsLen)
        ]
        maxDistance = -1
        maxDistancePair = None
                     
        # 获取中垂线
        def getPerpendicularBisector(pointPair):
            midPoint = (pointPair[0] + pointPair[1])/2
            subX =  pointPair[1].x-pointPair[0].x
            subY = pointPair[1].y-pointPair[0].y
            slope = None
            if subX == 0:
                slope = 0
            elif subY == 0:
                slope = None
            else:
                slope = -subX/subY
            line = Line()
            line.buildByPointAndSlope(midPoint, slope)
            return line

        for i in range(pointsLen):
            for j in range(i+1, pointsLen):
                distanceMatrix[j][i] = distanceMatrix[i][j] = self.points[i].distant(self.points[j])
                if distanceMatrix[i][j] > maxDistance:
                    maxDistance = distanceMatrix[i][j]
                    maxDistancePair = (self.points[i], self.points[j])
        
        l = getPerpendicularBisector(maxDistancePair)
        A = set()
        B = set()
        for point in self.points:
            if l.compute(point) == 0:
                A = set(self.points)
                B = set()
                return { "A": A, "B": B }
            elif l.compute(point) < 0:
                A.add(point)
            else:
                B.add(point)
        
        for pa in A:
            for pb in B:
                l_ab = getPerpendicularBisector((pa,pb))
                for a in A:
                    if l_ab.compute(a) >= 0:
                        A = set(self.points)
                        B = set()
                        return { "A": A, "B": B }
                for b in B:
                    if l_ab.compute(b) <= 0:
                        A = set(self.points)
                        B = set()
                        return { "A": A, "B": B }
        
        return { "A": A, "B": B }


def test1():
    flat = Flat([(-9,0),(9,0),(-1,2),(1,-2)])
    print(flat.getDivision())

def test2():
    flat = Flat([(0,0),(1,1),(2,2)])
    print(flat.getDivision())

def test3():
    flat = Flat([(-3,0),(3,0),(-1,2),(1,-2)])
    print(flat.getDivision())

def test4():
    flat = Flat([(-1,0),(1,0)])
    print(flat.getDivision())

def test5():
    flat = Flat([(-1,0)])
    print(flat.getDivision())

test1()
test2()
test3()
test4()
test5()