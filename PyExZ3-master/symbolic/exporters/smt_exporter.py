import os

class SMTExporter:
    def __init__(self, output_dir):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
    
    def _convert_expr_to_smt(self, expr):
        """Convert PyExZ3 expression to SMT format"""
        if isinstance(expr, list):
            op = expr[0]
            args = expr[1:]
            
            if op == "=":
                return f"(= {self._convert_expr_to_smt(args[0])} {self._convert_expr_to_smt(args[1])})"
            elif op == "not":
                return f"(not {self._convert_expr_to_smt(args[0])})"
            elif op == "<":
                return f"(< {self._convert_expr_to_smt(args[0])} {self._convert_expr_to_smt(args[1])})"
            elif op == ">":
                return f"(> {self._convert_expr_to_smt(args[0])} {self._convert_expr_to_smt(args[1])})"
            elif op == "<=":
                return f"(<= {self._convert_expr_to_smt(args[0])} {self._convert_expr_to_smt(args[1])})"
            elif op == ">=":
                return f"(>= {self._convert_expr_to_smt(args[0])} {self._convert_expr_to_smt(args[1])})"
            elif op == "+":
                return f"(+ {self._convert_expr_to_smt(args[0])} {self._convert_expr_to_smt(args[1])})"
            elif op == "-":
                if len(args) == 1:
                    return f"(- {self._convert_expr_to_smt(args[0])})"
                else:
                    return f"(- {self._convert_expr_to_smt(args[0])} {self._convert_expr_to_smt(args[1])})"
            elif op == "*":
                return f"(* {self._convert_expr_to_smt(args[0])} {self._convert_expr_to_smt(args[1])})"
            elif op == "/":
                return f"(/ {self._convert_expr_to_smt(args[0])} {self._convert_expr_to_smt(args[1])})"
            elif op == "%":
                return f"(mod {self._convert_expr_to_smt(args[0])} {self._convert_expr_to_smt(args[1])})"
            elif op == "abs":
                return f"(abs {self._convert_expr_to_smt(args[0])})"
            elif op == "and":
                return f"(and {self._convert_expr_to_smt(args[0])} {self._convert_expr_to_smt(args[1])})"
            elif op == "or":
                return f"(or {self._convert_expr_to_smt(args[0])} {self._convert_expr_to_smt(args[1])})"
            elif op == "xor":
                return f"(xor {self._convert_expr_to_smt(args[0])} {self._convert_expr_to_smt(args[1])})"
            elif op == "str.<":
                return f"(str.< {self._convert_expr_to_smt(args[0])} {self._convert_expr_to_smt(args[1])})"
            elif op == "str.<=":
                return f"(str.<= {self._convert_expr_to_smt(args[0])} {self._convert_expr_to_smt(args[1])})"
            else:
                return f"; Unsupported operator: {op}"
        elif isinstance(expr, str):
            return f'"{expr}"'
        elif isinstance(expr, (int, float)):
            return str(expr)
        else:
            # Handle symbolic variables
            if hasattr(expr, 'name'):
                return expr.name
            return str(expr)
    
    def _convert_predicate_to_smt(self, predicate):
        """Convert predicate to SMT format"""
        sym_type = predicate.symtype
        result = predicate.result
        
        if hasattr(sym_type, 'expr') and sym_type.expr:
            smt_expr = self._convert_expr_to_smt(sym_type.expr)
        else:
            smt_expr = self._convert_expr_to_smt(sym_type)
        
        if not result:
            smt_expr = f"(not {smt_expr})"
        
        return smt_expr
    
    def export_path(self, solver, asserts, query):
        """Export path constraints to SMT2 format"""
        smt_content = "(set-logic ALL)\n"
        
        # Declare variables (default to Int for simplicity)
        declared_vars = set()
        var_declarations = []
        
        def declare_vars(expr):
            if isinstance(expr, list):
                for arg in expr[1:]:
                    declare_vars(arg)
            elif hasattr(expr, 'name') and expr.name not in declared_vars:
                var_declarations.append(f"(declare-const {expr.name} Int)\n")
                declared_vars.add(expr.name)
        
        # Declare variables from assertions
        for assert_pred in asserts:
            if hasattr(assert_pred, 'symtype'):
                declare_vars(assert_pred.symtype)
        
        if hasattr(query, 'symtype'):
            declare_vars(query.symtype)
        
        # Add variable declarations to smt_content
        for decl in var_declarations:
            smt_content += decl
        
        # Add assertions
        for assert_pred in asserts:
            smt_expr = self._convert_predicate_to_smt(assert_pred)
            smt_content += f"; {assert_pred}\n"
            smt_content += f"(assert {smt_expr})\n"
        
        # Add query
        if query:
            query_expr = self._convert_predicate_to_smt(query)
            smt_content += f"; Query: {query}\n"
            smt_content += f"(assert (not {query_expr}))\n"
        
        smt_content += "(check-sat)\n"
        smt_content += "(get-model)\n"
        
        with open(os.path.join(self.output_dir, "path.smt2"), "w") as f:
            f.write(smt_content)
    
    def export_frontier(self, solver, frontier):
        """Export frontier constraints to SMT2 format"""
        frontier_dir = os.path.join(self.output_dir, "frontier")
        os.makedirs(frontier_dir, exist_ok=True)
        
        for i, constraint in enumerate(frontier):
            asserts, query = constraint.getAssertsAndQuery()
            smt_content = "(set-logic ALL)\n"
            
            # Declare variables (default to Int for simplicity)
            declared_vars = set()
            var_declarations = []
            
            def declare_vars(expr):
                if isinstance(expr, list):
                    for arg in expr[1:]:
                        declare_vars(arg)
                elif hasattr(expr, 'name') and expr.name not in declared_vars:
                    var_declarations.append(f"(declare-const {expr.name} Int)\n")
                    declared_vars.add(expr.name)
            
            # Declare variables from assertions
            for assert_pred in asserts:
                if hasattr(assert_pred, 'symtype'):
                    declare_vars(assert_pred.symtype)
            
            if hasattr(query, 'symtype'):
                declare_vars(query.symtype)
            
            # Add variable declarations to smt_content
            for decl in var_declarations:
                smt_content += decl
            
            # Add assertions
            for assert_pred in asserts:
                smt_expr = self._convert_predicate_to_smt(assert_pred)
                smt_content += f"; {assert_pred}\n"
                smt_content += f"(assert {smt_expr})\n"
            
            # Add query
            if query:
                query_expr = self._convert_predicate_to_smt(query)
                smt_content += f"; Query: {query}\n"
                smt_content += f"(assert (not {query_expr}))\n"
            
            smt_content += "(check-sat)\n"
            smt_content += "(get-model)\n"
            
            with open(os.path.join(frontier_dir, f"frontier_{i}.smt2"), "w") as f:
                f.write(smt_content)
    
    def export_execution_summary(self, execution_data):
        """Export execution summary to SMT format"""
        smt_content = "(set-logic ALL)\n"
        
        # Add execution summary comments
        smt_content += f"; Execution Summary\n"
        smt_content += f"; Generated Inputs: {len(execution_data.get('generated_inputs', []))}\n"
        smt_content += f"; Return Values: {execution_data.get('return_values', [])}\n"
        smt_content += f"; Path Length: {len(execution_data.get('branch_trace', []))}\n"
        
        with open(os.path.join(self.output_dir, "execution_summary.smt2"), "w") as f:
            f.write(smt_content)
