#!/bin/bash/python3
from devana.syntax_abstraction.organizers.sourcemodule import SourceModule, ModuleFilter
from pyvis.network import Network
import os
import tarfile
import urllib.request
from pathlib import Path
import psutil
import argparse


def download_and_extract_code():
    code_archive_filename = "dlib.tar.gz"
    download_url = r"https://github.com/davisking/dlib/archive/refs/tags/v19.22.tar.gz"
    if Path(code_archive_filename).exists():
        return
    urllib.request.urlretrieve(download_url, code_archive_filename)
    tar = tarfile.open(f"./{code_archive_filename}", "r:gz")
    tar.extractall(path=".")
    tar.close()


def create_dependency_graph(api: SourceModule):
    network = Network(height='1080px', width='1920px')
    for i, f in enumerate(api.files):
        network.add_node(i + 1, label=f.name, physics=False)
    for i, f in enumerate(api.files):
        for inc in f.includes:
            name = os.path.basename(inc.path)
            for j, s in enumerate(api.files):
                if name == os.path.basename(s.path):
                    network.add_edge(i + 1, j + 1, physics=False)
    network.options.edges.arrows = "to"
    network.show("dependency.html")


def create_module(path=r"./dlib-19.22/dlib", pattern=r"/.h"):
    api_filter = ModuleFilter()
    api_filter.allowed_filter = [pattern]
    source = SourceModule("API", path)
    return source


def check_system():
    total_mem_gb = psutil.virtual_memory().total/1024**3
    if total_mem_gb < 15:
        print("WARNING")
        print("It is recommended to have at least 16 GB of RAM in order to process large modules.")
        print("If you don't have enough memory, choose a small subfolder to parse.")
        input("Press any key to continue...")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--parse_path", required=False, default=r"./dlib-19.22/dlib")
    parser.add_argument('--no_download', action='store_true', required=False)
    args = parser.parse_args()
    check_system()
    if not args.no_download:
        download_and_extract_code()
    module = create_module(args.parse_path)
    create_dependency_graph(module)
