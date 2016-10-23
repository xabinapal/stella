# -*- coding: utf-8 -*-

import re

__all__ = ['TokenType', 'Token', 'StatementType', 'Statement']

################################################################################
### _ProductionType
################################################################################

class _ProductionType(tuple):
    def __init__(self, *args, **kwargs):
        self.items = []

    @staticmethod
    def _init_member(member):
        pass

    def __getattr__(self, name):
        def production_type(expr=None):
            new = self.__class__(self + (name,))
            new.name = name
            new.expr = expr
            new.parent = self

            self.__class__._init_member(new)

            parent = self
            while parent.__class__ == self.__class__:
                parent.items.append(new)
                parent = parent.parent

            return new

        return production_type

    def __repr__(self):
        return '<' + self.__class__.__name__ + '> ' + '.'.join(self)

################################################################################
### TokenType
################################################################################

class _TokenType(_ProductionType):
    @staticmethod
    def _init_member(member):
        member.compiled_expr = re.compile(member.expr) if member.expr else None

    def match(self, value):
        return self.compiled_expr.fullmatch(value) if self.expr else None

    def is_of(self, value):
        if not isinstance(value, str):
            return False
            
        parents = [x for x in self]
        parents.reverse()
        
        tokenized_value = value[1:-1].split('.')
        tokenized_value.reverse()
        
        while parents and tokenized_value:
            if parents.pop() == tokenized_value[-1]:
                tokenized_value.pop()

        return not tokenized_value

TokenType = _TokenType('t')

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

################################################################################
### StatementType
################################################################################

class _StatementType(_ProductionType):
    def __repr__(self):
        return 'StatementType' + ('.' if self else '') + '.'.join(self)

    @staticmethod
    def is_statement(value):
        if not isinstance(value, str):
            return False

        return value[1:-1].split('.')[0] == 's'

StatementType = _StatementType('s')
