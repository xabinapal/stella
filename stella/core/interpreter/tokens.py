# -*- coding: utf-8 -*-

import re

################################################################################
### TokenType
################################################################################

class _TokenType(tuple):
    def __contains__(self, item):
        return item is not None and (self is item or item[:len(self)] == self)
    
    def __getattr__(self, name):
        new = _TokenType(self + (name,))
        setattr(self, name, new)
        new.parent = self

        def token(expr=None):
            new.expr = re.compile(expr) if expr else None
            return new
        return token

    def __repr__(self):
        return 'TokenType' + ('.' if self else '') + '.'.join(self)
    
    def match(self, value):
        return self.expr.fullmatch(value) if self.expr else None

TokenType = _TokenType()

################################################################################
### Token
################################################################################

class Token(object):
    def __init__(self, token_type, value):
        self.token_type = token_type
        self.value = value

    def __repr__(self):
        return '(' + repr(self.token_type) + ', "' + self.value + '")'
