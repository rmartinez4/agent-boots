import os

schema_get_files_info = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "Lists files in a specified directory relative to the working directory, providing file size and directory status",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory path to list files from, relative to the working directory (default is the working directory itself)",
                },
            },
        },
    },
}

def get_files_info(working_directory: str, directory: str = ".") -> str:
    """Guardrails for the LLM: we never want it to be able to perform 
    any work outside the working_directory that we give it."""
    if directory == ".":
        message = 'Result for current directory:\n'
    else:
        message = f'Result for "{directory}" directory:\n'

    try:
        abs_work_dir = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(abs_work_dir, directory))

        valid_target_dir = os.path.commonpath([abs_work_dir, target_dir]) == abs_work_dir
        if not valid_target_dir:
            message += f'\tError: Cannot list "{directory}" as it is outside the permitted working directory\n'
        elif not os.path.isdir(target_dir):
            message += f'\tError: "{directory}" is not a directory\n'
        else:
            for item in os.listdir(target_dir):
                item_path = os.path.join(target_dir, item)
                message += f"  - {item}: file_size={os.path.getsize(item_path)}, is_dir={os.path.isdir(item_path)}\n"

        return message

    except Exception as e: 
        return message + f'\tError: {e}\n'
