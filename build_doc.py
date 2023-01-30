#!/bin/bash/python3
import subprocess
from subprocess import PIPE
import argparse
from pathlib import Path
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--no_test_coverage', action='store_true', required=False)
    parser.add_argument('--no_api', action='store_true', required=False)
    parser.add_argument('--no_changelog', action='store_true', required=False)
    parser.add_argument('--verbose', action='store_true', required=False)
    args = parser.parse_args()

    verbose = args.verbose

    if not args.no_test_coverage:
        print("Generate coverage report")
        print("-----------------")
        result = subprocess.run('coverage run  --source=devana -m unittest discover -v -s tests -q', shell=True)
        result.check_returncode()
        if verbose:
            print(result.stdout)
        result = subprocess.run('coverage html -d docs/test_coverage', shell=True)
        result.check_returncode()
        if verbose:
            print(result.stdout)

    if not args.no_api:
        print("Generate api doc")
        print("-----------------")
        result = subprocess.run('sphinx-apidoc ./src/devana -o ./doc_src/api -t ./doc_src/_templates -f', shell=True)
        result.check_returncode()
        if verbose:
            print(result.stdout)

    if not args.no_changelog:
        print("Generate changelog")
        print("-----------------")
        result = subprocess.run('gitchangelog', stdout=PIPE, shell=True)
        result.check_returncode()
        changelog_path = "./doc_src/changelog_list.rst"
        with open(changelog_path, "wt") as f:
            f.write(result.stdout.decode("utf-8"))

    print("Render documentation")
    print("-----------------")
    result = subprocess.run('sphinx-build doc_src ./docs -E', shell=True)
    result.check_returncode()
    if verbose:
        print(result.stdout)

    print("Finished")
