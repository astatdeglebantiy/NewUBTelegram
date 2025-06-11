import subprocess


def _function(_vars_, command: str):
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return {
        "stdout": result.stdout,
        "stderr": result.stderr,
        "returncode": result.returncode
    }
