from pathlib import Path
from PIL import Image
import logging
import torch
from utils.env_loader import env


class FeatureExtractor:
    def __init__(self):
        from models.func_models import pipeline_transformer, select_transformers_model
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
        from onnxruntime import InferenceSession
        from transformers import ViTImageProcessor
        import onnxruntime as rt
        
        logging.basicConfig(level = logging.INFO)
        self.device = rt.get_device()
        self.model = InferenceSession(env["FEATURE_EXTRACTOR_ONNX_MODEL_PATH"], providers=env["PROVIDER"].split(','))
        self.preprocessor = ViTImageProcessor.from_pretrained(env["FEATURE_EXTRACTOR_MODEL_FOLDER"])
        
        dummy_img = Image.new('RGB', size=(224, 224))
        dummy_img = self.preprocessor(dummy_img, return_tensors="np")
        _ = self.execute_model(dummy_img)
        logging.info('Initial FeatureExtractor Run Pass ...')
      
    def preprocess(self, img):
        img = img.convert("RGB")
        return self.preprocessor(images=img, return_tensors="np")

    def execute_model(self, img):
        return self.model.run(output_names=["last_hidden_state"], input_feed=dict(img))[0][:, 0]
    
    def extract(self, img):
        img = self.preprocess(img)
        feature = self.execute_model(img)
        output = feature.flatten()
        return output.tolist()
    

if __name__ == '__main__':
    feature_extractor = FeatureExtractor()
    img_path = Path("/home/music/Desktop/measure_model/data/image_net/n01491361_tiger_shark.JPEG")
    feature = feature_extractor.extract(img=Image.open(img_path))