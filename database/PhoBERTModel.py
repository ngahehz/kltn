from transformers import AutoTokenizer, AutoModel

class PhoBERTModel:
    _tokenizer_instance = None
    _model_instance = None

    @staticmethod
    def get_tokenizer_instance():
        if PhoBERTModel._tokenizer_instance is None:
            PhoBERTModel._tokenizer_instance = AutoTokenizer.from_pretrained("VoVanPhuc/sup-SimCSE-VietNamese-phobert-base")
        return PhoBERTModel._tokenizer_instance

    @staticmethod
    def get_model_instance():
        if PhoBERTModel._model_instance is None:
            PhoBERTModel._model_instance = AutoModel.from_pretrained("VoVanPhuc/sup-SimCSE-VietNamese-phobert-base")
        return PhoBERTModel._model_instance