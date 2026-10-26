import os

def write_file(working_directory: str, file_path: str, content: str) -> str:
    message = ""
    try:
        abs_work_dir = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(abs_work_dir, file_path))

        valid_target_file = os.path.commonpath([abs_work_dir, target_file]) == abs_work_dir
        if not valid_target_file:
            message += f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        elif os.path.isdir(target_file):
            message += f'Error: Cannot write to "{file_path}" as it is a directory'

        else:
            os.makedirs(os.path.dirname(target_file), exist_ok=True)
            with open(target_file, "w") as f:
                f.write(content)
            message += f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

        return message

    except Exception as e: 
        return message + f'Error: {e}\n'
