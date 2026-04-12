# Copyright: see copyright.txt

import os
import sys
# 首先设置sys.path，确保后续导入能正常工作
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import logging
import traceback
import argparse
import time
from pathlib import Path

from symbolic.loader import *
from symbolic.explore import ExplorationEngine

print("PyExZ3 (Python Exploration with Z3) - Enhanced Symbolic Execution Tool")

# Parse command line arguments
parser = argparse.ArgumentParser(description='Enhanced symbolic execution for student code analysis')
parser.add_argument('file', help='Path to Python file to analyze')
parser.add_argument('-l', '--log', dest='logfile', help='Save log output to a file', default='')
parser.add_argument('-s', '--start', dest='entry', help='Specify entry point function name', default='')
parser.add_argument('-g', '--graph', dest='dot_graph', action='store_true', help='Generate a DOT graph of execution tree')
parser.add_argument('-m', '--max-iters', dest='max_iters', type=int, help='Run specified number of iterations', default=0)
parser.add_argument('--cvc', dest='cvc', action='store_true', help='Use the CVC SMT solver instead of Z3', default=False)
parser.add_argument('--z3', dest='cvc', action='store_false', help='Use the Z3 SMT solver')

# New options for enhanced functionality (Week 1)
parser.add_argument('--mode', choices=['function', 'script'], default='function',
                    help='Execution mode: function (default) or script')
parser.add_argument('--dump-constraints', action='store_true', 
                    help='Dump path constraints to output directory')
parser.add_argument('--dump-trace', action='store_true',
                    help='Dump execution trace to output directory')
parser.add_argument('--dump-semantics', action='store_true',
                    help='Dump semantic tags to output directory')
parser.add_argument('--output-dir', default='outputs',
                    help='Output directory for results (default: outputs/)')
parser.add_argument('--input-spec', type=str, default='',
                    help='JSON specification for input modeling (inline JSON or file path)')
parser.add_argument('--input-model', type=str, default='',
                    help='Path to JSON file containing input model specification')

# Week 2: Export functionality
parser.add_argument('--export-json', action='store_true',
                    help='Export execution results to JSON format')
parser.add_argument('--export-smt', action='store_true',
                    help='Export constraints to SMTLIB2 format')
parser.add_argument('--export-path', action='store_true',
                    help='Export path constraints (implies --export-json and/or --export-smt)')
parser.add_argument('--export-frontier', action='store_true',
                    help='Export frontier constraints (implies --export-json and/or --export-smt)')
parser.add_argument('--export-trace', action='store_true',
                    help='Export execution trace (implies --export-json)')
parser.add_argument('--export-corpus', action='store_true',
                    help='Export clustering-ready corpus in JSONL format (Week 4 feature)')
parser.add_argument('--ast-transform', action='store_true', default=True,
                    help='Enable AST transformation to preserve symbolic information (default: True)')
parser.add_argument('--no-ast-transform', dest='ast_transform', action='store_false',
                    help='Disable AST transformation')

args = parser.parse_args()

# Week 4: Enable default exports if no export arguments are provided
# Check if any export arguments were provided
any_export_args = (args.export_json or args.export_smt or args.export_path or 
                   args.export_frontier or args.export_trace or args.export_corpus)

if not any_export_args:
    # Enable default exports: path constraints, frontier, trace, and corpus (Week 4 feature)
    args.export_path = True
    args.export_frontier = True
    args.export_trace = True
    args.export_corpus = True

# Set up output directory structure
run_id = f"run_{int(time.time() * 1000)}"
output_dir = Path(args.output_dir) / run_id
output_dir.mkdir(parents=True, exist_ok=True)

# Set up logging
if args.logfile:
    logging.basicConfig(filename=args.logfile, level=logging.DEBUG, 
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
else:
    logging.basicConfig(level=logging.WARNING)

solver = "cvc" if args.cvc else "z3"

if not os.path.exists(args.file):
    print(f"Error: File {args.file} does not exist")
    sys.exit(1)

filename = os.path.abspath(args.file)

# Get the object describing the application
app = loaderFactory(filename, args.entry, use_ast_transform=args.ast_transform, mode=args.mode)
if app == None:
    sys.exit(1)

print(f"Exploring {app.getFile()}.{app.getEntry()} in {args.mode} mode")
print(f"Output directory: {output_dir}")
print(f"AST transformation: {'enabled' if args.ast_transform else 'disabled'}")

# Load input model if specified
input_model = None
if args.input_spec or args.input_model:
    try:
        from symbolic.input_model import load_input_model, register_input_model, InputModel, InputField, InputType
        import json
        from pathlib import Path
        
        program_id = f"{app.getFile()}_{app.getEntry()}"
        
        if args.input_model:
            # Load from file
            model_path = Path(args.input_model)
            if model_path.exists():
                input_model = InputModel.from_json_file(model_path)
                register_input_model(program_id, input_model)
                print(f"[INFO] Loaded input model from {args.input_model}")
            else:
                print(f"[WARNING] Input model file not found: {args.input_model}")
        elif args.input_spec:
            # Try to parse as inline JSON
            try:
                spec_data = json.loads(args.input_spec)
                input_model = InputModel.from_dict(spec_data)
                register_input_model(program_id, input_model)
                print(f"[INFO] Loaded input model from inline specification")
            except json.JSONDecodeError:
                # Might be a file path
                spec_path = Path(args.input_spec)
                if spec_path.exists():
                    input_model = InputModel.from_json_file(spec_path)
                    register_input_model(program_id, input_model)
                    print(f"[INFO] Loaded input model from {args.input_spec}")
                else:
                    print(f"[WARNING] Input spec not valid JSON and file not found: {args.input_spec}")
        
        if input_model:
            print(f"[INFO] Input model loaded with {len(input_model.fields)} fields")
    except Exception as e:
        print(f"[WARNING] Failed to load input model: {e}")

result = None
try:
    engine = ExplorationEngine(app.createInvocation(), solver=solver)
    generatedInputs, returnVals, path = engine.explore(args.max_iters)
    
    # TODO: Week 1 - Add constraint dumping functionality
    if args.dump_constraints:
        print(f"[INFO] Constraint dumping not yet implemented (Week 1)")
    
    # TODO: Week 1 - Add trace dumping functionality  
    if args.dump_trace:
        print(f"[INFO] Trace dumping not yet implemented (Week 1)")
    
    # TODO: Week 1 - Add semantics dumping functionality
    if args.dump_semantics:
        print(f"[INFO] Semantic tags dumping not yet implemented (Week 1)")
    
    # Week 2 & Week 4: Export functionality
    export_performed = False
    export_json = False
    export_smt = False
    export_corpus = args.export_corpus
    if args.export_json or args.export_smt or args.export_path or args.export_frontier or args.export_trace or export_corpus:
        # Import exporters
        from symbolic.exporters.json_exporter import JSONExporter
        from symbolic.exporters.smt_exporter import SMTExporter
        from symbolic.trace import get_trace_recorder
        global_trace_recorder = get_trace_recorder()
        
        # Determine what to export
        export_json = args.export_json or args.export_path or args.export_frontier or args.export_trace or export_corpus
        export_smt = args.export_smt or args.export_path or args.export_frontier
        
        # Week 4: Import corpus exporter if needed
        if export_corpus:
            try:
                from symbolic.exporters.corpus_exporter import CorpusExporter
            except ImportError as e:
                print(f"[WARNING] Failed to import corpus exporter: {e}")
                print(f"[WARNING] Corpus export will be disabled")
                export_corpus = False
        
        if export_json:
            json_exporter = JSONExporter(output_dir)
            print(f"[INFO] JSON exporter initialized for {output_dir}")
        
        if export_smt:
            smt_exporter = SMTExporter(output_dir)
            print(f"[INFO] SMT exporter initialized for {output_dir}")
        
        # Export path constraints
        if args.export_path and hasattr(path, 'getConstraints'):
            constraints = path.getConstraints()
            for i, constraint in enumerate(constraints):
                if export_json:
                    try:
                        # Need to get inputs and return values for this constraint
                        inputs = generatedInputs[i] if i < len(generatedInputs) else {}
                        retval = returnVals[i] if i < len(returnVals) else None
                        json_file = json_exporter.export_path_constraint(
                            constraint, inputs, retval, None, i
                        )
                        print(f"[INFO] Exported path constraint {i} to JSON: {json_file}")
                        
                        # Week 4: Export to corpus format if requested
                        if export_corpus:
                            try:
                                # Read the JSON data back for corpus export
                                import json as json_module
                                with open(json_file, 'r', encoding='utf-8') as f:
                                    path_data = json_module.load(f)
                                
                                # Create corpus exporter and export
                                corpus_exporter = CorpusExporter(output_dir)
                                program_id = f"{app.getFile()}_{app.getEntry()}"
                                submission_id = f"{program_id}_submission"
                                corpus_exporter.set_program_info(program_id, submission_id)
                                
                                corpus_file = corpus_exporter.export_corpus_record(
                                    path_data, i
                                )
                                print(f"[INFO] Exported path constraint {i} to corpus: {corpus_file}")
                            except Exception as corpus_e:
                                print(f"[WARNING] Failed to export path constraint {i} to corpus: {corpus_e}")
                    except Exception as e:
                        print(f"[WARNING] Failed to export path constraint {i} to JSON: {e}")
                
                if export_smt:
                    try:
                        smt_file = smt_exporter.export_path_constraint_smt2(constraint, i)
                        print(f"[INFO] Exported path constraint {i} to SMT2: {smt_file}")
                    except Exception as e:
                        print(f"[WARNING] Failed to export path constraint {i} to SMT2: {e}")
        
        # Export frontier constraints
        if args.export_frontier and hasattr(engine, 'getFrontierConstraints'):
            frontier_constraints = engine.getFrontierConstraints()
            for i, frontier in enumerate(frontier_constraints):
                parent_constraint = frontier.get('parent') if isinstance(frontier, dict) else None
                if export_json and parent_constraint:
                    try:
                        json_files = json_exporter.export_frontier_constraint(
                            [frontier], parent_constraint, i
                        )
                        for json_file in json_files:
                            print(f"[INFO] Exported frontier constraint {i} to JSON: {json_file}")
                    except Exception as e:
                        print(f"[WARNING] Failed to export frontier constraint {i} to JSON: {e}")
                
                if export_smt and parent_constraint:
                    try:
                        smt_file = smt_exporter.export_frontier_constraint_smt2(
                            frontier, parent_constraint, i, i
                        )
                        print(f"[INFO] Exported frontier constraint {i} to SMT2: {smt_file}")
                    except Exception as e:
                        print(f"[WARNING] Failed to export frontier constraint {i} to SMT2: {e}")
        
        # Export trace
        if args.export_trace:
            try:
                traces = global_trace_recorder.traces
                if traces:
                    json_file = json_exporter.export_trace_summary(
                        traces, len(generatedInputs)
                    )
                    print(f"[INFO] Exported trace summary to JSON: {json_file}")
                else:
                    print(f"[INFO] No traces recorded for export")
            except Exception as e:
                print(f"[WARNING] Failed to export trace: {e}")
        
        export_performed = True
        print("[INFO] Export operations completed")
    
    # check the result
    result = app.executionComplete(returnVals)

    # output DOT graph
    if args.dot_graph:
        dot_file = output_dir / f"{app.getFile()}.dot"
        with open(dot_file, "w") as file:
            file.write(path.toDot())
        print(f"DOT graph saved to: {dot_file}")
    
    # Save basic execution info with export status
    exec_info = {
        "mode": args.mode,
        "function": f"{app.getFile()}.{app.getEntry()}",
        "iterations": len(generatedInputs),
        "run_id": run_id,
        "timestamp": time.time(),
        "ast_transform_enabled": args.ast_transform,
        "export_performed": export_performed,
        "export_options": {
            "json": export_json,
            "smt": export_smt,
            "path": args.export_path,
            "frontier": args.export_frontier,
            "trace": args.export_trace,
            "corpus": export_corpus
        }
    }
    
    import json
    info_file = output_dir / "execution_info.json"
    with open(info_file, "w") as f:
        json.dump(exec_info, f, indent=2)
    
    print(f"Execution info saved to: {info_file}")

except ImportError as e:
    # createInvocation can raise this
    logging.error(e)
    sys.exit(1)

if result == None or result == True:
    print("Exploration completed successfully")
    sys.exit(0)
else:
    print("Exploration failed")
    sys.exit(1)