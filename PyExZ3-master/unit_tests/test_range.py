def test_range(x):
    """Test range type with symbolic execution"""
    r = range(10)
    if x in r:
        return "x is in range(10)"
    else:
        return "x is not in range(10)"

if __name__ == "__main__":
    # Test with concrete values
    print(test_range(5))  # Should be "x is in range(10)"
    print(test_range(15))  # Should be "x is not in range(10)"
