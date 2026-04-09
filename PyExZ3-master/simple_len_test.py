#!/usr/bin/env python
import os
import sys

os.chdir(os.path.dirname(os.path.abspath(__file__)))
print("Current dir:", os.getcwd())

# Import the necessary modules
sys.path.insert(0, '.')

try:
    from symbolic.loader import Loader
    from symbolic.explore import ExplorationEngine
    
    test_file = os.path.abspath('test/len_test.py')
    print(f"Testing file: {test_file}")
    
    # Create loader and engine
    app = Loader(test_file, 'len_test', use_ast_transform=False)
    print("Loader created successfully")
    
    engine = ExplorationEngine(app.createInvocation(), solver='z3')
    generatedInputs, returnVals, path = engine.explore(5)
    
    print(f"Generated inputs: {len(generatedInputs)}")
    print(f"Return values: {returnVals}")
    
    # Check if we got expected results
    if len(generatedInputs) >= 2:
        print("PASS: Found multiple paths as expected")
    else:
        print(f"FAIL: Expected at least 2 paths, got {len(generatedInputs)}")
        
except Exception as e:
    print(f"ERROR: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()