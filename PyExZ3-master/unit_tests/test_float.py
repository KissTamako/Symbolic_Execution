from symbolic.args import symbolic

@symbolic(x=0.0)
def test_float(x):
    if x > 0.5:
        if x < 1.5:
            return "between 0.5 and 1.5"
        else:
            return "greater than or equal to 1.5"
    else:
        return "less than or equal to 0.5"

def expected_result():
    return ["less than or equal to 0.5", "between 0.5 and 1.5", "greater than or equal to 1.5"]
