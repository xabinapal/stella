# -*- coding: utf-8 -*-

from core.interpreter.tokens import TokenType

################################################################################
### Identifiers
################################################################################

Identifier = TokenType.Identifier()

identifiers = (
	Identifier.LITERAL(r'[a-zA-Z_][a-zA-Z0-9_]*'),
	Identifier.WHITESPACE(r'[\s\t]+'),
	Identifier.NEWLINE(r'\r?\n'),
	Identifier.COMMENT(r'#.*\n?'),
)

################################################################################
### Keywords
################################################################################

Keyword = TokenType.Keyword()

keywords = (
	Keyword.BREAK('BREAK'),
	Keyword.CASE('CASE'),
	Keyword.CONTINUE('CONTINUE'),
	Keyword.DO('DO'),
	Keyword.ELSE('ELSE'),
	Keyword.FLOAT('FLOAT'),
	Keyword.FOR('FOR'),
	Keyword.IF('IF'),
	Keyword.INT('INT'),
	Keyword.RETURN('RETURN'),
	Keyword.SWITCH('SWITCH'),
	Keyword.WHILE('WHILE'),
	Keyword.BOOL('BOOL'),
)

################################################################################
### Constants
################################################################################

Constant = TokenType.Constant()
IntegerConstant = Constant.IntegerConstant()

FloatingConstant = Constant.FloatingConstant()

constants = (
	IntegerConstant.DECIMAL(r'(0|[1-9][0-9]*)'),
	IntegerConstant.HEXADECIMAL(r'0x[0-9a-fA-F]*'),
	IntegerConstant.OCTAL(r'0[0-7]+'),
	IntegerConstant.BINARY(r'0b[0-1]*'),
	FloatingConstant.DECIMAL(r'([0-9]+\.[0-9]*|[0-9]*\.[0-9]+)'),
)

################################################################################
### Punctuators
################################################################################

Punctuator = TokenType.Punctuator()

punctuators = (
	Punctuator.LBRACK(r'\['),
	Punctuator.RBRACK(r'\]'),
	Punctuator.LPAREN(r'\('),
	Punctuator.RPAREN(r'\)'),
	Punctuator.LBRACE(r'\{'),
	Punctuator.RBRACE(r'\}'),

	Punctuator.DOT(r'\.'),
	Punctuator.COMMA(r','),
	Punctuator.SEMICOLON(r';'),
	Punctuator.EQUAL(r'='),

	Punctuator.INC(r'\+'),
	Punctuator.DEC(r'-'),
	Punctuator.MUL(r'\*'),
	Punctuator.DIV(r'/'),
	Punctuator.MOD(r'%'),

	Punctuator.LSHIFT(r'<<'),
	Punctuator.RSHIFT(r'>>'),
	Punctuator.LROT(r'<<<'),
	Punctuator.RROT(r'>>>'),

	Punctuator.AND(r'&'),
	Punctuator.OR(r'\|'),
	Punctuator.XOR(r'\^'),
	Punctuator.NOT(r'~'),

	Punctuator.INC_OP(r'\+\+'),
	Punctuator.DEC_OP(r'--'),
	Punctuator.AND_OP(r'&&'),
	Punctuator.OR_OP(r'\|\|'),
	Punctuator.NOT_OP(r'!'),

	Punctuator.LT_OP(r'<'),
	Punctuator.GT_OP(r'>'),
	Punctuator.LEQ_OP(r'<='),
	Punctuator.GEQ_OP(r'>='),
	Punctuator.EQ_OP(r'=='),
	Punctuator.NEQ_OP(r'!='),
)

################################################################################
### Tokens
################################################################################

tokens = keywords + identifiers + constants + punctuators
