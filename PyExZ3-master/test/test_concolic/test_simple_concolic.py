def simple_concolic(x):
    if x > 0:
        return "Positive"
    elif x == 0:
        return "Zero"
    else:
        return "Negative"

def expected_result():
    return ["Positive", "Zero", "Negative"]
