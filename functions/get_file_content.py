import os
from config import MAX_CHARS

def get_file_content(working_directory: str, file_path: str) -> str:

    message = ""

    try:
        abs_work_dir = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(abs_work_dir, file_path))

        valid_target_file = os.path.commonpath([abs_work_dir, target_file]) == abs_work_dir

        if not valid_target_file:
            message += f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        elif not os.path.isfile(target_file):
            message += f'Error: File not found or is not a regular file: "{file_path}"'
        else: 
            with open(target_file, "r") as f:
                message += f.read(MAX_CHARS)

                # After reading the first MAX_CHARS...
                if f.read(1):
                    message += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'

        return message
    
    except Exception as e: 
        return message + f'\tError: {e}\n'

