"""Code for executing command-line commands  capturing their output/error streams"""
import subprocess
import logging

#Log config
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
log_file_path = 'logs.log'
file_handler = logging.FileHandler(log_file_path)
console_handler = logging.StreamHandler()
log_format = logging.Formatter('%(asctime)s %(name)s %(levelname)s: %(message)s')
file_handler.setFormatter(log_format)
console_handler.setFormatter(log_format)
logger.addHandler(file_handler)
logger.addHandler(console_handler)


def run(cmd_str: str):
    """
    Function that will execute a given command-line as a string.

    :param cmd_str: A string containing the command to be executed.
    :return: standard output or standard error of the executed command.
    """
    logger.debug(f"Executing command: {cmd_str}")

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
        logger.error(f"Error running cmd '{cmd_str}':\n\terr: {stderr}\n\tout: {stdout}")
        raise Exception(
            f"Error running cmd '{cmd_str}':\n\terr: {stderr}\n\tout: {stdout}"
        )
    
    logger.debug(f"Command executed successfully: {cmd_str}")

    return stdout
