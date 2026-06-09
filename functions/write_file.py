import os
from google.genai import types


def write_file(working_directory: str, file_path: str, content: str) -> str:
    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))

    if not abs_file_path.startswith(abs_working_dir):
        return f'Error: Cannot write "{file_path}" as it is outside the permitted working directory'

    if os.path.isdir(abs_file_path):
        return f'Error: Cannot write to "{file_path}" as it is a directory'

    dir_name = os.path.dirname(abs_file_path)
    try:
        os.makedirs(dir_name, exist_ok=True)
    except Exception as e:
        return f'Error: Failed to create directories for "{file_path}": {e}'

    try:
        with open(abs_file_path, "w") as f:
            f.write(content)
        return f'Successfully wrote {len(content)} characters to "{file_path}"'

    except Exception as e:
        return f'Error: Failed to write to "{file_path}": {e}'


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes content to a file within the working directory, creating the file (and any necessary parent directories) if it does not exist, or overwriting it if it does.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file to write, relative to the working directory",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Content to write to the file",
            ),
        },
        required=["file_path", "content"],
    ),
)
