# src/parser/license_info_parser.py

def parse_license_info(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    license_info = []
    for line in lines:
        if ":" in line:
            parts = line.split(":")
            key = parts[0].strip()
            value = ":".join(parts[1:]).strip()
            if key in ["License File Sold To / Install", "License File Webkey Access Code", "License File Issuer", "Flexera Daemon Version", "Vendor Daemon Version"]:
                license_info.append((key, value))
    
    return license_info
