import os

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