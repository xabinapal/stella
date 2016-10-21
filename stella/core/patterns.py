# -*- coding: utf-8 -*-

class Singleton(type):
    def __call__(cls, *args, **kw):
        if not cls.instance:
            cls.instance = super(Singleton, cls).__call__(*args, **kw)

        return cls.instance