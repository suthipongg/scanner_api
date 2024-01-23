from pathlib import Path
from PIL import Image
import logging, os
import torch
env = os.environ

# Original model
class FeatureExtractor:
    def __init__(self):
        logging.basicConfig(level = logging.INFO)
        # import transformers model and preprocessor
        from controllers.utils import pipeline_transformer, select_transformers_model
        from transformers import ViTImageProcessor, ViTModel

        # load model and preprocessor
        self.model, self.preprocessor = select_transformers_model(ViTModel, ViTImageProcessor, 
                                              pretrain=env['PRETRAIN_MODEL_PATH'])
        if int(env['LOAD_STATE_DICT']):
            self.model.load_state_dict(torch.load(env['MODELS_STATE_DICT_PATH'])['model_state_dict'])
        # create extractor pipeline
        self.extractor = pipeline_transformer(layer=env["FEATURE_EXTRACTOR_LAYER"], row=int(env["FEATURE_EXTRACTOR_ROW"]),
                                            device=env["DEVICE"])
        self.extractor.selct_model(self.model, self.preprocessor)
        # test dummy image
        dummy_img = Image.new('RGB', size=(224, 224))
        _ = self.extract(dummy_img)
        logging.info('Initial FeatureExtractor Run Pass ...')
        
    def extract(self, img):
        feature = self.extractor.extract(img)
        return feature.tolist()

# ONNX model
class FeatureExtractor_onnx:
    def __init__(self):
        logging.basicConfig(level = logging.INFO)
        # import onnx model and preprocessor
        from controllers.utils import pipeline_transformer_onnx, select_transformers_onnx_model
        from transformers import ViTImageProcessor
        
        # load model and preprocessor
        self.model, self.preprocessor = select_transformers_onnx_model(path=env['PRETRAIN_MODEL_PATH'], processor=ViTImageProcessor, 
                                                                       providers=env['PROVIDER'].split(','))
        # create extractor pipeline
        self.extractor = pipeline_transformer_onnx(layer=env["FEATURE_EXTRACTOR_LAYER"], row=int(env["FEATURE_EXTRACTOR_ROW"]))
        self.extractor.selct_model(self.model, self.preprocessor)
        # test dummy image
        dummy_img = Image.new('RGB', size=(224, 224))
        _ = self.extract(dummy_img)
        logging.info('Initial FeatureExtractor Run Pass ...')
    
    def extract(self, img):
        feature = self.extractor.extract(img)
        return feature.tolist()
    
# Choose model onnx or original
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

if __name__ == '__main__':
    feature_extractor = FeatureExtractor()
    img_path = Path("/home/music/Desktop/measure_model/data/image_net/n01491361_tiger_shark.JPEG")
    feature = feature_extractor.extract(img=Image.open(img_path))