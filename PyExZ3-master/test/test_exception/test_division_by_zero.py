def division_by_zero(y):
    if y == 0:
        return "Division by zero"
    elif y == 1:
        return "1.0"
    elif y == -1:
        return "-1.0"
    else:
        return str(1 / y)

def expected_result():
    return ["Division by zero", "1.0", "-1.0"]
