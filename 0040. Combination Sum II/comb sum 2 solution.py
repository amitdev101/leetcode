class Solution(object):
    def combinationSum2(self, candidates, target):
        """
        :type candidates: List[int]
        :type target: int
        :rtype: List[List[int]]
        """
        candidates.sort()
        ansset = set()
        # it can work without set also as i am checking duplicate number in the code itself
        n = len(candidates)
        def comb(currlist,currsum,i):
            if currsum==target:
                ansset.add(tuple(currlist))
            elif i==n or currsum>target:
                return
            else:
                # new solution with iterative duplication check
                index = i
                for i in range(index,len(candidates)):
                    if (i>index) and candidates[i]==candidates[i-1]:
                        continue
                    elif candidates[i] >(target-currsum):
                        break
                    else :
                        comb(currlist+[candidates[i]],currsum+candidates[i],i+1)
                        
                        
        comb([],0,0)
        return list(ansset)
            
        