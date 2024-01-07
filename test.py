class Solution(object):
    def minCostClimbingStairs(self, cost):
        """
        :type cost: List[int]
        :rtype: int
        """
        self.dp = []
        self.cost = cost
        self.descend(len(cost) - 2, 0)
        self.descend(len(cost) - 1, 0)
        print (self.dp)
        return min(self.dp)
        
    def descend(self,index, cur_cost):
        if index == 0 or index == 1:
            self.dp.append(cur_cost + self.cost[index])
        else:
            self.descend(index-1, self.cost[index])
            self.descend(index-2, self.cost[index])

solution = Solution()
print (solution.minCostClimbingStairs([10,15,20]))