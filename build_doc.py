#!/bin/bash/python3
import subprocess
import argparse

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
    result = subprocess.run('coverage run  --source=devana -m unittest discover -v -s tests/parser/unit -q', shell=True)
    result.check_returncode()
    if verbose:
        print(result.stdout)
    result = subprocess.run('coverage html -d doc/test_coverage', shell=True)
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
    result = subprocess.run('gitchangelog', shell=True)
    result.check_returncode()
    f = open("./doc/changelog_list.rst", "wt")
    f.write(str(result.stdout))
    f.close()

print("Render documentation")
print("-----------------")
result = subprocess.run('sphinx-build doc ./doc -E', shell=True)
result.check_returncode()
if verbose:
    print(result.stdout)

print("Finished")
