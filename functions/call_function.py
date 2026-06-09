from google.genai import types
from functions.get_files_info import get_files_info
from functions.get_files_content import get_file_content
from functions.write_file import write_file
from functions.run_python_file import run_python_file

working_directory = "calculator"


def call_function(function_call: types.FunctionCall, verbose: bool = False) -> types.Content:
    if verbose:
        print(f" → {function_call.name}({function_call.args})")
    else:
        print(f" → Calling: {function_call.name}")

    args = function_call.args or {}

    function_map = {
        "get_file_content": lambda: get_file_content(working_directory, **args),
        "get_files_info": lambda: get_files_info(working_directory, **args),
        "write_file": lambda: write_file(working_directory, **args),
        "run_python_file": lambda: run_python_file(working_directory, **args),
    }

    if function_call.name not in function_map:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call.name,
                    response={"error": f"Unknown function: {function_call.name}"},
                )
            ],
        )

    content = function_map[function_call.name]()

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_call.name,
                response={"content": content},
            )
        ],
    )
