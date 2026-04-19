import os
import sys
import tempfile
import unittest


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pyexz3
from symbolic.exporters.json_exporter import JSONExporter
from symbolic.normalizer import ConstraintNormalizer
from symbolic.predicate import Predicate
from symbolic.runtime_helpers import get_next_symbolic_input, init_symbolic_inputs
from symbolic.symbolic_types import SymbolicFloat, SymbolicInteger, SymbolicStr
from symbolic.z3_wrap import Z3Wrapper


class TestRecentRegressions(unittest.TestCase):
    def test_analyze_input_calls_prefers_string_for_raw_input(self):
        repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        script_path = os.path.join(repo_root, "test", "input_mixed.py")
        result = pyexz3.analyze_input_calls(script_path)
        self.assertEqual([item["type"] for item in result], ["str", "int", "float"])

    def test_runtime_helpers_build_symbolic_inputs(self):
        init_symbolic_inputs(
            [
                ("name", None, "str"),
                ("age", None, "int"),
                ("height", None, "float"),
            ]
        )

        first = get_next_symbolic_input()
        second = get_next_symbolic_input()
        third = get_next_symbolic_input()

        self.assertIsInstance(first, SymbolicStr)
        self.assertIsInstance(second, SymbolicInteger)
        self.assertIsInstance(third, SymbolicFloat)
        self.assertEqual(first.name, "name")
        self.assertEqual(second.name, "age")
        self.assertEqual(third.name, "height")

    def test_json_exporter_uses_symbolic_variables_for_templates(self):
        a = SymbolicInteger("a", -2)
        b = SymbolicInteger("b", 2)
        predicate = Predicate(abs(a) == b, True)
        normalizer = ConstraintNormalizer()
        raw_predicates, normalized_predicates = normalizer.normalize_path([predicate])

        with tempfile.TemporaryDirectory() as temp_dir:
            exporter = JSONExporter(temp_dir)
            templates = exporter._build_constraint_templates(
                [predicate], raw_predicates, normalized_predicates
            )

        self.assertEqual(templates[0]["operation"], "==")
        self.assertEqual(templates[0]["variables"], ["a", "b"])

    def test_normalizer_uses_symbolic_variables_for_string_predicates(self):
        text = SymbolicStr("input_0", "A")
        predicate = Predicate(len(text) > 0, True)
        normalizer = ConstraintNormalizer()

        _, normalized_predicates = normalizer.normalize_path([predicate])

        self.assertEqual(normalized_predicates, ["(< 0 (str.len ARG0))"])

    def test_float_solver_respects_false_branch_history(self):
        value = SymbolicFloat("x", 0.0)
        first_branch = Predicate(value > 0, False)
        second_branch = Predicate(value < 0, False)
        solver = Z3Wrapper()

        model = solver.findCounterexample([first_branch], second_branch)

        self.assertIsNotNone(model)
        self.assertLess(model["x"], 0.0)


if __name__ == "__main__":
    unittest.main()
