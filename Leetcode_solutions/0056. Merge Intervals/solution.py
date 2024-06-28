from typing import List


class Solution:
    def merge(self, intervals: List[List[int]]) -> List[List[int]]:
        if not intervals:
            return []
        intervals.sort(key = lambda x: x[0])
        # print(intervals)
        result = list()
        prev_interval = None
        for interval in intervals:
            if not prev_interval:
                prev_interval = interval
                
            if prev_interval[0] <= interval[0] <= prev_interval[1]:
                # interval can be merged
                prev_interval[1] = max(prev_interval[1], interval[1])
            else:
                # this interval cannot be merged.
                # store prev_interval
                result.append(prev_interval)
                prev_interval = interval
        if prev_interval:
            result.append(prev_interval)
        return result

if __name__=='__main__':
    sol = Solution()
    intervals = [[1,3],[2,6],[8,10],[15,18]]
    merged_intervals = sol.merge(intervals=intervals)
    print(merged_intervals)
        