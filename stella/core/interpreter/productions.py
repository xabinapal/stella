# -*- coding: utf-8 -*-

import re

__all__ = ['ProductionError', 'TokenType', 'Token', 'StatementType', 'Statement']

################################################################################
### ProductionError
################################################################################

class ProductionError(SyntaxError):
    pass

################################################################################
### _ProductionType
################################################################################

class _ProductionType(tuple):
    def __init__(self, *args, **kw):
        self.name = None
        self.expr = None
        self.parent = None

        self.items = [self]

    @staticmethod
    def _init_member(member, **kw):
        pass

    def __contains__(self, item):
        return item in self.items

    def __getattr__(self, name):
        existing = next((x for x in self.items if x.name == name), None)
        if existing:
            self.items.remove(existing)
            existing.parent = None

        parent = self.parent
        while parent.__class__ == self.__class__:
            if next((x for x in parent.items if x.name == name), None):
                raise KeyError(name)

            parent = parent.parent

        def production_type(expr=None, **kw):
            new = self.__class__(self + (name,))
            new.name = name
            new.expr = expr
            new.parent = self

            self.__class__._init_member(new, **kw)

            parent = self
            while parent.__class__ == self.__class__:
                parent.items.append(new)
                parent = parent.parent

            return new

        return production_type

    def __repr__(self):
        return '<' + self.__class__.__name__ + '> ' + '.'.join(self)

    def is_str_repr(self, value):
        if not isinstance(value, str):
            return False

        if value[0] != '{' or value[-1] != '}':
            return False
            
        parents = [x for x in self]
        parents.reverse()
        
        tokenized_value = value[1:-1].split('.')
        tokenized_value.reverse()
        
        while parents and tokenized_value:
            if parents.pop() == tokenized_value[-1]:
                tokenized_value.pop()

        return not tokenized_value

    def parse_str_repr(self, value):
        if not isinstance(value, str):
            return None

        if value[0] != '{' or value[-1] != '}':
            return False

        value = value[1:-1].split('.')
        for x in self.items:
            item = [y for y in x]
            tokenized_value = value[:]
            while item and tokenized_value:
                if item.pop() == tokenized_value[-1]:
                    tokenized_value.pop()

            if not tokenized_value:
                return x

        return None

################################################################################
### TokenType
################################################################################

class _TokenType(_ProductionType):
    @staticmethod
    def _init_member(member, **kw):
        member.compiled_expr = re.compile(member.expr) if member.expr else None
        
        member.has_unary_bp = kw.get('has_unary_bp', member.parent.has_unary_bp)
        member.has_infix_bp = kw.get('has_infix_bp', member.parent.has_infix_bp)

        member.unary_bp = kw.get('unary_bp', None)
        member.infix_bp = kw.get('infix_bp', None)

        if member.unary_bp and not member.has_unary_bp:
            raise ProductionError('Unary binding power not allowed')

        if member.infix_bp and not member.has_infix_bp:
            raise ProductionError('Infix binding power not allowed')

    def match(self, value):
        return self.compiled_expr.fullmatch(value) if self.expr else None

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
    pass

StatementType = _StatementType('s')
