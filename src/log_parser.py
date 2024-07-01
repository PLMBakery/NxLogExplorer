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

def parse_performance_metrics(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    performance_metrics = []
    for line in lines:
        if "Loaded and updated part" in line:
            performance_metrics.append(("Loaded Part", line.split("real")[1].strip()))
        if "Performed operation" in line:
            performance_metrics.append(("Performed Operation", line.split("real")[1].strip()))
    
    return performance_metrics
