sr=input()
s=''
for ch in sr:
    if ch>="A" and ch<="Z":
        s+=chr(ord("Z")-(ord(ch)-ord('A')))
    elif ch>='a' and ch<='z':
        s+=chr(ord('z')-(ord(ch)-ord('a')))
    else:
        s+=ch
print(s)

