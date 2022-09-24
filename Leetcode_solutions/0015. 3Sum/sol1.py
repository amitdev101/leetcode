List = list
class Solution:
    def threeSum(self, nums: List[int]) -> List[List[int]]:
        res = set()
        nums.sort()
        st = set()
        n = len(nums)
        for i in range(n):
            if i>2 and nums[i]==nums[i-2]: # no point in selecting same two numbers everytime
                continue
            for j in range(i+1, n):
                target = -(nums[i] + nums[j]) 
                if target in st: 
                    res.add((nums[i], nums[j], target))
            st.add(nums[i]) ### adding every element in set
        return list(res)

if __name__=='__main__':
    sol = Solution()
    input = [1,1,-1,0,0,0]
    print(sol.threeSum(input))