# -*- coding: utf-8 -*-

import io
import collections

from stella.core.utils import CharStream, Rewinder
from stella.core.interpreter.tokens import Token

__all__ = ['Tokenizer', 'Lexer']

################################################################################
### Tokenizer
################################################################################

class Tokenizer(object):
    def __init__(self, tokens):
        self.tokens = tokens

    def get_token(self, value):
        return next((x for x in self.tokens if x.match(value)), None)

################################################################################
### Lexer
################################################################################

class Lexer(object):
    def __init__(self, stream, tokenizer):
        char_stream = CharStream(stream)
        self.iterator = Rewinder(char_stream)
        self.tokenizer = tokenizer

    def __iter__(self):
        return Rewinder(self)

    def __next__(self):
        token = None

        tmp_value = next(self.iterator)
        tmp_token = self.tokenizer.get_token(tmp_value)
        token_found = False
        while tmp_token or not token_found:
            if tmp_token:
                token_found = True
                value = tmp_value
                token = tmp_token

            try:
                char = self.iterator.peek()
                tmp_token = self.tokenizer.get_token(tmp_value + char)

                if not token and not tmp_token and self.tokenizer.get_token(char):
                    token_found = True
                    value = tmp_value

                if tmp_token or not token_found:
                    tmp_value = tmp_value + char
                    next(self.iterator)

            except StopIteration:
                value = tmp_value
                token = tmp_token
                break

        self.iterator.commit()
        return Token(token, value)
