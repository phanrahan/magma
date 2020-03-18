"""
Expected to be run from repo root
"""
import shutil
import os


def copy_golds(dir_path):
    for f in os.listdir(os.path.join(dir_path, "gold")):
        try:
            shutil.copy(
                os.path.join(dir_path, "build", f),
                os.path.join(dir_path, "gold", f)
            )
        except FileNotFoundError as e:
            # corresponding build has different name or extra file
            pass


copy_golds("tests")


for name in os.listdir("tests"):
    if not os.path.isdir(os.path.join("tests", name)):
        continue
    if "gold" in os.listdir(os.path.join("tests", name)):
        copy_golds(os.path.join("tests", name))
