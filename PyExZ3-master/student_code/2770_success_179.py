x = input()
y = input()
def anagramSolution(s1,s2):
    if len(s1)!=len(s2):
        return False
    list_1=list(s1)
    n=len(s1) 
    for c in s2:
        found = False 
        for i in range(n): 
            if list_1[i]==c:
                return True 
            list_1[i]=None 
            break
        if not found: 
            return False
    return True
print(anagramSolution(x,y)) 
