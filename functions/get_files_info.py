import os
from google.genai import types


def get_files_info(working_directory: str, directory: str = ".") -> str:
    abs_working_dir = os.path.abspath(working_directory)
    abs_directory = os.path.abspath(os.path.join(working_directory, directory))

    if not abs_directory.startswith(abs_working_dir):
        return f'Error: "{directory}" is outside the permitted working directory'

    try:
        contents = os.listdir(abs_directory)
    except FileNotFoundError:
        return f'Error: Directory "{directory}" does not exist'

    if not contents:
        return f'Directory "{directory}" is empty'

    lines = []
    for item in sorted(contents):
        item_path = os.path.join(abs_directory, item)
        is_dir = os.path.isdir(item_path)
        size = os.path.getsize(item_path)
        kind = "dir" if is_dir else "file"
        lines.append(f"  {item} [{kind}, {size} bytes]")

    return "\n".join(lines)


schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files and subdirectories in a specified directory relative to the working directory, showing file size and type.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list, relative to the working directory. Defaults to the working directory itself.",
            ),
        },
    ),
)
