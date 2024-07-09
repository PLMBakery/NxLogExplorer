# src/parser/tc_info_parser.py

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

def parse_tc_environment_data(file_path):
    import re

    with open(file_path, 'r') as file:
        content = file.read()
    
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
                if parsed_data and not line.strip() == '':
                    parsed_data[-1] = (parsed_data[-1][0], f"{parsed_data[-1][1]} {line.strip()}")
        
        return parsed_data
    
    return []
