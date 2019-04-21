#!/usr/bin/env python3

# Packages the code into a standalone application
# Is a python script since I dont want to write a separate shell script and bash script

import os
import subprocess

filepath = os.path.dirname(os.path.abspath(__file__)) + '/ses/gui.py'

cmd = []
cmd.append('pyinstaller')
cmd.append('--onefile')
cmd.extend(['--name', 'SES-Rollout'])
#cmd.append('--debug')
# cmd.extend(['--paths', ''])
cmd.append(filepath)

print(cmd)

subprocess.run(cmd)
