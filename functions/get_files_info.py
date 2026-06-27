import os

def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        abs_path_working_directory = os.path.abspath(working_directory)
        target_path = os.path.normpath(os.path.join(abs_path_working_directory,directory))

        valid_target_path = os.path.commonpath([abs_path_working_directory,target_path]) == abs_path_working_directory
    except:
        raise Exception(f'Error: Cannot get files info.')
    

    if not valid_target_path:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    
    is_directory = os.path.isdir(directory)

    if not is_directory:
        return f'Error: "{directory}" is not a directory'
    
    return f'Success: "{directory}" is within the working directory'