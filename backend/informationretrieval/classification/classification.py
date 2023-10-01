import pickle

from transformers import AutoModelForSequenceClassification, AutoTokenizer

from informationretrieval.health_retrieval import fasttext_model
from informationretrieval.utils import get_category_title


class ClassicClassifier:
    def predict(self, text):
        emb = fasttext_model.get_text_embeding(text)
        return get_category_title(self.model.predict(emb.reshape(1, -1))[0])


class NaiveBayesClassifier(ClassicClassifier):
    def __init__(self):
        self.model = pickle.load(open('models/classification-clustering/naive-bayes.sav', 'rb'))


class LogisticRegressionClassifier(ClassicClassifier):
    def __init__(self):
        self.model = pickle.load(open('models/classification-clustering/logistic-regression.sav', 'rb'))


class TransformerClassifier:
    def __init__(self):
        self.model = AutoModelForSequenceClassification.from_pretrained('models/transformer_model',
                                                                        local_files_only=True)
        self.tokenizer = AutoTokenizer.from_pretrained('models/pretrained-transformer-tokenizer')

    def predict(self, text):
        _input = self.tokenizer(text, truncation=True, padding=True, return_tensors='pt')
        output = self.model(**_input)
        return get_category_title(output[0].softmax(1).argmax().item())


transformer_classifier = TransformerClassifier()
logistic_regression_classifier = LogisticRegressionClassifier()
naive_bayes_classifier = NaiveBayesClassifier()
