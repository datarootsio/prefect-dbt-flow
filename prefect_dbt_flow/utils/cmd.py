import subprocess


def run(cmd_str: str):
    # TODO: get logs continuously
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
