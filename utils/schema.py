import os
from urllib.parse import quote

def encode_url_filename(url_path):
    dir_name = os.path.dirname(url_path)
    file_name = os.path.basename(url_path)
    return os.path.join(dir_name, quote(file_name))