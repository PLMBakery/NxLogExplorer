# src/parser/performance_metrics_parser.py

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
