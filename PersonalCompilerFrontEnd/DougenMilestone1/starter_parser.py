'''
File: starter_parser.py

This is Python Yacc code defining the grammar for a small C-like language
used in the Drake University Compiler Construction course (CS 161)

Author: Eric D. Manley

Last Updated: 8/21/2019

'''
import ply.yacc as yacc
from LastLighthouse_lexer import tokens #the lexer we wrote
import sys
import AST #abstract syntax tree we wrote


'''
***Here is the full grammar***
program : block

block : LBRACE stmt_list RBRACE

stmt_list : stmt_list stmt
stmt_list : 

stmt : type ID SEMICOLON
stmt : ID ASSIGN expr SEMICOLON
stmt : block
stmt : READ ID SEMICOLON
stmt : WRITE expr SEMICOLON

type : INT

expr : expr PLUS term
expr : term

term : term TIMES factor
term : factor

factor : ID
factor : NUM
factor : LPAREN expr RPAREN

'''

#Each production in the grammar gets a function describing
#what to do when that rule is used in parsing

#program is the top-level symbol, for now defined as a single
#block of code. Once we have the full AST built, we call the
#gen() function on the root which will recursively emit the
#three address code for the entire tree
def p_program(p):
	'''
	program : block
	'''
	p[0] = p[1]
	p[0].gen()

def p_block(p):
	'''
	block : LBRACE stmt_list RBRACE
	'''
	p[0] = p[2]

#sequence nodes allow statements to be executed
#one after another
def p_stmt_list(p):
	'''
	stmt_list : stmt_list stmt
	'''
	p[0] = AST.SeqNode(p[1],p[2])

#a statement list can be empty, if so we have a
#termoinal spot in the AST represented by None
def p_stmt_list_empty(p):
	'''
	stmt_list : 
	'''
	p[0] = None

#declaration statements - the language doesn't do
#anything with this other than parse them
def p_stmt_decl(p):
	'''
	stmt : type ID SEMICOLON
	'''
	p[0] = None #we don't need to include declarations in the tree yet

#assignment statements get assignment nodes
def p_stmt_assign(p):
	'''
    stmt : ID ASSIGN expr SEMICOLON
	'''
	p[0] = AST.AssignNode(p[1],p[3])

#blocks just get passed up the tree
def p_stmt_block(p):
	'''
	stmt : block
	'''
	p[0] = p[1]

#read statements get read nodes
def p_stmt_read(p):
	'''
	stmt : READ ID SEMICOLON
	'''
	p[0] = AST.ReadNode(p[2])

#write statements get write nodes
def p_stmt_write(p):
	'''
	stmt : WRITE expr SEMICOLON
	'''
	p[0] = AST.WriteNode(p[2])

#we're not doing anything with types yet
def p_type(p):
	'''
	type : INT
	'''
	pass

#expression with the + operator are represented
#with a binary operator node in the AST
def p_expr_plus(p):
	'''
	expr : expr PLUS term
	'''
	p[0] = AST.BinaryOpNode(p[2],p[1],p[3])
	

def p_expr_term(p):
	'''
	expr : term
	'''
	p[0] = p[1]


#expression with the * operator are represented
#with a binary operator node in the AST
def p_term_times(p):
	'''
	term : term TIMES factor
	'''
	p[0] = AST.BinaryOpNode(p[2],p[1],p[3])

def p_term_factor(p):
	'''
	term : factor
	'''
	p[0] = p[1]

#we only need the value passed by the lexer
#to create a leaf node with an ID
def p_factor_id(p):
	'''
	factor : ID
	'''
	p[0] = AST.LeafNode(p[1])

#we only need the value passed by the lexer (which was converted to an int)
#to create a leaf node with a NUM
def p_factor_num(p):
	'''
	factor : NUM
	'''
	p[0] = AST.LeafNode(p[1])

#parenthetical statements can be passed up the tree
def p_factor_parens(p):
	'''
	factor : LPAREN expr RPAREN
	'''
	p[0] = p[2]


# Error rule for syntax errors
def p_error(p):
	print("Syntax error in input!")

# Build the parser
parser = yacc.yacc()
#parse the string from standard in
#stop at the EOF character
parser.parse(sys.stdin.read())



