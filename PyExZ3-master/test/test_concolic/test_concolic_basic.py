def concolic_basic(x, y):
    if x > 0:
        if y > 0:
            return "Both positive"
        else:
            return "x positive, y non-positive"
    else:
        if y > 0:
            return "x non-positive, y positive"
        else:
            return "Both non-positive"

def expected_result():
    return ["Both positive", "x positive, y non-positive", "x non-positive, y positive", "Both non-positive"]
