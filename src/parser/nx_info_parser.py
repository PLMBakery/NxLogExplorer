# src/parser/nx_info_parser.py

import re

def parse_nx_config_info(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Define the variables to capture
    variables_to_capture = [
        "NX_COMPATIBLE_BASE_RELEASE_VERSION",
        "NX_DEFAULT_SETTINGS_DIR",
        "NX_FULL_VERSION",
        "NX_HOTFIX_NUMBER",
        "NX_PRODUCT_NAME",
        "NX_RELEASE_VERSION",
        "NX_VERSION",
        "UGII_FULL_VERSION",
        "UGII_MAJOR_VERSION",
        "UGII_MINOR_VERSION",
        "UGII_PRODUCT_NAME",
        "UGII_SUBMINOR_VERSION",
        "UGII_VERSION"
    ]
    
    config_data = []
    for line in content.split('\n'):
        for variable in variables_to_capture:
            if variable in line:
                parts = line.split(maxsplit=2)
                if len(parts) >= 3:
                    location = parts[0].strip()[1:-1]  # Strip the square brackets
                    value = parts[2].strip()
                    config_data.append((variable, value, location))
    
    location_pattern = r'Variable locations:\n(.*?)\n\s*\*'
    location_match = re.search(location_pattern, content, re.DOTALL)
    
    location_mapping = {}
    if location_match:
        location_block = location_match.group(1).strip()
        location_lines = location_block.split('\n')
        for line in location_lines:
            if line.strip() and '[' in line and ']' in line:
                parts = line.split(']', 1)
                if len(parts) == 2:
                    location_id = parts[0].strip()[1:]  # Remove the leading '['
                    location_desc = parts[1].strip()
                    location_mapping[location_id] = location_desc
    
    for i in range(len(config_data)):
        variable, value, location_id = config_data[i]
        location_desc = location_mapping.get(location_id, "Unknown")
        config_data[i] = (variable, value, location_desc)
    
    return config_data
