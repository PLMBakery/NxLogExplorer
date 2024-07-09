# src/parser/environment_variables_parser.py

def parse_environment_variables(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    lines = content.splitlines()
    env_vars = []
    prefixes = ["CLASSPATH", "IMAN", "JRE", "SPLM", "NX", "UGII", "UGS", "TC", "USER"]

    in_block = False
    for line in lines:
        if 'System Environment Variables' in line:
            in_block = True
            continue
        if in_block:
            if line.strip().startswith('**************'):
                break
            for prefix in prefixes:
                if line.strip().startswith(prefix):
                    key_value = line.split(None, 1)
                    if len(key_value) == 2:
                        env_vars.append((key_value[0].strip(), key_value[1].strip()))
                    break

    return env_vars
