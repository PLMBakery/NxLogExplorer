import os

def print_directory_structure(root_dir, padding=""):
    print(padding[:-1] + "+--" + os.path.basename(root_dir) + "/")
    padding = padding + "   "
    files = []
    dirs = []
    for item in os.listdir(root_dir):
        if os.path.isdir(os.path.join(root_dir, item)):
            dirs.append(item)
        else:
            files.append(item)
    for dir in dirs:
        print_directory_structure(os.path.join(root_dir, dir), padding + "|  ")
    for file in files:
        print(padding + "+--" + file)

root_directory = "G:\\My Drive\\Gitea\\NxLogExplorer"
print_directory_structure(root_directory)
