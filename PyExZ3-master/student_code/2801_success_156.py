s=input()
n=0
for i in s:
    if i in "1234567890":
        n=n+1
        break
for i in s:
    if "a"<=i<="z":
        n=n+1
        break
for i in s:
    if "A"<=i<="Z":
        n=n+1
        break
for i in s:
    if i in "~!@#$%^&*()_=-/,.?<>;:[]{ }|\ ":
        n=n+1
        break
if len(s)>=8:
    n=n+1
print(n)
