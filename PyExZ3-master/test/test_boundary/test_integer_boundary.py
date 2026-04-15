def integer_boundary(x):
    if x == 0:
        return "Zero"
    elif x == 1:
        return "One"
    elif x == -1:
        return "Minus one"
    elif x == 2147483647:
        return "Max int"
    elif x == -2147483648:
        return "Min int"
    else:
        return "Other"

def expected_result():
    return ["Zero", "One", "Minus one", "Max int", "Min int", "Other"]
