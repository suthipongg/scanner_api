from utils.env_loader import env
import logging
from controllers.elasticsearch_query import ES_access
from PIL import Image

if int(env["IS_ONNX_MODEL"]):
    logging.info('ONNX model is loading')
    from models.feature_extractor import FeatureExtractor_onnx
    feature_extractor = FeatureExtractor_onnx()
    logging.info('ONNX model is initialized')
elif int(env["IS_ORIGINAL_MODEL"]) or (not int(env["IS_ORIGINAL_MODEL"]) and not int(env["IS_ONNX_MODEL"])):
    logging.info('Original model is loading')
    from models.feature_extractor import FeatureExtractor
    feature_extractor = FeatureExtractor()
    logging.info('Original model is initialized')

if int(env["USE_ES"]):
    es_access = ES_access(env["ES_INDEX"], url=env["ES_URL"])
    logging.info('Elasticsearch is running')

# Define a function to process uploaded images and extract features
def extract_image(img):
    img = Image.open(img).convert('RGB')
    features = feature_extractor.extract(img)
    return features

def search_image(features):
    search_results = es_access.search_in_elasticsearch(features, tag_name_compare=["train_split", "train_val"], top_n=5, collapse=True)
    return search_results

def process_image(img):
    features = extract_image(img)
    search_results = search_image(features)
    return search_results