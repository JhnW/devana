#!/bin/bash/python3
import subprocess

if __name__ == "__main__":
    result = subprocess.run("pip install -e .", shell=True)
    result.check_returncode()
