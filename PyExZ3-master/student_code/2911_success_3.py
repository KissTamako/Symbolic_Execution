a=input()
s=''
for i in a:
    s+=str((int(i)+5)%10)
s1=list(s)
s1.reverse()
b=''.join(s1)
print(b)
