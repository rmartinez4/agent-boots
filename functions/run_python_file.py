import os
import subprocess

def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
        abs_work_dir = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(abs_work_dir, file_path))

        valid_target_file = os.path.commonpath([abs_work_dir, target_file]) == abs_work_dir
        if not valid_target_file:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(target_file):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        if not target_file.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", target_file]

        if args is not None:
            command.extend(args)

        message = ""

        process = subprocess.run(command, cwd=working_directory, capture_output=True, text=True, timeout=30)

        if process.returncode != 0:
            message += f"Process exited with code {process.returncode}\n"

        if process.stdout is None and process.stderr is None:
            message += "No output produced\n"
        else:
            message += f"STDOUT:{process.stdout}STDERR:{process.stderr}"

        return message

    except Exception as e: 
        return f'Error: executing Python file: {e}'
