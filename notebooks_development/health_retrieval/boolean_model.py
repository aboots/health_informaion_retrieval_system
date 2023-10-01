import json
import numpy as np
from hazm import *
from random import shuffle


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

    def get_nearest_neighbors(self, query, k):
        neighbors = list()
        operands, operators = self.process_query(query)
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
        shuffle(neighbors)
        return neighbors[:k] if k < len(neighbors) else neighbors

    def print_similars(self, query, k=10):
        ls = self.get_nearest_neighbors(query, k)
        for i, item in enumerate(ls):
            print(f"{i + 1}- title: {item['title']}")
            print(f"{i + 1}- link: {item['link']}")
            print('-------------------------')
