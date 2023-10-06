"""Code for executing command-line commands  capturing their output/error streams"""
import subprocess


def run(cmd_str: str):
    """
    Function that will execute a given command-line as a string.

    Args:
        cmd_str: A string containing the command to be executed.

    Returns:
        stdout: A standard output or standard error of the executed command.
    """
    result = subprocess.run(
        cmd_str, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )

    try:
        stdout = result.stdout.decode("utf-8") or "No Output"
    except Exception:
        stdout = "No Output"

    try:
        stderr = result.stderr.decode("utf-8") or "No Output"
    except Exception:
        stderr = "No Output"

    if result.returncode != 0:
        raise Exception(
            f"Error running cmd '{cmd_str}':\n\terr: {stderr}\n\tout: {stdout}"
        )

    return stdout
