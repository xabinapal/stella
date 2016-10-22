# -*- coding: utf-8 -*-

import collections
import re

__all__ = ['TokenType', 'Token']

################################################################################
### TokenType
################################################################################

class _TokenType(tuple):
    def __contains__(self, item):
        return item is not None and (self is item or item[:len(self)] == self)
    
    def __getattr__(self, name):
        new = self.__class__(self + (name,))
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

    def is_of(self, value):
        parents = collections.deque(self)
        while hasattr('parent', parents[0]):
            parents.append(parents[0].parent)

        tokenized_value = value[1:-1].split('.')
        if tokenized_value[0] != 't':
            return False

        tokenized_value = collections.deque(tokenized_value[1:])
        while parents and tokenized_value:
            if tokenized_value[0] == parents[0]:
                tokenized_value.popleft()

            parents.popleft()

        return not parents and not tokenized_value

TokenType = _TokenType()

################################################################################
### Token
################################################################################

class Token(object):
    def __init__(self, ttype, value):
        self.ttype = ttype
        self.value = value
        
    def __eq__(self, other):
        if type(other) != Token:
            return False

        return self.ttype == other.ttype and self.value == other.value

    def __repr__(self):
        return '(' + repr(self.ttype) + ', "' + self.value + '")'
