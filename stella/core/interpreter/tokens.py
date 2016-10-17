# -*- coding: utf-8 -*-

import re

__all__ = ['TokenType', 'Token']

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
        new.name = name

        def token(expr=None):
            new.expr = expr
            new.compiled_expr = re.compile(expr) if expr else None
            return new

        return token

    def __repr__(self):
        return 'TokenType' + ('.' if self else '') + '.'.join(self)
    
    def match(self, value):
        return self.compiled_expr.fullmatch(value) if self.expr else None

TokenType = _TokenType()

################################################################################
### Token
################################################################################

class Token(object):
    def __init__(self, ttype, value):
        self.ttype = ttype
        self.value = value
        
    def __eq__(self, other):
        return self.ttype == other.ttype and self.value == other.value

    def __repr__(self):
        return '(' + repr(self.token_type) + ', "' + self.value + '")'
