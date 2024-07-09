# src/parser/log_parser.py

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from parser.file_reader import read_log_file

def parse_log_file(file_path):
    content = read_log_file(file_path)
    if content:
        # Hier Logik zur Analyse der Logdatei
        return f"Analyseergebnisse der Datei {file_path}"
    else:
        return f"Datei {file_path} konnte nicht gefunden werden."

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
        elif tc_section and not line.startswith("Teamcenter Integration") and line.strip() == "":
            break  # End the section when a blank line is encountered after capturing "Teamcenter Integration" lines
        if tc_section:
            parts = line.split(":")
            key = parts[0].strip()
            value = ":".join(parts[1:]).strip() if len(parts) > 1 else ""
            tc_integration_info.append((key, value))

    return tc_integration_info

def parse_tc_aw_variables(file_path):
    variables = []

    with open(file_path, 'r') as file:
        lines = file.readlines()

    for line in lines:
        if line.startswith("TC_") or line.startswith("AW_"):
            parts = line.split("=")
            key = parts[0].strip()
            value = "=".join(parts[1:]).strip() if len(parts) > 1 else ""
            variables.append((key, value))

    return variables

# Ab Zeile 151 in log_parser.py hinzufügen
def parse_tc_integration_info(file_path):
    tc_integration_info = []

    with open(file_path, 'r') as file:
        lines = file.readlines()

    tc_section = False
    for line in lines:
        if "Teamcenter Integration" in line:
            tc_section = True
        elif tc_section and not line.startswith("Teamcenter Integration") and line.strip() == "":
            break  # End the section when a blank line is encountered after capturing "Teamcenter Integration" lines
        if tc_section:
            parts = line.split(":")
            key = parts[0].strip()
            value = ":".join(parts[1:]).strip() if len(parts) > 1 else ""
            tc_integration_info.append((key, value))

    return tc_integration_info

import re

def parse_tc_environment_data(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    
    # Define a more precise pattern to capture the relevant block
    pattern = r'={48}\nTeamcenter Integration Server system log : .+?\n={48}\n(.+?)(?=={48}\n|Teamcenter Integration: In four-tier mode|Teamcenter Integration: Attempting to initialize use of FMS|Attempting to load module libfccclient|Successfully loaded dynamic module|UGOPEN_UTILS:: process_manifest_directories|Command line: .+?\n|$)'
    match = re.search(pattern, content, re.DOTALL)
    
    if match:
        data_block = match.group(1)
        data_lines = data_block.strip().split('\n')
        parsed_data = []
        current_section = None

        for line in data_lines:
            if line.startswith('---'):
                current_section = line.strip('- ')
                continue
            if ':' in line:
                key, value = map(str.strip, line.split(':', 1))
                if current_section:
                    key = f"{current_section} - {key}"
                parsed_data.append((key, value))
            else:
                # Handle lines without colons (likely part of a previous key's value)
                if parsed_data and not line.strip() == '':
                    parsed_data[-1] = (parsed_data[-1][0], f"{parsed_data[-1][1]} {line.strip()}")
        
        return parsed_data
    
    return []

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

import re

def parse_nx_config_info(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Debug-Ausgabe des gesamten Dateiinhalts
    print("File Content:")
    print(content[:1000])  # nur die ersten 1000 Zeichen ausgeben
    
    # Define a pattern to capture the NX Configuration Variables block
    pattern = r'\*\s+Locked NX Configuration Variables\s+\*\n(.*?)\n\*{14}\s+System Environment Variables\s+\*{14}'
    match = re.search(pattern, content, re.DOTALL)
    
    if match:
        data_block = match.group(1)
        
        # Debug-Ausgabe des gefundenen Blocks
        print("Found Block:")
        print(data_block)
        
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

    # Debug-Ausgabe, wenn kein Block gefunden wurde
    print("No NX Configuration Variables block found")
    return [("No NX Configuration Variables found", "")]
