import json
import numpy as np
from hazm import *
from random import shuffle
from informationretrieval.health_retrieval import fasttext_model


class BooleanModel:
    def __init__(self):
        self.lemmatizer = Lemmatizer()
        self.boolean_matix = np.load('models/doc-term-boolean.npy')
        with open(f'models/doc-term-boolean-data.json', 'r', encoding="utf-8") as f:
            self.data = json.loads(f.read())
        with open(f'models/doc-term-boolean-tokens.json', 'r', encoding="utf-8") as f:
            self.all_tokens = json.loads(f.read())

    def process_query(self, query):
        query_tokens = query.strip().lower().split()
        query_tokens = [self.lemmatizer.lemmatize(token) for token in query_tokens]
        operands = list()
        operators = list()
        i = 0
        while i < len(query_tokens):
            token = query_tokens[i]
            if token == 'and' or token == 'or':
                operators.append(token)
            elif token == 'not':
                operands.append(('not', query_tokens[i + 1]))
                i += 1
            else:
                operands.append(('', token))
            i += 1
        return operands, operators

    def get_token_column(self, token):
        if token[1] in self.all_tokens:
            column = self.boolean_matix[:, self.all_tokens.index(token[1])]
            if token[0] == 'not':
                column = ~column
            return column
        else:
            return np.zeros(len(self.data), dtype=bool)

    def operate(self, operand1, operand2, operator):
        if operator == 'and':
            return operand1 & operand2
        elif operator == 'or':
            return operand1 | operand2

    def get_nearest_neighbors(self, query, k, query_expansion=True):
        results = set()
        operands, operators = self.process_query(query)
        results |= set(self.get_result(operands, operators))
        if query_expansion:
            for _ in range(5):
                new_operands = self.query_expansion(operands)
                results |= set(self.get_result(new_operands, operators))
        results = list(results)
        shuffle(results)
        return results[:k] if k < len(results) else results

    def get_result(self, operands, operators):
        neighbors = list()
        n = len(operands)
        if n < 2:
            result = self.get_token_column(operands[0])
        else:
            column_operand_1 = self.get_token_column(operands[0])
            column_operand_2 = self.get_token_column(operands[1])
            result = self.operate(column_operand_1, column_operand_2, operators[0])
            for i, operand in enumerate(operands[2:]):
                other_operand = self.get_token_column(operand)
                result = self.operate(result, other_operand, operators[i + 1])
        indices = result.nonzero()[0]
        for index in indices:
            neighbors.append(self.data[index])
        return self.convert_dic_ls_to_tuples(neighbors)

    def query_expansion(self, operands):
        new_operands = []
        for item in operands:
            similar_words = fasttext_model.ft_model.wv.most_similar(item[1])
            similar_words_list = []
            for word in similar_words:
                if 0.8 < word[1] < 0.98:
                    lemmatized = self.lemmatizer.lemmatize(word[0])
                    if lemmatized not in ([_[1] for _ in new_operands] + similar_words_list):
                        similar_words_list.append(lemmatized)
            if len(similar_words_list) > 0:
                new_operands.append((item[0], np.random.choice(similar_words_list)))
        return new_operands if new_operands else operands

    def print_similars(self, query, k=10):
        ls = self.get_nearest_neighbors(query, k)
        for i, item in enumerate(ls):
            print(f"{i + 1}- title: {item[0]}")
            print(f"{i + 1}- link: {item[1]}")
            print('-------------------------')

    def convert_dic_ls_to_tuples(self, ls):
        final_ls = []
        for item in ls:
            final_ls.append((item['title'], item['link']))
        return final_ls

    def get_query(self, query, k=10, query_expansion=True):
        return self.get_nearest_neighbors(query, k, query_expansion)


boolean_model = BooleanModel()
