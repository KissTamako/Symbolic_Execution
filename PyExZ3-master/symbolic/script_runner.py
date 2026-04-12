# Copyright: see copyright.txt
"""
Script mode execution for symbolic execution.

Week 1: Skeleton implementation
Week 3: Will implement actual script execution functionality
"""

import sys
import os
from typing import Dict, List, Any, Optional, Tuple, Union
from pathlib import Path

from .invocation import FunctionInvocation
from .loader import Loader
from .input_model import InputModel, ModelType


class ScriptRunner:
    """Runs Python scripts in symbolic execution mode."""
    
    def __init__(self):
        self.script_path: Optional[Path] = None
        self.input_model: Optional[InputModel] = None
        self.symbolic_inputs: Dict[str, Any] = {}
        self.execution_result: Any = None
        self.exception: Optional[Exception] = None
    
    def load_script(self, script_path: Union[str, Path]) -> bool:
        """
        Load a Python script for execution.
        
        Args:
            script_path: Path to Python script
        
        Returns:
            True if script loaded successfully
        """
        self.script_path = Path(script_path)
        if not self.script_path.exists():
            print(f"Error: Script not found: {script_path}")
            return False
        
        # TODO: Week 3 - Implement actual script loading
        print(f"[INFO] Script loading not yet implemented (Week 1)")
        return True
    
    def set_input_model(self, model: InputModel):
        """Set input model for script execution."""
        self.input_model = model
        if model and model.model_type == ModelType.SCRIPT:
            self.symbolic_inputs = model.generate_symbolic_inputs()
    
    def create_script_invocation(self) -> Optional[FunctionInvocation]:
        """
        Create a script invocation for symbolic execution.
        
        Returns:
            FunctionInvocation for script execution, or None if failed
        """
        if not self.script_path:
            print("Error: No script loaded")
            return None
        
        from .loader import ScriptLoader
        
        try:
            # Create a ScriptLoader instance
            loader = ScriptLoader(str(self.script_path), use_ast_transform=True)
            
            # Get the FunctionInvocation from loader
            invocation = loader.createInvocation()
            
            # If we have an input model, add symbolic arguments
            if self.input_model and invocation:
                # Get symbolic inputs from model
                symbolic_inputs = self.input_model.get_symbolic_inputs()
                
                # Add each symbolic input as an argument to the invocation
                for name, value in symbolic_inputs.items():
                    # Skip special inputs that will be handled by loader
                    if name in ['__stdin_lines', '__argv']:
                        continue
                    
                    # Add argument constructor
                    invocation.addArgumentConstructor(
                        name, 
                        value, 
                        lambda n, v: v  # Simple identity function for now
                    )
            
            return invocation
            
        except Exception as e:
            print(f"Error creating script invocation: {e}")
            return None
    
    def execute_script(self, symbolic_inputs: Optional[Dict[str, Any]] = None) -> Tuple[Any, Optional[Exception]]:
        """
        Execute the script with given symbolic inputs.
        
        Args:
            symbolic_inputs: Symbolic input values
        
        Returns:
            Tuple of (execution_result, exception)
        """
        if symbolic_inputs:
            self.symbolic_inputs = symbolic_inputs
        
        if not self.script_path:
            return None, RuntimeError("No script loaded")
        
        try:
            # Read script content
            script_content = self.script_path.read_text(encoding='utf-8')
            
            # Prepare execution namespace
            namespace = {
                '__name__': '__main__',
                '__file__': str(self.script_path),
            }
            
            # Handle sys.argv simulation
            import sys
            
            # Store original argv
            original_argv = sys.argv.copy()
            
            # Set up simulated argv based on symbolic inputs
            if '__argv' in self.symbolic_inputs:
                argv_value = self.symbolic_inputs['__argv']
                if isinstance(argv_value, list):
                    sys.argv = [str(self.script_path)] + [str(v) for v in argv_value]
                else:
                    sys.argv = [str(self.script_path), str(argv_value)]
            else:
                sys.argv = [str(self.script_path)]
            
            # Handle input() function replacement
            import builtins
            original_input = builtins.input
            
            # Track input calls for symbolic input injection
            input_call_count = 0
            stdin_values = self.symbolic_inputs.get('__stdin_lines', [])
            
            def symbolic_input(prompt=""):
                nonlocal input_call_count
                if input_call_count < len(stdin_values):
                    value = stdin_values[input_call_count]
                    input_call_count += 1
                    # Convert to string if not already
                    if not isinstance(value, str):
                        value = str(value)
                    return value
                else:
                    # Fallback to empty string if no more symbolic inputs
                    return ""
            
            builtins.input = symbolic_input
            
            # Execute the script
            try:
                # Compile and execute
                code = compile(script_content, str(self.script_path), 'exec')
                exec(code, namespace, namespace)
                
                # Try to get result from main() function or last expression
                if 'main' in namespace and callable(namespace['main']):
                    self.execution_result = namespace['main']()
                elif '__result__' in namespace:
                    self.execution_result = namespace['__result__']
                else:
                    # No explicit result
                    self.execution_result = None
                    
            finally:
                # Restore original functions
                builtins.input = original_input
                sys.argv = original_argv
            
            self.exception = None
            return self.execution_result, None
            
        except Exception as e:
            self.exception = e
            return None, e
    
    def analyze_script_structure(self) -> Dict[str, Any]:
        """
        Analyze script structure to identify entry points and dependencies.
        
        Returns:
            Dictionary with script analysis results
        """
        if not self.script_path:
            return {}
        
        # TODO: Week 3 - Implement actual script analysis
        return {
            "file_path": str(self.script_path),
            "file_size": self.script_path.stat().st_size if self.script_path.exists() else 0,
            "has_main": self._has_main_guard(),
            "imports": self._extract_imports(),
            "functions": [],
            "classes": [],
            "top_level_statements": 0
        }
    
    def _has_main_guard(self) -> bool:
        """Check if script has __name__ == '__main__' guard."""
        if not self.script_path or not self.script_path.exists():
            return False
        
        try:
            content = self.script_path.read_text()
            return 'if __name__ == "__main__"' in content or "__name__ == '__main__'" in content
        except:
            return False
    
    def _extract_imports(self) -> List[str]:
        """Extract import statements from script."""
        if not self.script_path or not self.script_path.exists():
            return []
        
        try:
            content = self.script_path.read_text()
            imports = []
            lines = content.split('\n')
            for line in lines:
                line = line.strip()
                if line.startswith('import ') or line.startswith('from '):
                    imports.append(line)
            return imports
        except:
            return []
    
    def get_execution_summary(self) -> Dict[str, Any]:
        """Get summary of script execution."""
        return {
            "script_path": str(self.script_path) if self.script_path else None,
            "execution_successful": self.exception is None,
            "execution_result": self.execution_result,
            "exception": str(self.exception) if self.exception else None,
            "symbolic_inputs_used": self.symbolic_inputs,
            "input_model_type": self.input_model.model_type if self.input_model else None
        }


def create_script_invocation(script_path: Union[str, Path], 
                            input_model: Optional[InputModel] = None) -> Optional[FunctionInvocation]:
    """
    Convenience function to create script invocation.
    
    Args:
        script_path: Path to Python script
        input_model: Input model for script execution
    
    Returns:
        FunctionInvocation for script execution
    """
    runner = ScriptRunner()
    if not runner.load_script(script_path):
        return None
    
    if input_model:
        runner.set_input_model(input_model)
    
    return runner.create_script_invocation()


def create_function_invocation(function_path: Union[str, Path], 
                              function_name: Optional[str] = None) -> Optional[FunctionInvocation]:
    """
    Convenience function to create function invocation.
    This maintains compatibility with existing function mode.
    
    Args:
        function_path: Path to Python file containing function
        function_name: Name of function to invoke
    
    Returns:
        FunctionInvocation for function execution
    """
    # This is a wrapper around existing loader functionality
    from .loader import loaderFactory
    
    # TODO: Week 3 - Integrate with enhanced loader
    print(f"[INFO] Enhanced function invocation not yet implemented (Week 1)")
    return None


# Compatibility imports
import sys
if sys.version_info < (3, 10):
    from typing import Union
else:
    from typing import Union