import collections
import re
from projekt.tokens import Token as t

Token = collections.namedtuple('Token', ['type', 'value', 'line', 'column'])


class Scanner:

    def __init__(self, input):
        self.tokens = []
        self.current_token_number = 0
        for token in self.tokenize(input):
            self.tokens.append(token)

    def tokenize(self, input_string):
        keywords = {t.VERSION, t.SERVICES, t.BUILD, t.PORTS, t.IMAGE, t.VOLUMES, t.ENVIRONMENT, t.NETWORKS,
                    t.DEPLOY}
        token_specification = [
            (t.STRING, r'\"(.*?)\"'),
            (t.NUMBER, r'\d+(\.\d*)?'),
            (t.ID, r'[A-Za-z_./-]+'),
            (t.ASSIGN, r':'),
            (t.ITEM, r'-'),
            (t.NEWLINE, r'\n'),
            (t.SKIP, r'[ \t]')
        ]
        tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
        get_token = re.compile(tok_regex).match
        line_number = 1
        position = 0
        current_position = line_start = 0
        match = get_token(input_string)
        while match is not None:
            match_type = match.lastgroup
            if match_type == t.NEWLINE:
                line_start = position
                line_number += 1
            elif match_type != t.SKIP:
                value = match.group(match_type)
                if match_type == t.ID and value in keywords:
                    match_type = value
                elif match_type == t.ID and value == "-":
                    match_type = t.ITEM
                elif match_type == t.ID and value == ":":
                    match_type = t.ASSIGN
                yield Token(match_type, value, line_number, match.start() - line_start)
            current_position = match.end()
            match = get_token(input_string, current_position)
        if current_position != len(input_string):
            raise RuntimeError('Error: Unexpected character %r on line %d' % \
                               (input_string[current_position], line_number))
        yield Token('EOF', '', line_number, current_position - line_start)

    def next_token(self):
        self.current_token_number += 1
        if self.current_token_number - 1 < len(self.tokens):
            return self.tokens[self.current_token_number - 1]
        else:
            raise RuntimeError('Error: No more tokens')
