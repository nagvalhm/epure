import subprocess

subprocess.call(["pip", "install", "--upgrade", "pip"], shell=True)
subprocess.call(["pip", "install", "-r", "pyt/requirements.txt"], shell=True)
subprocess.call(["pre-commit", "install"], shell=True)
# subprocess.call(["pre-commit", "uninstall"], shell=True)