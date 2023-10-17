import onnxruntime as rt
from onnxruntime import InferenceSession
from transformers import ViTImageProcessor

from pathlib import Path
from PIL import Image
import sys, logging, os
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))
load_dotenv()
    
from script.tool import standardize_feature

env = os.environ

class FeatureExtractor:
    def __init__(self):
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
        output = standardize_feature(output)
        return output.tolist()


if __name__ == '__main__':
    fe = FeatureExtractor()
    img_path = Path("/home/music/Desktop/measure_model/data/image_net/n01491361_tiger_shark.JPEG")
    feature = fe.extract(img=Image.open(img_path))