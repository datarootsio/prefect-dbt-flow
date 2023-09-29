import subprocess
from typing import List

def _run_cmd(cmd: List[str]) -> str:
    """
    Function to execute a command and return its output.
    Raises an exception if the command fails.
    """
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    try:
        stdout = result.stdout.decode("utf-8") if result.stdout else "No Output"
        stderr = result.stderr.decode("utf-8") if result.stderr else "No Output"
    except (UnicodeDecodeError, AttributeError):
        stdout = "No Output"
        stderr = "No Output"

    if result.returncode != 0:
        raise Exception(
            f"Error running cmd '{' '.join(cmd)}':\n\terr: {stderr}\n\tout: {stdout}"
            )

    return stdout