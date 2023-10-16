import onnxruntime as rt
from onnxruntime import InferenceSession
from transformers import ViTImageProcessor

from pathlib import Path
from PIL import Image
import sys, logging

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from config import ConFig
from script.tool import standardize_feature

class FeatureExtractor:
    def __init__(self):
        logging.basicConfig(level = logging.INFO)
        self.device = rt.get_device()
        self.model = InferenceSession(ConFig.FEATURE_EXTRACTOR_ONNX_MODEL_PATH, providers=ConFig.PROVIDER)
        self.preprocessor = ViTImageProcessor.from_pretrained(ConFig.FEATURE_EXTRACTOR_MODEL_FOLDER)
        
        dummy_img = Image.new('RGB', size=ConFig.IMAGE_SHAPE)
        dummy_img = self.preprocessor(dummy_img, return_tensors="np")
        _ = self.model.run(output_names=[ConFig.LAYER_OUTPUT], input_feed=dict(dummy_img))
        logging.info('Initial FeatureExtractor Run Pass ...')
      
    def preprocess(self, img):
        img = img.convert("RGB")
        return self.preprocessor(images=img, return_tensors="np")

    def extract(self, img):
        img = self.preprocess(img)
        feature = self.model.run(output_names=[ConFig.LAYER_OUTPUT], input_feed=dict(img))[0][:, 0]
        output = feature.flatten().reshape(1, -1)
        output = standardize_feature(output)
        return output


if __name__ == '__main__':
    fe = FeatureExtractor()
    img_path = Path("/home/music/Desktop/measure_model/data/image_net/n01491361_tiger_shark.JPEG")
    feature = fe.extract(img=Image.open(img_path))