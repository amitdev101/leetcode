class Solution(object):
    def combinationSum(self, candidates, target):
        """
        :type candidates: List[int]
        :type target: int
        :rtype: List[List[int]]
        """
        candidates = list(set(candidates))
        n = len(candidates)
        anslist = list()
        
        def getcombinations(currlist,i,currsum):
            if currsum==target:
                anslist.append(currlist)
            elif i==n or currsum>target:
                return
            else :
                # skipping the element 
                getcombinations(currlist,i+1,currsum)
                # taking the element and keeping the index same(As we can take this number infinite times)
                getcombinations(currlist+[candidates[i]],i,currsum+candidates[i])
        
        getcombinations([],0,0)
        return anslist
            
                