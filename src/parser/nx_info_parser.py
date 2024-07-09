# src/parser/nx_info_parser.py

def parse_nx_info(file_path):
    nx_info = []
    with open(file_path, 'r') as file:
        lines = file.readlines()

    for line in lines:
        if "NX specific info" in line:  # Placeholder for actual condition
            parts = line.split(":")
            key = parts[0].strip()
            value = ":".join(parts[1:]).strip()
            nx_info.append((key, value))

    return nx_info

def parse_nx_config_info(file_path):
    import re

    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    pattern = r'\*\s+Locked NX Configuration Variables\s+\*\n(.*?)\n\*{14}\s+System Environment Variables\s+\*{14}'
    match = re.search(pattern, content, re.DOTALL)
    
    if match:
        data_block = match.group(1)
        
        data_lines = data_block.strip().split('\n')
        parsed_data = []

        for line in data_lines:
            if line.strip() and not line.startswith("Variable locations:"):
                parts = line.split(maxsplit=2)
                if len(parts) == 3:
                    key = parts[1].strip()
                    value = parts[2].strip()
                    parsed_data.append((key, value))
        
        return parsed_data

    return [("No NX Configuration Variables found", "")]
