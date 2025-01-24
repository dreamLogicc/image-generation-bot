from huggingface_hub import InferenceClient


class IMGGen:

    def __init__(self, hf_key: str, model: str = "stabilityai/stable-diffusion-3.5-large"):
        self.client = InferenceClient(model, token=hf_key)
        self.model = model

    def set_model(self, model: str, hf_key: str):
        self.model = model
        self.client = InferenceClient(model, token=hf_key)

    def get_model(self):
        return self.model

    def generate(self, text: str):
        return self.client.text_to_image(text)
