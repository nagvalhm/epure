# type: ignore
import subprocess

def exec_shell_cmd(cmd):
    return subprocess.call(cmd.split())
    # return subprocess.call(cmd.split(), shell=True)

exec_shell_cmd("pyt//env39//Scripts//pip.exe install --upgrade pip")
exec_shell_cmd("pyt//env39//Scripts//pip.exe install -r pyt/requirements.txt")
exec_shell_cmd("pre-commit install")
# exec_shell_cmd("pre-commit uninstall")