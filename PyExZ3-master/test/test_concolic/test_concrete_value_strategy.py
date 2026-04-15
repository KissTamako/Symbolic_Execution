def concrete_value_strategy_test(x, y):
    if x > 0:
        if y > 0:
            return "Both positive"
        elif y == 0:
            return "x positive, y zero"
        else:
            return "x positive, y negative"
    elif x == 0:
        if y > 0:
            return "x zero, y positive"
        elif y == 0:
            return "Both zero"
        else:
            return "x zero, y negative"
    else:
        if y > 0:
            return "x negative, y positive"
        elif y == 0:
            return "x negative, y zero"
        else:
            return "Both negative"

def expected_result():
    return ["Both positive", "x positive, y zero", "x positive, y negative",
            "x zero, y positive", "Both zero", "x zero, y negative",
            "x negative, y positive", "x negative, y zero", "Both negative"]
