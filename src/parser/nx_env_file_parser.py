# src/parser/nx_env_file_parser.py

def parse_nx_env_files(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    lines = content.splitlines()
    env_files = []

    for line in lines:
        if "Using environment file" in line:
            parts = line.split("Using environment file")
            if len(parts) == 2:
                env_files.append(("ENV File", parts[1].strip()))
        elif "Using" in line and "file from" in line:
            parts = line.split("Using")
            if len(parts) == 2:
                file_name = parts[1].split("file from")[0].strip().split('_env.dat')[0]
                env_files.append((file_name, parts[1].strip()))

    return env_files
