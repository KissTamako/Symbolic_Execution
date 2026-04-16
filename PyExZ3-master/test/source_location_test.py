# Test case for source location information

def source_location_test(x):
    """Test function to verify source location tracking"""
    if x > 0:
        return "Positive"
    elif x < 0:
        return "Negative"
    else:
        return "Zero"

# Expected result function
def expected_result():
    return ["Positive", "Negative", "Zero"]
