# src/parser/installation_info_parser.py

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
