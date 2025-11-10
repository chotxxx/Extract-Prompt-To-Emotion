import re
try:
    from underthesea import word_tokenize
    UNDERTHESEA_AVAILABLE = True
except ImportError:
    UNDERTHESEA_AVAILABLE = False
try:
    from transformers import AutoTokenizer
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False

class VietnamesePreprocessor:
    def __init__(self, phobert_model="vinai/phobert-base"):
        if TRANSFORMERS_AVAILABLE:
            self.tokenizer = AutoTokenizer.from_pretrained(phobert_model, use_fast=False)
        else:
            self.tokenizer = None
        # Sentiment Slang Dictionary - customizable
        self.slang_dict = {
            "ko": "không",
            "mng": "mọi người",
            "bt": "bình thường",
            "dc": "được",
            "k": "không",
            "r": "rồi",
            "vs": "với",
            "tk": "tớ",
            "mn": "mọi người",
            "ad": "admin",
            "vip": "vip",
            "pro": "chuyên nghiệp",
            "ngon": "tốt",
            "xấu": "tệ",
            "tuyệt": "tuyệt vời",
            "oke": "ok",
            "ok": "được",
            "hihi": "cười",
            "haha": "cười",
            "hehe": "cười",
            # Add more as needed
        }

    def remove_noise(self, text):
        """Remove noise: special chars, URLs, mentions, repeated chars"""
        # Remove URLs
        text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
        # Remove mentions
        text = re.sub(r'@\w+', '', text)
        # Remove repeated chars (e.g., ngonnn -> ngon)
        text = re.sub(r'(.)\1{2,}', r'\1', text)
        # Remove special chars except Vietnamese diacritics and spaces
        text = re.sub(r'[^\w\sàáảãạâầấẩẫậăằắẳẵặèéẻẽẹêềếểễệđìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵÀÁẢÃẠÂẦẤẨẪẬĂẰẮẲẴẶÈÉẺẼẸÊỀẾỂỄỆĐÌÍỈĨỊÒÓỎÕỌÔỒỐỔỖỘƠỜỚỞỠỢÙÚỦŨỤƯỪỨỬỮỰỲÝỶỸỴ]', ' ', text)
        # Normalize whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        return text

    def normalize_teencode(self, text):
        """Normalize teencode and slang"""
        words = text.split()
        normalized_words = []
        for word in words:
            lower_word = word.lower()
            if lower_word in self.slang_dict:
                normalized_words.append(self.slang_dict[lower_word])
            else:
                normalized_words.append(word)
        return ' '.join(normalized_words)

    def word_segmentation(self, text):
        """Word segmentation using underthesea or fallback"""
        if UNDERTHESEA_AVAILABLE:
            return word_tokenize(text, format="text")
        else:
            # Fallback: simple split by spaces
            return text

    def tokenize(self, text):
        """Tokenize using PhoBERT tokenizer or fallback"""
        if TRANSFORMERS_AVAILABLE and self.tokenizer:
            return self.tokenizer(text, return_tensors="pt", padding=True, truncation=True)
        else:
            # Fallback: return text as dict
            return {"input_ids": text, "attention_mask": [1] * len(text.split())}

    def preprocess(self, text):
        """Full preprocessing pipeline"""
        text = self.remove_noise(text)
        text = self.normalize_teencode(text)
        segmented = self.word_segmentation(text)
        return segmented

    def preprocess_for_phobert(self, text):
        """Preprocess and tokenize for PhoBERT"""
        processed = self.preprocess(text)
        return self.tokenize(processed)