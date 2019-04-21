#!/usr/bin/env python3

# Packages the code into a standalone application
# Is a python script since I dont want to write a separate shell script and bash script
# https://stackoverflow.com/questions/37888581/pyinstaller-ui-files-filenotfounderror-errno-2-no-such-file-or-directory

import os
import subprocess

filepath = os.path.dirname(os.path.abspath(__file__)) + '/ses/gui.py'
name = 'SES-Rollout'

# Prepare spec file
cmd = []
cmd.append('pyi-makespec')
cmd.append('--noconsole')
cmd.append('--onefile')
#cmd.append('--onedir')
cmd.extend(['--name', name])
cmd.extend(['--add-data', 'qt/ses.ui'+os.pathsep+'qt/'])
cmd.append(filepath)

print(cmd)
subprocess.run(cmd)

# Run pyinstaller
cmd = []
cmd.append('pyinstaller')
cmd.append(name+'.spec')

#cmd.append('--debug')
# cmd.extend(['--paths', ''])

print(cmd)
subprocess.run(cmd)
