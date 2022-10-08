class TrieNode:
    """General TrieNode to store Node data
    """
    def __init__(self,char = ""):
        self.char = char 
        self.isEnd = False
        self.count = 0
        self.children = dict()


class Trie:
    def __init__(self):
        self.root = TrieNode()
        
    def insert(self,word:str) -> None:
        try :
            if not word:
                return
            node = self.root
            for char in word:
                if char in node.children:
                    node = node.children[char]
                else:
                    new_node = TrieNode(char)
                    node.children[char] = new_node
                    node = new_node
            node.isEnd = True
            node.count+=1
        except Exception as e:
            raise Exception("Error occured in when inserting : " + str(e) )

    
    def query(self,word)->int:
        '''Return count if word is present'''
        # TODO 
        ...