import os
from google.genai import types 

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)


def get_files_info(working_directory: str, directory: str = ".") -> str:
    print(f'Result for current directory:') if directory == '.' else print(f'Result for \'{directory}\' directory:')

    try:
        abs_path_working_directory = os.path.abspath(working_directory)
        target_path = os.path.normpath(os.path.join(abs_path_working_directory,directory))

        valid_target_path = os.path.commonpath([abs_path_working_directory,target_path]) == abs_path_working_directory
    except:
        return f'Error: Cannot get files info due to library functions error.'
    

    if not valid_target_path:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    
    is_directory = os.path.isdir(target_path)

    if not is_directory:
        return f'Error: "{directory}" is not a directory'
    
    target_path_files_names = os.listdir(target_path)
    files_strings = []

    for item in target_path_files_names:
        files_strings.append(f' - {item}: file_size={os.path.getsize(f'{target_path}/{item}')} bytes, is_dir={os.path.isdir(f'{target_path}/{item}')}')
        
    directory_string = '\n'.join(files_strings)


    return directory_string