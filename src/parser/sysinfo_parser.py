# src/parser/sysinfo_parser.py

def parse_system_info(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    system_info = []
    for line in lines:
        if ":" in line:
            parts = line.split(":")
            key = parts[0].strip()
            value = ":".join(parts[1:]).strip()
            if key in ["Date", "Information listing created by", "Current work part", "Node name", "Machine type", "OS", "# Processors", "Memory", "Free Swap", "Process ID"]:
                system_info.append((key, value))
    
    return system_info
