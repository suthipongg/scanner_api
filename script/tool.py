from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def standardize_feature(arr):
    return (arr-arr.mean())/arr.std()