// https://leetcode.com/problems/longest-valid-parentheses/discuss/1279254/My-C%2B%2B-Simple-Solution


int longestValidParentheses(string s) {
        int  maxCount =0, n = s.size();
        stack<int> stk;
        
        for(int i=0;i<n;i++)
        {
            if(s[i] == '(') 
                stk.push(i);
            
           else if(!stk.empty() && s[stk.top()] == '(')
                stk.pop();
                
            else 
                stk.push(i);
        }
        if(stk.empty())
            return n;
        
        int end = n, start=0;
        while(!stk.empty())
        {
            int start = stk.top();
            stk.pop();
            
            maxCount = max(maxCount, end -start-1);
            
            end = start;
        }
        
        maxCount = max(maxCount, end);
        
        return maxCount;
    }