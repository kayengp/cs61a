# test.py

import sys
import importlib.util

def test_function(module_name, function_name, num_args, *args):
    # Import the module dynamically
    spec = importlib.util.spec_from_file_location(module_name, module_name)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    # Get the function object
    function = getattr(module, function_name)

    # Split args into chunks based on num_args
    chunked_args = []
    for i in range(0, len(args), num_args):
        chunk = args[i:i+num_args]
        evaluated_chunk = []
        for arg in chunk:
            # If arg could be evaluate as lambda function defined in module, add lambda function in arg list
            evaluated_arg = eval_lambda(arg, module)
            if evaluated_arg is not None:
                evaluated_chunk.append(evaluated_arg)
            else:
                evaluated_chunk.append(arg)
        chunked_args.append(evaluated_chunk)

    # Call the function with the provided arguments
    for i, chunk in enumerate(chunked_args):
        print(f"INFO: Calling function '{function_name}' with arguments {chunk} (call {i+1})")
        try:
            result = function(*chunk)
            print(result)
            print()  # Print an empty line after each function call
        except Exception as e:
            print(f"ERROR: Exception occurred while calling function '{function_name}' with arguments {chunk} (call {i+1}): {e}", file=sys.stderr)


def eval_lambda(term_name, module):
    """Evaluate a lambda function string defined in the module."""
    try:
        return eval(term_name, {**vars(module), '__builtins__': None})
    except Exception as e:
        # logging.error(f"Error evaluating lambda function '{term_name}': {e}")
        return None


if __name__ == "__main__":
    if len(sys.argv) < 5:
        print("Usage: python3 test.py <module_name> <function_name> <num_args_for_each_call> <arg1> <arg2> ...")
        sys.exit(1)

    module_name = sys.argv[1]
    function_name = sys.argv[2]
    num_args = int(sys.argv[3])
    args = sys.argv[4:]

    test_function(module_name, function_name, num_args, *args)
