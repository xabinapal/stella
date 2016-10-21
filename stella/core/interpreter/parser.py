# -*- coding: utf-8 -*-

import itertools

from stella.core.utils import Rewinder
from stella.core.interpreter.lexer import Tokenizer, Lexer, LexError
from stella.core.automata import NFA, convert_to_nfa

__all__ = ['ParseError', 'Parser']

################################################################################
### ParseError
################################################################################

class ParseError(SyntaxError):
    pass
    
################################################################################
### Parser
################################################################################

class Parser(object):
    def __init__(self, lexer, statements, ignore=[]):
        self.lexer = Rewinder(lexer)
        self.automata = [convert_to_nfa(
            x,
            r'\{(s|t)(\.[a-zA-Z_][a-zA-Z0-9_]+)*\}',
            lambda x, y: x == y.ttype) for x in statements]

        self.ignore = zip(ignore)
        self.ignore_until = None

    def __iter__(self):
        return Rewinder(self)

    def __next__(self):
        ignore_token = False
        while not ignore_token:
            try:
                token = next(self.lexer)
            except StopIteration:
                if self.ignore_until:
                    raise ParseError()

            ignore_token = self._ignore_token(token)

        return token

    def _ignore_token(self, token):
        if self.ignore_until:
            if token == self.ignore_until:
                self.ignore_until = None
            return True

        if not token.ttype:
            raise ParseError(token.value)

        ignore = (x for x in self.ignore if x[0] == token.ttype)
        ignore = next(ignore_token, None)

        if ignore:
            self.ignore_until = ignore[1] if len(ignore) > 1 else None
            return True

        return False
