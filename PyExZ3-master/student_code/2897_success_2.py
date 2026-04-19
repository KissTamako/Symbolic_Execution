Roma=list(input())
Roma=Roma[::-1]
nums=[]
for x in Roma:
    if x == "I":
        nums.append(1)
    if x == "V":
        nums.append(5)
    if x == "X":
        nums.append(10)
    if x == "L":
        nums.append(50)
    if x == "C":
        nums.append(100)
    if x == "D":
        nums.append(500)
    if x == "M":
        nums.append(1000)
lis=[]
for x in list(range(len(nums))):
    if x == 0:
        lis.append(nums[x])
    elif x >= 1:
        if nums[x] >= nums[x-1]:
            lis.append(nums[x]) 
        elif nums[x]<nums[x-1]:
            lis.append(-nums[x])
a=sum(lis)
print(a)
