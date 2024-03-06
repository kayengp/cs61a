# test.py

import sys
import importlib.util
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

def test_function(module_name, function_name, num_args, *args):
    # Import the module dynamically
    spec = importlib.util.spec_from_file_location(module_name, module_name)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    # Get the function object
    function = getattr(module, function_name)

    # Split args into chunks based on num_args
    chunked_args = [args[i:i+num_args] for i in range(0, len(args), num_args)]

    # Call the function with the provided arguments
    for i, chunk in enumerate(chunked_args):
        logging.info(f"Calling function '{function_name}' with arguments {chunk} (call {i+1})")
        try:
            result = function(*chunk)
            print(result)
            print()  # Print an empty line after each function call
        except Exception as e:
            logging.error(f"Exception occurred while calling function '{function_name}' with arguments {chunk} (call {i+1}): {e}")

if __name__ == "__main__":
    if len(sys.argv) < 5:
        print("Usage: python3 test.py <module_name> <function_name> <num_args_for_each_call> <arg1> <arg2> ...")
        sys.exit(1)

    module_name = sys.argv[1]
    function_name = sys.argv[2]
    num_args = int(sys.argv[3])
    args = [int(arg) for arg in sys.argv[4:]]

    test_function(module_name, function_name, num_args, *args)
