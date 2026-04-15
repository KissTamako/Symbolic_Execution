from symbolic.args import symbolic

@symbolic(x=0)
def test_minimal(x):
    if x > 0:
        return 1
    else:
        return 0

def expected_result():
    return [0, 1]
