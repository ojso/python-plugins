import os
import shutil


def remove(dir, dirname):
    for root, dirs, files in os.walk(dir):
        if "venv" in root or "git" in root:
            continue
        for dir in dirs:
            if dir == dirname:
                rm_path = os.path.join(root, dir)
                print(f"Removing {rm_path}")
                shutil.rmtree(rm_path)


def remove_pycache(dir="."):
    remove(dir, "__pycache__")


def remove_ipynb_checkpoints(dir="."):
    remove(dir, ".ipynb_checkpoints")


def find_empty_dirs(dir="."):
    for root, dirs, files in os.walk(dir):
        if "venv" in root or "git" in root:
            continue
        for dir in dirs:
            dir_path = os.path.join(root, dir)
            if not os.listdir(dir_path):
                print(f"Empty dir: {dir_path}")
