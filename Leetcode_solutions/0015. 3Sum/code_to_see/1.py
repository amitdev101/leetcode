List = list
Vector = list[int]
print(List)
class Solution:
    def threeSum(self, nums: List[int]) -> List[List[int]]:
        nums = sorted(nums)
        ans = []
        for a_pos in range(len(nums)-2):
            target = 0 - nums[a_pos]
            b_pos, c_pos = a_pos + 1, len(nums) - 1
            ##############REDUCE DUPLICATE################
            if a_pos > 0 and nums[a_pos] == nums[a_pos-1]: ### here should be apos>2 and apos-2 
                continue
            ##############################################
            while b_pos < c_pos:
                b_c = nums[b_pos] + nums[c_pos]
                if b_c < target:
                    b_pos += 1
                elif b_c > target:
                    c_pos -= 1
                else:
                    ans.append([nums[a_pos], nums[b_pos], nums[c_pos]])
                    ##################REDUCE DUPLICATE###################
                    while b_pos < c_pos and nums[b_pos] == nums[b_pos+1]:
                        b_pos += 1
                    while b_pos < c_pos and nums[c_pos] == nums[c_pos-1]:
                        c_pos -= 1
                    b_pos += 1
                    c_pos -= 1
                    #####################################################
        return ans

if __name__=='__main__':
    numlist = [-1,-1,-1,-2]
    sol = Solution()
    ans = sol.threeSum(numlist)
    print(ans)