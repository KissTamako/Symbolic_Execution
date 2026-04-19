icard = input()
birthday =  str(icard[6:10])+'-'+str(icard[10:12])+'-'+str(icard[12:14])
mask = str(icard[0:6])+'********'+ str(icard[14:])
print(birthday)
print(mask)

