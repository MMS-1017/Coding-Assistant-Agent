import os
import subprocess
from google.genai import types


def run_python_file(working_directory: str, file_path: str, args: list[str] = []) -> str:
    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))

    if not abs_file_path.startswith(abs_working_dir):
        return f'Error: Cannot run "{file_path}" as it is outside the permitted working directory'

    if not os.path.isfile(abs_file_path):
        return f'Error: "{file_path}" does not exist or is not a file'

    if not abs_file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file'

    try:
        cmd = ["python", file_path] + list(args)
        result = subprocess.run(
            cmd,
            timeout=30,
            capture_output=True,
            text=True,
            cwd=abs_working_dir,
        )

        if result.stdout == "" and result.stderr == "":
            return "No output produced"

        if result.returncode != 0:
            return f"Error: Script exited with code {result.returncode}\nStderr:\n{result.stderr.strip()}"

        output = f"Stdout:\n{result.stdout.strip()}"
        if result.stderr.strip():
            output += f"\n\nStderr:\n{result.stderr.strip()}"
        return output

    except subprocess.TimeoutExpired:
        return f'Error: "{file_path}" timed out after 30 seconds'
    except Exception as e:
        return f'Error: Failed to run "{file_path}": {e}'


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs a Python file within the working directory and returns its output. Accepts optional CLI arguments.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the Python file to run, relative to the working directory",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="Optional list of CLI arguments to pass to the script",
            ),
        },
        required=["file_path"],
    ),
)
