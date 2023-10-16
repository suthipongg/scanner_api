# config.py
import os, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[0]


class ConFig(object):
    # feature extractor
    MODELS_PATH = ROOT / 'models'
    FEATURE_EXTRACTOR_MODEL_FOLDER = MODELS_PATH / Path('vit_gg_onnx')
    FEATURE_EXTRACTOR_PREPROCESSOR_PATH = FEATURE_EXTRACTOR_MODEL_FOLDER / Path('preprocessor.json')
    FEATURE_EXTRACTOR_ONNX_MODEL_PATH = FEATURE_EXTRACTOR_MODEL_FOLDER / Path('model.onnx')
    LAYER_OUTPUT = 'last_hidden_state'
    PROVIDER = ['CPUExecutionProvider'] # ['CUDAExecutionProvider', 'CPUExecutionProvider']
    IMAGE_SHAPE = (224, 224)
    
    # scanner onnx backend
    PATH_DIRECTORY_LOCAL_UAT = ROOT / 'uploads'
    # PATH_DIRECTORY_LOCAL = '/Users/nawaphongyoochum/Work-TNT/Cosmenet/insert2es/'
    # PATH_DIRECTORY_LOCAL_UAT = '/app/www/vhosts/cosmenet.in.th/httpdocs-chat-new/httpdocs-chat-web/'
    ALLOWED_EXTENSIONS = set(['.png', '.jpg', '.jpeg', '.gif'])
    
    HOST = "0.0.0.0"
    PORT = "9085"
    LOGGING = False
    DEBUG = True
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024

    IS_ONNX_MODEL = True
    # IS_TENSORFLOW_MODEL = False
    # SCORE_THRESHOLD = 0.9

if __name__ == "__main__":
    print(ROOT)