import time
from pathlib import Path

from PIL import Image
import numpy as np

def to_unit_len(vector):
    return vector / np.linalg.norm(vector)

def standardize_feature(arr):
    return (arr-arr.mean())/arr.std()

def select_timm_model(model, num_classes=0, pretrain=True):
    from timm.models import create_model
    import timm
    
    model = create_model(model, num_classes=num_classes, pretrained=pretrain)
    data_config = timm.data.resolve_model_data_config(model)
    processor = timm.data.create_transform(**data_config, is_training=False)
    return model, processor

# pipeline for timm library
class pipeline_timm:
    def __init__(self, device='cuda:0'):
        self.device = device
    
    def selct_model(self, model, processor):
        self.model = model
        self.processor = processor
        self.model.eval().to(self.device)
    
    def process_model(self, img):
        inputs = self.processor(img).to(self.device).unsqueeze(0)
        outputs = self.model(inputs)
        return outputs
        
    def extract(self, img):
        ### return specific layer
        outputs = self.process_model(img)
        outputs.flatten().unsqueeze(0)
        outputs = standardize_feature(outputs).to('cpu').detach().numpy()
        return to_unit_len(outputs)
    
    def report_test(self):
        img = Image.new('RGB', (224, 224))
        start_time_torch = time.time()
        outputs = self.process_model(img)
        delta_time_torch = time.time() - start_time_torch
        print("runtime :", delta_time_torch*1000, "ms")
        print(f"Output shape at layer : {outputs.shape}")


def select_transformers_model(model, processor, pretrain="google/vit-base-patch16-224-in21k"):
    model = model.from_pretrained(pretrain)
    processor = processor.from_pretrained(pretrain)
    return model, processor

# pipeline for transformer library
class pipeline_transformer:
    def __init__(self, layer, row=False, device='cuda:0'):
        self.device = device
        self.layer = layer
        self.row = row
    
    def selct_model(self, model, processor):
        self.model = model
        self.processor = processor
        self.model.eval().to(self.device)
    
    def process_model(self, img, return_tensors="pt"):
        inputs = self.processor(images=img, return_tensors=return_tensors).to(self.device)
        outputs = self.model(**inputs)
        return outputs
        
    def extract(self, img, output_type='np'):
        ### return specific layer
        outputs = self.process_model(img)
        if type(self.row) == bool and not self.row:
            outputs = outputs[self.layer]
        else:
            outputs = outputs[self.layer][:, self.row]
        outputs = outputs.flatten().unsqueeze(0)
        outputs = standardize_feature(outputs)
        if output_type=='np':
            outputs = outputs.to('cpu').detach().numpy()
        return to_unit_len(outputs.flatten())
    
    def report_test(self):
        img = Image.new('RGB', (224, 224))
        start_time_torch = time.time()
        outputs = self.process_model(img)
        delta_time_torch = time.time() - start_time_torch
        print("runtime :", delta_time_torch*1000, "ms")
        print(f"outputs layers : {outputs.keys()}")
        print(f"shape last_hidden_state : {outputs.last_hidden_state.shape}")
        print(f"shape pooler_output : {outputs.pooler_output.shape}")


def select_transformers_onnx_model(path="google/vit-base-patch16-224-in21k", processor=None, providers=['CPUExecutionProvider']):
    from onnxruntime import InferenceSession
    
    model = InferenceSession(path, providers=providers)
    processor = processor.from_pretrained(Path(path).parent)
    return model, processor

# pipeline for transformer onnx library
class pipeline_transformer_onnx:
    def __init__(self, layer, row=False):
        self.layer = layer
        self.row = row
    
    def selct_model(self, model, processor):
        self.model = model
        self.processor = processor
    
    def process_model(self, img, return_tensors="np"):
        inputs = self.processor(images=img, return_tensors="np")
        outputs = self.model.run(output_names=[self.layer], input_feed=dict(inputs))[0]
        return outputs
        
    def extract(self, img):
        ### return specific layer
        outputs = self.process_model(img)
        if type(self.row) == bool and not self.row:
            outputs = outputs[0]
        else:
            outputs = outputs[:, self.row]
        outputs = standardize_feature(outputs)
        return outputs
    
    def report_test(self):
        img = Image.new('RGB', (224, 224))
        start_time_torch = time.time()
        outputs = self.process_model(img)
        delta_time_torch = time.time() - start_time_torch
        print("runtime :", delta_time_torch*1000, "ms")
        print(f"shape : {outputs.shape}")