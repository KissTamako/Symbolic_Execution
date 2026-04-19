a=input()
b=[]
for i in a:
    b.append(i)
for i in range(len(b)):
    if b[i] in 'qwertyuiopasdfghjklzxcvbnm':
        b[i]=chr(96+27-(ord(b[i])-96))
    elif b[i] in 'QWERTYUIOPASDFGHJKLZXCVBNM':
        b[i]=chr(63+27-(ord(b[i])-65))
print(a)
print(''.join(b))

