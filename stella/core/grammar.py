# -*- coding: utf-8 -*-

from stella.core.interpreter.productions import TokenType, StatementType
from stella.core.interpreter.parser import RDParser, TDOPParser

__all__ = ['Tokens', 'Statements', 'ProgramStatement']

################################################################################
### Keywords
################################################################################

Keyword = TokenType.Keyword()
FlowControl = Keyword.FlowControl()
DataType = Keyword.DataType()

FlowControlKeywords = (
    FlowControl.IF(r'if'),
    FlowControl.ELSE(r'else'),
    FlowControl.WHILE(r'while'),
    FlowControl.FOR(r'for'),
    FlowControl.BREAK(r'break'),
    FlowControl.CONTINUE(r'continue'),
    FlowControl.RETURN(r'return'),
)

DataTypeKeywords = (
    DataType.INTEGER('int'),
    DataType.FLOATING('float'),
)

Keywords = FlowControlKeywords + DataTypeKeywords

################################################################################
### Identifiers
################################################################################

Identifier = TokenType.Identifier()
Comment = Identifier.Comment()

_literal = Identifier.LITERAL(r'[a-zA-Z_][a-zA-Z0-9_]*')
_whitespace = Identifier.WSPACE(r'[\s\t]+')
_newline = Identifier.NLINE(r'\r?\n')
_comment_line = Comment.LINE(r'//.*\n?')
_comment_start = Comment.START(r'/\*')
_comment_end = Comment.END(r'\*/')

Identifiers = (
    _literal, _whitespace, _newline,
    _comment_line, _comment_start, _comment_end,
)

################################################################################
### Constants
################################################################################

Constant = TokenType.Constant()
IntegerConstant = Constant.IntegerConstant()
FloatingConstant = Constant.FloatingConstant()

Constants = (
    IntegerConstant.INTEGER_DECIMAL(r'(0|[1-9][0-9]*)'),
    IntegerConstant.INTEGER_HEXADECIMAL(r'0x[a-fA-F0-9]*'),
    IntegerConstant.INTEGER_OCTAL(r'0[0-7]+'),
    IntegerConstant.INTEGER_BINARY(r'0b[0-1]*'),
    FloatingConstant.FLOATING_DECIMAL(r'([0-9]+\.[0-9]*|[0-9]*\.[0-9]+)'),
)

################################################################################
### Punctuators
################################################################################

Punctuator = TokenType.Punctuator()
Operator = Punctuator.Operator()
UnaryOperator = Operator.UnaryOperator(has_unary_bp=True)
InfixOperator = Operator.InfixOperator(has_infix_bp=True)
UnaryOrInfixOperator = Operator.UnaryOrInfixOperator(has_unary_bp=True, has_infix_bp=True)

Punctuators = (
    Punctuator.DOT(r'\.'),
    Punctuator.COMMA(r','),
    Punctuator.SEMICOLON(r';'),
    Punctuator.EQUAL(r'='),

    Punctuator.LBRACE(r'\{'),
    Punctuator.RBRACE(r'\}'),

    Punctuator.LBRACK(r'\[', infix_bp=400),
    Punctuator.RBRACK(r'\]', infix_bp=400),
    Punctuator.LPAREN(r'\(', infix_bp=300),
    Punctuator.RPAREN(r'\)', infix_bp=300),

    UnaryOperator.INC_OP(r'\+\+', unary_bp=200),
    UnaryOperator.DEC_OP(r'--', unary_bp=200),
    UnaryOperator.BITWISE_NOT(r'~', unary_bp=100),
    UnaryOperator.LOGICAL_NOT(r'!', unary_bp=100),

    InfixOperator.MUL(r'\*', infix_bp=100),
    InfixOperator.DIV(r'/', infix_bp=100),
    InfixOperator.MOD(r'%', infix_bp=100),

    InfixOperator.LSHIFT(r'<<', infix_bp=80),
    InfixOperator.RSHIFT(r'>>', infix_bp=80),
    InfixOperator.LROT(r'<<<', infix_bp=80),
    InfixOperator.RROT(r'>>>', infix_bp=80),

    InfixOperator.LT_OP(r'<', infix_bp=70),
    InfixOperator.GT_OP(r'>', infix_bp=70),
    InfixOperator.LEQ_OP(r'<=', infix_bp=70),
    InfixOperator.GEQ_OP(r'>=', infix_bp=70),

    InfixOperator.EQ_OP(r'==', infix_bp=60),
    InfixOperator.NEQ_OP(r'!=', infix_bp=60),

    InfixOperator.BITWISE_AND(r'&', infix_bp=50),
    InfixOperator.BITWISE_XOR(r'\^', infix_bp=40),
    InfixOperator.BITWISE_OR(r'\|', infix_bp=30),

    InfixOperator.LOGICAL_AND(r'&&', infix_bp=20),
    InfixOperator.LOGICAL_OR(r'\|\|', infix_bp=10),

    UnaryOrInfixOperator.INC(r'\+', unary_bp=100, infix_bp=90),
    UnaryOrInfixOperator.DEC(r'-', unary_bp=100, infix_bp=90),
)

################################################################################
### Tokens
################################################################################

Tokens = Keywords + Identifiers + Constants + Punctuators
IgnoreTokens = (
    (_whitespace,),
    (_newline,),
    (_comment_line,),
    (_comment_start, _comment_end),
)

################################################################################
### Statements
################################################################################

ProgramStatement = StatementType.Program(r'{s.FunctionDeclaration}({s.Program}|)', parser=RDParser)

Function = StatementType.Function(parser=RDParser)

FunctionStatements = (
    Function.FunctionArgument(r'{t.DataType}{t.LITERAL}'),
    Function.FunctionNextArgument(r'{t.COMMA}{s.FunctionArgument}'),
    Function.FunctionArguments(r'{s.FunctionArgument}{s.FunctionNextArgument}*'),
    Function.FunctionArgumentList(r'{t.LPAREN}({s.FunctionArguments}|){t.RPAREN}'),
    Function.FunctionDeclaration(r'{t.DataType}{t.LITERAL}{s.FunctionArgumentList}{s.RegularBlock}'),
)

Variable = StatementType.Variable(parser=RDParser)

VariableStatements = (
    Variable.VariableDeclaration(r'{t.DataType}{t.LITERAL}({t.EQUAL}{t.SimpleExpression}|){t.SEMICOLON}'),
    Variable.VariableAssignment(r'{t.LITERAL}({t.EQUAL}{t.SimpleExpression}|)'),
)

Block = StatementType.Block(parser=RDParser)

BlockStatements = (
    Block.RegularBlock(r'{t.LBRACE}({s.Statement}|{s.RegularBlock})*{t.RBRACE}'),
    Block.LoopBlock(r'{t.LBRACE}({s.Jump}|{s.Statement}|{s.RegularBlock})*{t.RBRACE}'),
)

Jump = StatementType.Jump(parser=RDParser)

JumpStatements = (
    Jump.Break(r'{t.BREAK}{t.SEMICOLON}'),
    Jump.Continue(r'{t.CONTINUE}{t.SEMICOLON}'),
)

Control = StatementType.Control(parser=RDParser)

ControlStatements = (
    Control.If(r'{t.IF}{t.LPAREN}{s.SimpleExpression}{t.RPAREN}{s.RegularBlock}({t.ELSE}{s.Statement}|)'),
    Control.While(r'{t.WHILE}{t.LPAREN}{s.SimpleExpression}{t.RPAREN}{s.LoopBlock}'),
    Control.For(r'{t.FOR}{t.LPAREN}({s.SimpleExpression}|){t.SEMICOLON}({s.SimpleExpression}|){t.SEMICOLON}({s.SimpleExpression}|){t.RPAREN}{s.LoopBlock}'),
)

StatementType.SimpleExpression(parser=TDOPParser)

#Statements = (
#    StatementType.Empty(r'{t.SEMICOLON}'),
#)

Statements = (ProgramStatement,) + FunctionStatements + BlockStatements + JumpStatements # + ControlStatements

################################################################################
### ASTs
################################################################################

#class FunctionDeclaration(AST):
#    __statement__ = Function.FunctionDeclaration
