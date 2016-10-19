# -*- coding: utf-8 -*-

import itertools

from stella.core.utils import Rewinder

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
    def __init__(self, lexer, ignore=[]:
        self.lexer = Rewinder(lexer)
        self.ignore = zip(ignore)
        self.ignore_until = None

    def __iter__(self):
        return Rewinder(self)

    def __next__(self):
        valid_token = False
        while not valid_token:
            try:
                token = next(self.lexer)
            except StopIteration:
                if self.ignore_until:
                    raise ParseError()

            valid_token = self._is_valid_token(token)

        return token

    def _is_valid_token(self, token):
        if self.ignore_until:
            if token == self.ignore_until:
                self.ignore_until = None
            return False

        if not token.ttype:
            raise ParseError(token.value)

        ignore = (x for x in self.ignore if x[0] == token.ttype)
        ignore = next(ignore_token, None)

        if ignore:
            self.ignore_until = ignore[1] if len(ignore) > 1 else None
            return False

        return True
