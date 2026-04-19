s={"A":"A","B":"B","C":"C","D":"D","E":"E"}
n=eval(input())
if n>=90:
    print(s["A"])
elif n>=80 and n<90:
    print(s["B"])
elif n>=70 and n<80:
    print(s["C"])
elif n>=60 and n<70:
    print(s["D"])
else:
    print(s["E"])


