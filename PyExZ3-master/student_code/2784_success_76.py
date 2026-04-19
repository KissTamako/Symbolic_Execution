def main():
    inword = input()
    print(plural(inword))

def plural(x):
    if x.endswith("s") or x.endswith("x") or x.endswith("ch") or x.endswith("sh") or x.endswith("o"):
        return x+"es"
    elif x.endswith("y"):
        return x[0:len(x)-1]+"ies"
    else:
        return x+"s"

main()

