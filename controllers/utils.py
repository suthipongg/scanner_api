from pathlib import Path
import numpy as np

# convert to unit vector
def to_unit_len(vector):
    return vector / np.linalg.norm(vector)

# standardize feature
def standardize_feature(arr):
    return (arr-arr.mean())/arr.std()


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
        inputs = self.processor(images=img, return_tensors=return_tensors)
        outputs = self.model.run(output_names=[self.layer], input_feed=dict(inputs))[0]
        return outputs
        
    def extract(self, img):
        ### return specific layer
        outputs = self.process_model(img)
        if type(self.row) == bool and not self.row:
            outputs = outputs[0]
        else:
            outputs = outputs[:, self.row]
        outputs = outputs.flatten()
        outputs = standardize_feature(outputs)
        return to_unit_len(outputs)