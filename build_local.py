#!/bin/bash/python3
import subprocess

result = subprocess.run("pip install -e .", shell=True)
result.check_returncode()
