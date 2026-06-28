import os
from google.genai import types 

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description=f'Writes content to a file specified within directory, takes the file path and content as parameters',
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to get file from, relative to the working directory (default is the working directory itself)",
            ),
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file in the directory)",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="content to write to the file)",
            ),
        },
        required=["file_path"]
    ),
)

def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        abs_path_working_directory = os.path.abspath(working_directory)
        target_path = os.path.normpath(os.path.join(abs_path_working_directory,file_path))

        valid_target_path = os.path.commonpath([abs_path_working_directory,target_path]) == abs_path_working_directory
    

        if not valid_target_path:
            return f'Error: Cannot write "{file_path}" as it is outside the permitted working directory'
        
        is_dir = os.path.isdir(target_path)

        if is_dir:
            return f'Error: Cannot write to "{file_path}" as it is a directory'
        
        os.makedirs(os.path.dirname(target_path), exist_ok=True)

        with open(target_path, "w") as f:
            f.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except:
        return f'Error: Cannot write files info due to library functions error.'