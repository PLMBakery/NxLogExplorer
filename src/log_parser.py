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

def parse_installation_info(file_path):
    install_info = {
        "Kits Installed on Disk": [],
        "NX Version": "",
        "Disk Mark Mode": "",
        "Customizations": [],
        "Dynamic Modules": [],
        "Feature Toggles": []
    }

    with open(file_path, 'r') as file:
        lines = file.readlines()
        kits_section = False
        customizations_section = False
        modules_section = False
        toggles_section = False

        for i, line in enumerate(lines):
            line = line.strip()
            if line.startswith("Kits installed on disk"):
                kits_section = True
                continue
            elif line.startswith("Main"):
                kits_section = False
                install_info["NX Version"] = lines[i + 1].strip()
                install_info["Disk Mark Mode"] = lines[i + 2].strip()
            elif line.startswith("Processing customer default values"):
                install_info["Customizations"].append(line)
            elif line.startswith("Successfully loaded dynamic module"):
                install_info["Dynamic Modules"].append(line)
            elif line.startswith("Feature Toggle"):
                toggles_section = True
            elif line.startswith("************** Toggle's Information **************"):
                toggles_section = False
            elif toggles_section and "status:" in line:
                install_info["Feature Toggles"].append(line)
            elif kits_section:
                install_info["Kits Installed on Disk"].append(line)

    # Join list items into a single string with line breaks
    install_info["Kits Installed on Disk"] = "\n".join(install_info["Kits Installed on Disk"])
    install_info["Customizations"] = "\n".join(install_info["Customizations"])
    install_info["Dynamic Modules"] = "\n".join(install_info["Dynamic Modules"])
    install_info["Feature Toggles"] = "\n".join(install_info["Feature Toggles"])

    return list(install_info.items())

def parse_tc_info(file_path):
    # Dummy implementation for TC Info
    return [("TC Attribute 1", "Value 1"), ("TC Attribute 2", "Value 2")]

def parse_tc_integration_info(file_path):
    tc_integration_info = []

    with open(file_path, 'r') as file:
        lines = file.readlines()

    tc_section = False
    for line in lines:
        if "Teamcenter Integration" in line:
            tc_section = True
        if tc_section:
            if line.strip() == "":
                continue  # Skip empty lines
            tc_integration_info.append(line.strip())

    # Grouping the parsed information
    parsed_info = [("Teamcenter Integration", "\n".join(tc_integration_info))]
    return parsed_info
