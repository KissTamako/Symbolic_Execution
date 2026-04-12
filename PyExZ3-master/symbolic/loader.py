# Copyright: copyright.txt

import inspect
import re
import os
import sys
import importlib
import types
from pathlib import Path

from .invocation import FunctionInvocation
from .symbolic_types import SymbolicInteger, getSymbolic
from .ast_transform import transform_ast, compile_transformed_module, setup_branch_hook_globals
from .path_utils import ensure_paths_for_file, diagnose_import_error

# The built-in definition of len wraps the return value in an int() constructor, destroying any symbolic types.
# By redefining len here we can preserve symbolic integer types.
import builtins
builtins.len = (lambda x : x.__len__())

class Loader:
	def __init__(self, filename, entry, use_ast_transform=True):
		self._fullPath = filename  # Store full path
		self._fileName = os.path.basename(filename)
		self._fileName = self._fileName[:-3]  # Remove .py extension
		
		if (entry == ""):
			self._entryPoint = self._fileName
		else:
			self._entryPoint = entry
		self._use_ast_transform = use_ast_transform
		self._resetCallback(True)

	def getFile(self):
		return self._fileName

	def getEntry(self):
		return self._entryPoint
	
	def createInvocation(self):
		inv = FunctionInvocation(self._execute,self._resetCallback)
		func = self.app.__dict__[self._entryPoint]
		# Python 3.11 compatibility: replace getargspec with signature
		sig = inspect.signature(func)
		argspec_args = list(sig.parameters.keys())
		# check to see if user specified initial values of arguments
		if "concrete_args" in func.__dict__:
			for (f,v) in func.concrete_args.items():
				if not f in argspec_args:
					print("Error in @concrete: " +  self._entryPoint + " has no argument named " + f)
					raise ImportError()
				else:
					Loader._initializeArgumentConcrete(inv,f,v)
		if "symbolic_args" in func.__dict__:
			for (f,v) in func.symbolic_args.items():
				if not f in argspec_args:
					print("Error (@symbolic): " +  self._entryPoint + " has no argument named " + f)
					raise ImportError()
				elif f in inv.getNames():
					print("Error (@symbolic): " +  self._entryPoint + " has multiple definitions for " + f)
					raise ImportError()
				else:
					Loader._initializeArgumentSymbolic(inv,f,v,SymbolicInteger)
		# initalize all remaining arguments with symbolic types
		for a in argspec_args:
			if not a in inv.getNames():
				Loader._initializeArgumentSymbolic(inv, a, 0, SymbolicInteger)
		return inv

	# need these here (rather than inline above) to correctly capture values in lambda
	def _initializeArgumentConcrete(inv,f,val):
		inv.addArgumentConstructor(f, val, lambda n,v: val)

	def _initializeArgumentSymbolic(inv,f,val,st):
		inv.addArgumentConstructor(f, val, lambda n,v: st(n,v))

	def executionComplete(self, return_vals):
		if "expected_result" in self.app.__dict__:
			return self._check(return_vals, self.app.__dict__["expected_result"]())
		if "expected_result_set" in self.app.__dict__:
			return self._check(return_vals, self.app.__dict__["expected_result_set"](),False)
		else:
			print(self._fileName + ".py contains no expected_result function")
			return None

	# -- private

	def _resetCallback(self,firstpass=False):
		self.app = None
		if firstpass and self._fileName in sys.modules:
			print("There already is a module loaded named " + self._fileName)
			raise ImportError()
		try:
			if (not firstpass and self._fileName in sys.modules):
				del(sys.modules[self._fileName])
			
			# Load module with AST transformation if enabled
			if self._use_ast_transform:
				self.app = self._load_with_ast_transform()
			else:
				# Use improved import method with path_utils integration
				# Ensure the file's directory is in sys.path
				module_name = ensure_paths_for_file(self._fullPath)
				
				# Use importlib for more reliable import
				try:
					spec = importlib.util.spec_from_file_location(module_name, self._fullPath)
					if spec is None:
						raise ImportError(f"Could not create spec for {self._fullPath}")
					
					self.app = importlib.util.module_from_spec(spec)
					spec.loader.exec_module(self.app)
					
					# Also add to sys.modules for consistency
					sys.modules[module_name] = self.app
				except Exception as e:
					# Fall back to traditional import
					print(f"[WARN] importlib import failed, falling back to __import__: {e}")
					self.app = __import__(module_name)
			
			# For script mode, we don't require a specific entry function
			# The module will be executed as top-level code
			has_script_flag = getattr(self, '_is_script', False)
			if not has_script_flag:
				# Function mode: check that entry point exists and is callable
				if not self._entryPoint in self.app.__dict__ or not callable(self.app.__dict__[self._entryPoint]):
					print("File " +  self._fileName + ".py doesn't contain a function named " + self._entryPoint)
					raise ImportError()
			else:
				# Script mode: check if __main__ exists, but don't require it
				# If __main__ doesn't exist, we'll execute the module's top-level code
				pass
		except Exception as arg:
			print("Couldn't import " + self._fileName)
			print(arg)
			
			# Provide diagnostic information
			suggestions = diagnose_import_error(self._fileName, arg)
			if suggestions:
				print("Import error diagnosis:")
				for suggestion in suggestions:
					print(f"  - {suggestion}")
			
			raise ImportError()

	def _load_with_ast_transform(self):
		"""Load module with AST transformation to preserve symbolic information."""
		# Use the full path stored during initialization
		module_path = self._fullPath
		
		# Read source code
		with open(module_path, 'r', encoding='utf-8') as f:
			source_code = f.read()
		
		# Transform AST
		tree = transform_ast(source_code, module_path, inject_branch_hooks=True)
		
		# Create module
		module = types.ModuleType(self._fileName)
		module.__file__ = module_path
		
		# Setup globals with helper functions
		globals_dict = module.__dict__
		setup_branch_hook_globals(globals_dict)
		
		# Add necessary imports to module globals
		# These will be used by the transformed code
		from .runtime_helpers import _se_int, _se_str, _se_range, unwrap, wrap_concrete_constant
		from .ast_transform import branch_hook
		
		globals_dict['_se_int'] = _se_int
		globals_dict['_se_str'] = _se_str
		globals_dict['_se_range'] = _se_range
		globals_dict['unwrap'] = unwrap
		globals_dict['wrap_concrete_constant'] = wrap_concrete_constant
		globals_dict['__branch_hook'] = branch_hook
		
		# Also add builtins
		globals_dict['__builtins__'] = __builtins__
		
		# Compile and execute transformed code
		code = compile_transformed_module(tree, module_path)
		exec(code, globals_dict)
		
		return module

	def _execute(self, **args):
		return self.app.__dict__[self._entryPoint](**args)

	def _toBag(self,l):
		bag = {}
		for i in l:
			if i in bag:
				bag[i] += 1
			else:
				bag[i] = 1
		return bag

	def _check(self, computed, expected, as_bag=True):
		b_c = self._toBag(computed)
		b_e = self._toBag(expected)
		if as_bag and b_c != b_e or not as_bag and set(computed) != set(expected):
			print("-------------------> %s test failed <---------------------" % self._fileName)
			print("Expected: %s, found: %s" % (b_e, b_c))
			return False
		else:
			print("%s test passed <---" % self._fileName)
			return True


class ScriptLoader(Loader):
    """Loader for script mode execution (top-level code)."""
    
    def __init__(self, filename, use_ast_transform=True):
        # Script mode doesn't have a specific entry function
        # Override the parent's initialization to use "__main__" as entry point
        self._is_script = True
        # We need to manually set up the parent's attributes
        self._fullPath = filename  # Store full path
        self._fileName = os.path.basename(filename)
        self._fileName = self._fileName[:-3]  # Remove .py extension
        self._entryPoint = "__main__"  # Script mode entry point
        self._use_ast_transform = use_ast_transform
        
        # Now call parent's _resetCallback directly
        self._resetCallback(True)
        
    
    def createInvocation(self):
        """Create invocation for script execution."""
        inv = FunctionInvocation(self._execute_script, self._resetCallback)
        
        # For script mode, we need to handle input() and sys.argv
        # These will be handled symbolically during execution
        
        # Define script inputs as symbolic parameters
        # We'll support:
        # 1. stdin_lines: list of strings for input() calls
        # 2. argv: list of command-line arguments
        # 3. Additional named parameters from input model
        
        # For now, create a basic symbolic input for script execution
        # This will be extended by input modeling
        inv.addArgumentConstructor("__stdin_lines", [], lambda n,v: v)
        inv.addArgumentConstructor("__argv", [""], lambda n,v: v)
        
        return inv
    
    def _execute_script(self, **args):
        """Execute script with given symbolic inputs."""
        # Get stdin lines and argv from arguments
        stdin_lines = args.get("__stdin_lines", [])
        argv = args.get("__argv", [""])
        
        # Simulate sys.argv
        import sys as real_sys
        original_argv = real_sys.argv
        real_sys.argv = [self._fileName + ".py"] + argv
        
        # Simulate input() calls
        import builtins as real_builtins
        original_input = real_builtins.input
        
        stdin_index = [0]  # Use list for mutable closure
        
        def symbolic_input(prompt=""):
            if stdin_index[0] < len(stdin_lines):
                value = stdin_lines[stdin_index[0]]
                stdin_index[0] += 1
                return value
            else:
                # No more input lines, return empty string
                return ""
        
        real_builtins.input = symbolic_input
        
        try:
            # Execute the script's top-level code
            # The module is already loaded in self.app
            if hasattr(self.app, '__main__'):
                # If there's a __main__ function, call it
                return self.app.__main__()
            else:
                # Otherwise, execute the module's top-level code
                # by calling a dummy function that runs the module
                exec(compile('', '<string>', 'exec'), self.app.__dict__)
                return None
        finally:
            # Restore original input and argv
            real_builtins.input = original_input
            real_sys.argv = original_argv


def loaderFactory(filename,entry, use_ast_transform=True, mode='function'):
    """
    Create a loader for the specified file.
    
    Args:
        filename: Path to Python file
        entry: Entry point function name (for function mode) or None (for script mode)
        use_ast_transform: Whether to apply AST transformation
        mode: Execution mode - 'function' or 'script'
    
    Returns:
        Loader instance or None if failed
    """
    if not os.path.isfile(filename) or not re.search(".py$",filename):
        print("Please provide a Python file to load")
        return None
    
    try: 
        dir = os.path.dirname(filename)
        sys.path = [ dir ] + sys.path
        
        # Debug: print loader creation info
        print(f"[DEBUG] loaderFactory: filename={filename}, entry={entry}, mode={mode}, use_ast_transform={use_ast_transform}")
        
        if mode == 'script':
            ret = ScriptLoader(filename, use_ast_transform=use_ast_transform)
            print(f"[DEBUG] Created ScriptLoader for {filename}")
        else:
            ret = Loader(filename,entry, use_ast_transform=use_ast_transform)
            print(f"[DEBUG] Created Loader for {filename} with entry {entry}")
        return ret
    except ImportError:
        sys.path = sys.path[1:]
        return None
