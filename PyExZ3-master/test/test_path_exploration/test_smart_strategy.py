def smart_strategy_test(x, y, z):
    if x > 0:
        if y > 0:
            if z > 0:
                return "All positive"
            else:
                return "x,y positive, z non-positive"
        else:
            if z > 0:
                return "x positive, y non-positive, z positive"
            else:
                return "x positive, y,z non-positive"
    else:
        if y > 0:
            if z > 0:
                return "x non-positive, y,z positive"
            else:
                return "x non-positive, y positive, z non-positive"
        else:
            if z > 0:
                return "x,y non-positive, z positive"
            else:
                return "All non-positive"

def expected_result():
    return ["All positive", "x,y positive, z non-positive", "x positive, y non-positive, z positive", 
            "x positive, y,z non-positive", "x non-positive, y,z positive", "x non-positive, y positive, z non-positive", 
            "x,y non-positive, z positive", "All non-positive"]
