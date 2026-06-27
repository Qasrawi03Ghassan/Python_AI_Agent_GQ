import os
from config import CHARACTERS_READ_LIMIT

def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        abs_path_working_directory = os.path.abspath(working_directory)
        target_path = os.path.normpath(os.path.join(abs_path_working_directory,file_path))

        valid_target_path = os.path.commonpath([abs_path_working_directory,target_path]) == abs_path_working_directory
    

        if not valid_target_path:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        
        is_file = os.path.isfile(target_path)

        if not is_file:
            return f'Error: File not found or is not a regular file: "{file_path}"'
        
        with open(target_path,"r") as f:
            file_contents_string = f.read(CHARACTERS_READ_LIMIT)

            if f.read(1):
                file_contents_string += f'[...File "{file_path}" truncated at {CHARACTERS_READ_LIMIT} characters!]'
        
        
        return file_contents_string        

    except:
        return f'Error: Cannot get files info due to library functions error.'
    
    