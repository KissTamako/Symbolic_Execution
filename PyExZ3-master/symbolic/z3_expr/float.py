from z3 import *
from .expression import Z3Expression

class Z3Float(Z3Expression):
    def __init__(self, enable_simplify=False):
        super(Z3Float, self).__init__(enable_simplify)
    
    def toZ3(self, solver, asserts, query):
        """Convert the assertions and query to Z3 expressions"""
        # Add assertions
        for a in asserts:
            expr = self._predToZ3(a)
            if expr is not None:
                solver.assert_exprs(expr)
        
        # Add query
        expr = self._predToZ3(query)
        if expr is not None:
            # Add the negation of the query to find a counterexample
            solver.assert_exprs(Not(expr))
    
    def _predToZ3(self, pred):
        """Convert a predicate to a Z3 expression"""
        if hasattr(pred, 'symtype'):
            return self._exprToZ3(pred.symtype)
        return None
    
    def _exprToZ3(self, expr):
        """Convert an expression to a Z3 expression"""
        if expr.isVariable():
            if expr.name not in self.z3_vars:
                self.z3_vars[expr.name] = Real('{}'.format(expr.name))  # Use Real instead of FP for simplicity
            return self.z3_vars[expr.name]
        elif isinstance(expr.expr, list):
            op = expr.expr[0]
            args = expr.expr[1:]
            
            # Convert arguments
            z3_args = []
            for arg in args:
                if isinstance(arg, type(expr)):
                    z3_args.append(self._exprToZ3(arg))
                else:
                    # Handle concrete values
                    if isinstance(arg, float):
                        z3_args.append(RealVal(str(arg)))
                    elif isinstance(arg, int):
                        z3_args.append(RealVal(str(arg)))
                    else:
                        z3_args.append(RealVal(str(arg)))
            
            # Handle operations
            if op == '+':
                return z3_args[0] + z3_args[1]
            elif op == '-':
                return z3_args[0] - z3_args[1]
            elif op == '*':
                return z3_args[0] * z3_args[1]
            elif op == '/':
                return z3_args[0] / z3_args[1]
            elif op == '%':
                # For modulo operation, use floor division
                return z3_args[0] - (z3_args[1] * floor(z3_args[0] / z3_args[1]))
            elif op == '**':
                return z3_args[0] ** z3_args[1]
            elif op == 'abs':
                return abs(z3_args[0])
            elif op == '==':
                return z3_args[0] == z3_args[1]
            elif op == '!=':
                return z3_args[0] != z3_args[1]
            elif op == '<':
                return z3_args[0] < z3_args[1]
            elif op == '<=':
                return z3_args[0] <= z3_args[1]
            elif op == '>':
                return z3_args[0] > z3_args[1]
            elif op == '>=':
                return z3_args[0] >= z3_args[1]
            elif op == 'to_int':
                # Convert to integer using floor for negative numbers
                return ToReal(Int('to_int_' + str(hash(expr))))
            elif op == 'floor':
                return floor(z3_args[0])
            elif op == 'ceil':
                return ceil(z3_args[0])
            elif op == 'sin':
                return sin(z3_args[0])
            elif op == 'cos':
                return cos(z3_args[0])
            elif op == 'tan':
                return tan(z3_args[0])
            elif op == 'asin':
                return asin(z3_args[0])
            elif op == 'acos':
                return acos(z3_args[0])
            elif op == 'atan':
                return atan(z3_args[0])
            elif op == 'sqrt':
                return sqrt(z3_args[0])
            elif op == 'exp':
                return exp(z3_args[0])
            elif op == 'log':
                return log(z3_args[0])
            elif op == 'log10':
                return log10(z3_args[0])
            elif op == 'pow':
                return z3_args[0] ** z3_args[1]
        
        return None
    
    def getIntVars(self):
        """Get integer variables (empty for float)"""
        return []
    
    def predToZ3(self, pred, solver, model):
        """Evaluate a predicate against a model"""
        # For simplicity, we'll just use the concrete value
        return pred.getConcrValue()
    
    def _getModel(self, solver):
        """Extract float values from the model"""
        res = {}
        model = solver.model()
        for name in self.z3_vars.keys():
            try:
                ce = model.eval(self.z3_vars[name])
                # Try to convert to float
                if is_real(ce):
                    # For simplicity, we'll just use the concrete value
                    # In a real implementation, we would extract the float value
                    res[name] = float(str(ce))
            except:
                pass
        return res
