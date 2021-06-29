class Solution:
    def isValid(self, s: str) -> bool:
        if s:
            while '()' in s or '{}' in s or '[]' in s:
                s = s.replace('()', '').replace('{}', '').replace('[]', '')
        if s:
            return False

        return True
        
        