from pathlib import Path
from PIL import Image
import logging, os
import torch
env = os.environ

class FeatureExtractor:
    def __init__(self):
        logging.basicConfig(level = logging.INFO)
        from controllers.utils import pipeline_transformer, select_transformers_model
        from transformers import ViTImageProcessor, ViTModel

        self.model, self.preprocessor = select_transformers_model(ViTModel, ViTImageProcessor, 
                                              pretrain=env['PRETRAIN_MODEL_PATH'])
        if int(env['LOAD_STATE_DICT']):
            self.model.load_state_dict(torch.load(env['MODELS_STATE_DICT_PATH'])['model_state_dict'])
            
        self.extractor = pipeline_transformer(layer=env["FEATURE_EXTRACTOR_LAYER"], row=int(env["FEATURE_EXTRACTOR_ROW"]),
                                            device=env["DEVICE"])
        self.extractor.selct_model(self.model, self.preprocessor)
        
    def extract(self, img):
        feature = self.extractor.extract(img)
        return feature.tolist()


class FeatureExtractor_onnx:
    def __init__(self):
        logging.basicConfig(level = logging.INFO)
        from controllers.utils import pipeline_transformer_onnx, select_transformers_onnx_model
        from transformers import ViTImageProcessor
        
        self.model, self.preprocessor = select_transformers_onnx_model(path=env['FEATURE_EXTRACTOR_ONNX_MODEL_PATH'], processor=ViTImageProcessor, 
                                                                       providers=env['PROVIDER'].split(','))
        
        self.extractor = pipeline_transformer_onnx(layer=env["FEATURE_EXTRACTOR_LAYER"], row=int(env["FEATURE_EXTRACTOR_ROW"]))
        self.extractor.selct_model(self.model, self.preprocessor)
        
        dummy_img = Image.new('RGB', size=(224, 224))
        _ = self.extract(dummy_img)
        logging.info('Initial FeatureExtractor Run Pass ...')
    
    def extract(self, img):
        feature = self.extractor.extract(img)
        return feature.tolist()
    

if int(env["IS_ONNX_MODEL"]):
    logging.info('ONNX model is loading')
    feature_extractor = FeatureExtractor_onnx()
    logging.info('ONNX model is initialized')
elif int(env["IS_ORIGINAL_MODEL"]):
    logging.info('Original model is loading')
    feature_extractor = FeatureExtractor()
    logging.info('Original model is initialized')
else:
    logging.info('No model is loaded')
    feature_extractor = None

# Define a function to process uploaded images and extract features
def extract_image(img):
    img = Image.open(img).convert('RGB')
    features = feature_extractor.extract(img)
    return features

if __name__ == '__main__':
    feature_extractor = FeatureExtractor()
    img_path = Path("/home/music/Desktop/measure_model/data/image_net/n01491361_tiger_shark.JPEG")
    feature = feature_extractor.extract(img=Image.open(img_path))