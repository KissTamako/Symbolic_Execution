# Copyright: see copyright.txt

import re


class ConstraintNormalizer:
    """Normalize symbolic path constraints into a stable textual form."""

    _FALLBACK_EXCLUDE = {
        "abs",
        "and",
        "or",
        "not",
        "True",
        "False",
        "str",
        "len",
        "int",
        "real",
        "to",
        "floor",
        "ceil",
        "sin",
        "cos",
        "tan",
        "asin",
        "acos",
        "atan",
        "sqrt",
        "exp",
        "log",
        "log10",
    }

    def __init__(self):
        self.var_name_map = {}
        self.var_counter = 0
        self.var_map_built = False

    def normalize_path(self, path_predicates):
        """Return raw and normalized strings for a list of predicates."""
        self._build_var_map(path_predicates)

        raw_predicates_str = []
        normalized_predicates_str = []
        for predicate in path_predicates:
            raw_predicates_str.append(predicate.get_symbolic_expr())
            normalized_predicates_str.append(self._normalize_predicate(predicate))

        return raw_predicates_str, normalized_predicates_str

    def _build_var_map(self, path_predicates):
        """Build a stable variable renaming map using predicate variable metadata."""
        self.var_name_map = {}
        self.var_counter = 0
        self.var_map_built = True

        all_vars = []
        for predicate in path_predicates:
            if hasattr(predicate, "getVars"):
                for var_name in predicate.getVars():
                    if var_name not in all_vars:
                        all_vars.append(var_name)
                continue

            expr_str = predicate.get_symbolic_expr()
            matches = re.findall(r"\b([a-zA-Z_][a-zA-Z0-9_]*)\b", expr_str)
            for var_name in matches:
                if var_name in self._FALLBACK_EXCLUDE:
                    continue
                if var_name not in all_vars:
                    all_vars.append(var_name)

        for var_name in all_vars:
            self.var_name_map[var_name] = f"ARG{self.var_counter}"
            self.var_counter += 1

    def _normalize_predicate(self, predicate):
        symbolic_expr = predicate.get_symbolic_expr()
        expr_tree = self._parse_expr_str(symbolic_expr)
        normalized_tree = self.normalize_expression(expr_tree)

        if not predicate.result:
            normalized_tree = ["not", normalized_tree]

        return self._expr_tree_to_str(normalized_tree)

    def _parse_expr_str(self, expr_str):
        """Parse a simple S-expression string into a nested list tree."""
        expr_str = expr_str.strip()

        if "(" not in expr_str:
            try:
                return int(expr_str)
            except ValueError:
                try:
                    return float(expr_str)
                except ValueError:
                    return expr_str

        if expr_str.startswith("(") and expr_str.endswith(")"):
            balance = 0
            for index, char in enumerate(expr_str):
                if char == "(":
                    balance += 1
                elif char == ")":
                    balance -= 1
                    if balance == 0 and index == len(expr_str) - 1:
                        expr_str = expr_str[1:-1].strip()
                        break

        parts = []
        current_part = []
        depth = 0
        for char in expr_str:
            if char == "(":
                depth += 1
                current_part.append(char)
            elif char == ")":
                depth -= 1
                current_part.append(char)
            elif char == " " and depth == 0:
                if current_part:
                    parts.append("".join(current_part))
                    current_part = []
            else:
                current_part.append(char)

        if current_part:
            parts.append("".join(current_part))

        if not parts:
            return expr_str

        op = parts[0]
        args = [self._parse_expr_str(arg) for arg in parts[1:]]
        return [op] + args

    def _expr_tree_to_str(self, expr_tree):
        if isinstance(expr_tree, list):
            op = expr_tree[0]
            args = expr_tree[1:]
            return f"({op} {' '.join(self._expr_tree_to_str(arg) for arg in args)})"
        return str(expr_tree)

    def _rename_variable(self, var_name):
        if var_name in self.var_name_map:
            return self.var_name_map[var_name]

        if self.var_map_built:
            return var_name

        normalized_name = f"ARG{self.var_counter}"
        self.var_name_map[var_name] = normalized_name
        self.var_counter += 1
        return normalized_name

    def normalize_expression(self, expr):
        if not isinstance(expr, list):
            if isinstance(expr, str):
                return self._rename_variable(expr)
            return expr

        op = expr[0]
        normalized_args = [self.normalize_expression(arg) for arg in expr[1:]]

        if op in ["+", "*"]:
            return self._normalize_commutative_arithmetic(op, normalized_args)
        if op in ["and", "or"]:
            normalized_args.sort(key=lambda item: str(item))
            return [op] + normalized_args
        if op in ["<", ">", "<=", ">=", "==", "!="]:
            return self._normalize_comparison(op, normalized_args)
        if op == "not":
            return [op, normalized_args[0]]
        if op == "abs":
            return [op, normalized_args[0]]
        return [op] + normalized_args

    def _normalize_commutative_arithmetic(self, op, args):
        constants = []
        variables = []
        for arg in args:
            if isinstance(arg, (int, float)):
                constants.append(arg)
            else:
                variables.append(arg)

        if constants:
            merged_constant = sum(constants) if op == "+" else self._product(constants)
            if variables:
                variables.insert(0, merged_constant)
            else:
                return merged_constant

        variables.sort(key=lambda item: str(item))
        return [op] + variables

    def _product(self, constants):
        result = 1
        for constant in constants:
            result *= constant
        return result

    def _merge_constants(self, op, args):
        constants = []
        variables = []
        for arg in args:
            if isinstance(arg, (int, float)):
                constants.append(arg)
            else:
                variables.append(arg)

        if not constants:
            return [op] + variables

        if op == "+":
            merged_constant = sum(constants)
        elif op == "*":
            merged_constant = self._product(constants)
        else:
            return [op] + args

        if variables:
            return [op, merged_constant] + variables
        return merged_constant

    def _normalize_comparison(self, op, args):
        if len(args) != 2:
            return [op] + args

        left, right = args
        if op == ">":
            return ["<", right, left]
        if op == ">=":
            return ["<=", right, left]
        return [op, left, right]

    def normalize_constraint_str(self, constraint_str):
        expr_tree = self._parse_expr_str(constraint_str)
        normalized_tree = self.normalize_expression(expr_tree)
        return self._expr_tree_to_str(normalized_tree)
