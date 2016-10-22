# -*- coding: utf-8 -*-

from stella.core.utils import Rewinder
from stella.core.interpreter.lexer import Tokenizer, Lexer, LexError
from stella.core.automata import ENFA, convert_to_enfa

import copy

__all__ = ['ParseError', 'Parser']

################################################################################
### ParseError
################################################################################

class ParseError(SyntaxError):
    pass
    
################################################################################
### Parser
################################################################################

_st_re = r'\{(s|t)(\.[a-zA-Z_][a-zA-Z0-9_]+)*\}'

class Parser(object):
    def __init__(self, lexer, statements, ignore=[]):
        self.lexer = Rewinder(lexer)
        self.automata = [convert_to_enfa(x.expr, _st_re) for x in statements]
        self.ignore = ignore
        self.ignore_until = None

    def __iter__(self):
        return Rewinder(self)

    def __next__(self):
        self.lexer.peek() # if no tokens left, raises an StopIteration
        valid_automata = copy.deepcopy(self.automata)
        validated_automata = False
        while not validated_automata or len(valid_automata) > 1:
            token = self._get_token()
            for x in valid_automata:
                x.input(token)

            valid_automata[:] = (x for x in valid_automata if x.valid_state())
            validated_automata = True

        if not valid_automata:
            raise ParseError()

        print(valid_automata)

        return valid_automata[0]

    def _get_token(self):
        ignore_token = True
        while ignore_token:
            try:
                token = next(self.lexer)
                ignore_token = self._ignored_token(token)
            except StopIteration as e:
                if self.ignore_until:
                    raise ParseError()

                raise e

        return token

    def _ignored_token(self, token):
        if self.ignore_until:
            if token.ttype == self.ignore_until:
                self.ignore_until = None
            return True

        if not token.ttype:
            raise ParseError('Unexpected token ' + token.value)

        ignore = (x for x in self.ignore if x[0] == token.ttype)
        ignore = next(ignore, None)

        if ignore:
            self.ignore_until = ignore[1] if len(ignore) > 1 else None
            return True

        return False
