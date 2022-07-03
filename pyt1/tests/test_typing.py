import subprocess

def examine_shell_cmd(cmd):
    return not subprocess.call(cmd.split())

# def test_typing():
#     assert examine_shell_cmd('pyt1/env310/Scripts/python.exe -m pyright pyt1/epure --project pyt1')