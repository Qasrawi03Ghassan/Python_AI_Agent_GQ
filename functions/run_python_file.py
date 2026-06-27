import os
import subprocess

def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    
    try:
        abs_path_working_directory = os.path.abspath(working_directory)
        target_path = os.path.normpath(os.path.join(abs_path_working_directory,file_path))

        valid_target_path = os.path.commonpath([abs_path_working_directory,target_path]) == abs_path_working_directory

        if not valid_target_path:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        
        if not os.path.isfile(target_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        
        if not file_path.endswith("py"):
            return f'Error: "{file_path}" is not a Python file'
        
        command = ["python",target_path]

        if args:
            command.extend(args)

        result_process = subprocess.run(command,cwd=abs_path_working_directory,capture_output=True,text=True,timeout=30)
        output = ''

        if result_process.returncode != 0:
            output = f'Process exited with code {result_process.returncode}'
        elif result_process.stdout is None and result_process.stdin is None:
            output = f'No output produced'
        else:
            output = f'STDOUT: {result_process.stdout}\nSTDERR: {result_process.stderr}'
        
        return output
    
    except Exception as e:
        return f"Error: executing Python file: {e}"