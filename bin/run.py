import os, stat
file_name = os.path.join(os.getcwd(), 'bin/run.sh')
os.chmod(file_name, 0o755)
os.system(f'bash {file_name} start')
