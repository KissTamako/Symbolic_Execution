icard = input()
birthday =  icard[6:10]+"-"+icard[10:12]+"-"+icard[12:14]
mask = mask = icard.replace(icard[6:14],"********")
print(birthday)
print(mask)

