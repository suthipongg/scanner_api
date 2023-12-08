import os
from dotenv import load_dotenv
load_dotenv()

env = os.environ

def str2list(str, sep=","):
    return [s.strip() for s in str.split(sep)]