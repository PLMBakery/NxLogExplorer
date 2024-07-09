# src/parser/file_reader.py

def read_log_file(file_path):
    """
    Liest eine Logdatei aus und gibt ihren Inhalt zurück.
    """
    try:
        with open(file_path, 'r') as file:
            content = file.read()
        return content
    except FileNotFoundError:
        return None
