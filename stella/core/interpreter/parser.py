# -*- coding: utf-8 -*-

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
    def __init__(self, lexer):
        self.lexer = Rewinder(lexer)

    def __iter__(self):
        return Rewinder(self)

    def __next__(self):
        token = next(self.lexer)
        if not token.ttype:
            raise ParseError(token.value)

        return token
