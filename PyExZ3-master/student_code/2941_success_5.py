def count_foreign(ids):
        n=0
        for i in ids:
            if i[0]=='L':
                n+=1
        return n

origin=input().split()
print(count_foreign(origin))

