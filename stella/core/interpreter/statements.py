# -*- coding: utf-8 -*-

import re

__all__ = ['StatementType']

################################################################################
### StatementType
################################################################################

class _StatementType(tuple):
    def __contains__(self, item):
        return item is not None and (self is item or item[:len(self)] == self)
    
    def __getattr__(self, name):
        new = self.__class__(self + (name,))
        new.parent = self
        new.name = name

        def statement(expr=None):
            new.expr = expr
            return new

        return statement

    def __repr__(self):
        return 'StatementType' + ('.' if self else '') + '.'.join(self)

StatementType = _StatementType()