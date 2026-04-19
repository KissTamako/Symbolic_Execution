def main():
    inword = input()
    print(plural(inword))

def plural(a):
    if a[-1] in 'sx' or a[-2:] in ['sh','ch']:
        return a+'es'
    elif a[-1] in 'o':
        return a+'es'
    elif a[-1] in 'y':
        return a[0:-1]+'ies'
    else:
        return a+'s'


main()

