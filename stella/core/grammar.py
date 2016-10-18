# -*- coding: utf-8 -*-

from stella.core.interpreter.tokens import TokenType
from stella.core.interpreter.statements import StatementType

__all__ = ['Tokens, Statements']

################################################################################
### Keywords
################################################################################

Keyword = TokenType.Keyword()
FlowControl = Keyword.FlowControl()
DataType = Keyword.DataType()

FlowControlKeywords = (
    Keyword.FlowControl.FUNCTION('FUNCTION'),
    Keyword.FlowControl.IF('IF'),
    Keyword.FlowControl.ELSE('ELSE'),
    Keyword.FlowControl.WHILE('WHILE'),
    Keyword.FlowControl.FOR('FOR'),
    Keyword.FlowControl.BREAK('BREAK'),
    Keyword.FlowControl.CONTINUE('CONTINUE'),
    Keyword.FlowControl.RETURN('RETURN'),
)

DataTypeKeywords = (
    Keyword.DataType.DECIMAL('DECIMAL'),
    Keyword.DataType.INTEGER('INTEGER'),
)

Keywords = FlowControlKeywords + DataTypeKeywords

################################################################################
### Identifiers
################################################################################

Identifier = TokenType.Identifier()
Comment = Identifier.Comment()

Identifiers = (
    Identifier.LITERAL(r'[a-zA-Z_][a-zA-Z0-9_]*'),
    Identifier.WS(r'[\s\t]+'),
    Identifier.NEWLINE(r'\r?\n'),
    Comment.STR(r'/\*'),
    Comment.END(r'\*/'),
    Comment.LINE(r'//.*\n?'),
)

################################################################################
### Constants
################################################################################

Constant = TokenType.Constant()
IntegerConstant = Constant.IntegerConstant()
FloatingConstant = Constant.FloatingConstant()

Constants = (
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

Punctuators = (
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

Tokens = Keywords + Identifiers + Constants + Punctuators

################################################################################
### Statements
################################################################################

Statement = StatementType.SpaceSplit(separator=r'({t.WHITESPACE}|{t.NEWLINE})*', ignore=r'{t.COMMENT}')
Jump = Statement.Jump()

JumpStatements = (
    Jump.Break(r'{t.BREAK}{t.SEMICOLON}'),
    Jump.Continue(r'{t.CONTINUE}{t.SEMICOLON}'),
)

Statements = (
    Statement.Empty(r'{t.SEMICOLON}'),
    Statement.Block(r'{t.LBRACE}{s}{t.RBRACE}'),
    Statement.FunctionArguments(r'{t.DataType}{t.LITERAL}({t.COMMA}{s.FunctionArguments))?'),
    Statement.FunctionArgumentList(r'{t.LPAREN}{s.FunctionArguments}{t.RPAREN}'),
    Statement.Function(r'{t.FUNCTION}{t.DataType}{t.LITERAL}{t.FunctionArgumentList}{s.Block}'),
)
