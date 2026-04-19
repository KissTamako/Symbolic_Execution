a=input()
for i in a:
    if i.isalpha():
        if i.islower():
            b=chr(25-ord(i)+ord('a')*2)
            print(b,end='')
        elif i.isupper():
            b=chr(25-ord(i)+ord('A')*2)
            print(b,end='')
    else:
        print(i,end='')
