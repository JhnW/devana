#!/bin/bash/python3
import subprocess

if __name__ == "__main__":
    result = subprocess.run("pylint --recursive=y ./src/devana", shell=True)
    result.check_returncode()
