#!/usr/bin/env python
"""
Test script for Week 2 functionality.
"""

import sys
import os
import tempfile
from pathlib import Path

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_ast_transform():
    """Test AST transformation module."""
    print("=== Testing AST Transformation ===")
    
    try:
        import symbolic.ast_transform as at
        
        # Test 1: Basic transformation
        code = """
x = int(y)
z = str(w)
r = range(10)
"""
        tree = at.transform_ast(code, "test.py")
        print("✓ AST transformation successful")
        
        # Test 2: Compilation
        import types
        code_obj = at.compile_transformed_module(tree, "test_module")
        print("✓ AST compilation successful")
        
        # Test 3: Branch hook injection
        code_with_branch = """
if x > 0:
    print("positive")
else:
    print("non-positive")
"""
        tree_with_hooks = at.transform_ast(code_with_branch, "test.py", inject_branch_hooks=True)
        print("✓ Branch hook injection successful")
        
        return True
    except Exception as e:
        print(f"✗ AST transformation test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_runtime_helpers():
    """Test runtime helper functions."""
    print("\n=== Testing Runtime Helpers ===")
    
    try:
        import symbolic.runtime_helpers as rh
        
        # Test _se_int
        from symbolic.symbolic_types.symbolic_int import SymbolicInteger
        result = rh._se_int(5)
        assert isinstance(result, SymbolicInteger)
        print(f"✓ _se_int: {result}")
        
        # Test _se_str
        from symbolic.symbolic_types.symbolic_str import SymbolicStr
        result = rh._se_str("hello")
        assert isinstance(result, SymbolicStr)
        print(f"✓ _se_str: {result}")
        
        # Test _se_range
        result = rh._se_range(10)
        assert isinstance(result, range)
        print(f"✓ _se_range: {result}")
        
        # Test unwrap
        symbolic_int = SymbolicInteger("test", 42, None)
        unwrapped = rh.unwrap(symbolic_int)
        assert unwrapped == 42
        print(f"✓ unwrap: {unwrapped}")
        
        # Test wrap_concrete_constant
        wrapped = rh.wrap_concrete_constant(100)
        assert isinstance(wrapped, SymbolicInteger)
        print(f"✓ wrap_concrete_constant: {wrapped}")
        
        return True
    except Exception as e:
        print(f"✗ Runtime helpers test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_exporters():
    """Test JSON and SMT exporters."""
    print("\n=== Testing Exporters ===")
    
    try:
        # Create temporary directory for exports
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            
            # Test JSON exporter
            from symbolic.exporters.json_exporter import JSONExporter
            json_exporter = JSONExporter(tmp_path)
            
            # Create a mock constraint
            class MockConstraint:
                def get_path_predicates(self):
                    return [
                        {
                            'expr': 'x > 0',
                            'result': True,
                            'source_file': 'test.py',
                            'source_line': 10,
                            'branch_id': 0,
                            'vars': ['x']
                        }
                    ]
            
            constraint = MockConstraint()
            inputs = {'x': 5}
            
            json_file = json_exporter.export_path_constraint(
                constraint, inputs, 42, None, 0
            )
            assert json_file.exists()
            print(f"✓ JSON exporter created file: {json_file}")
            
            # Test SMT exporter
            from symbolic.exporters.smt_exporter import SMTExporter
            smt_exporter = SMTExporter(tmp_path)
            
            smt_file = smt_exporter.export_path_constraint_smt2(constraint, 0)
            assert smt_file.exists()
            print(f"✓ SMT exporter created file: {smt_file}")
            
            # Verify file contents
            with open(json_file, 'r') as f:
                json_content = f.read()
                assert '"tool": "PyExZ3"' in json_content
            
            with open(smt_file, 'r') as f:
                smt_content = f.read()
                assert '(set-logic' in smt_content or ';' in smt_content
            
            return True
    except Exception as e:
        print(f"✗ Exporters test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_z3_wrapper_export():
    """Test Z3 wrapper export functionality."""
    print("\n=== Testing Z3 Wrapper Export ===")
    
    try:
        from symbolic.z3_wrap import Z3Wrapper
        from symbolic.predicate import Predicate
        
        # Create a simple predicate for testing
        from symbolic.symbolic_types.symbolic_int import SymbolicInteger
        
        # We need a proper symbolic type for testing
        # This is a simplified test
        wrapper = Z3Wrapper()
        print("✓ Z3Wrapper initialized")
        
        # Note: Full Z3 integration testing would require actual predicates
        # For now, just ensure the module loads and has the new methods
        
        assert hasattr(wrapper, 'build_solver')
        assert hasattr(wrapper, 'export_current_query_to_smt2')
        assert hasattr(wrapper, 'export_constraints_to_smt2')
        
        print("✓ Z3Wrapper has all export methods")
        
        return True
    except Exception as e:
        print(f"✗ Z3 wrapper test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_loader_integration():
    """Test loader integration with AST transformation."""
    print("\n=== Testing Loader Integration ===")
    
    try:
        # Create a simple test module
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            test_file = tmp_path / "test_module.py"
            
            test_code = """
@concrete(x=5)
def test_function(x):
    y = int(x)  # This should be transformed to _se_int(x)
    z = str(y)  # This should be transformed to _se_str(y)
    if y > 0:   # This should have branch hook injected
        return "positive"
    else:
        return "non-positive"
"""
            test_file.write_text(test_code)
            
            # Test loader with AST transformation
            from symbolic.loader import loaderFactory
            
            # Note: This is a complex integration test
            # For now, just verify the loader imports correctly
            print("✓ Loader module imported successfully")
            
            # Verify loaderFactory accepts use_ast_transform parameter
            import inspect
            sig = inspect.signature(loaderFactory)
            assert 'use_ast_transform' in sig.parameters
            print("✓ loaderFactory accepts use_ast_transform parameter")
            
            return True
    except Exception as e:
        print(f"✗ Loader integration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all Week 2 tests."""
    print("Running Week 2 functionality tests...")
    print("=" * 50)
    
    results = []
    
    # Run tests
    results.append(("AST Transformation", test_ast_transform()))
    results.append(("Runtime Helpers", test_runtime_helpers()))
    results.append(("Exporters", test_exporters()))
    results.append(("Z3 Wrapper Export", test_z3_wrapper_export()))
    results.append(("Loader Integration", test_loader_integration()))
    
    # Summary
    print("\n" + "=" * 50)
    print("TEST SUMMARY")
    print("=" * 50)
    
    all_passed = True
    for name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{name}: {status}")
        if not passed:
            all_passed = False
    
    print("\n" + "=" * 50)
    if all_passed:
        print("✅ All Week 2 tests passed!")
        return 0
    else:
        print("❌ Some Week 2 tests failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())