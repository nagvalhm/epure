import subprocess

def exec_shell_cmd(cmd):
    return subprocess.call(cmd.split())
    # return subprocess.call(cmd.split(), shell=True)

exec_shell_cmd("pyt1//env310//Scripts//pip.exe install --upgrade pip")
exec_shell_cmd("pyt1//env310//Scripts//pip.exe install -r pyt1/requirements.txt")
exec_shell_cmd("pre-commit install")
# exec_shell_cmd("pre-commit uninstall")