'''
File: LastLighthouse_parser.py

This is Python Yacc code defining the grammar for a small C-like language
used in the Drake University Compiler Construction course (CS 161)

File: LastLighthouse_parser.py

This is Python parsing code which reads through a small C-like language
used in the Drake University Compiler Construction course (CS 161)

Author: Noah Dougen

Last Updated: 10/9/2019

'''
import ply.yacc as yacc
from LastLighthouse_lexer import tokens #the lexer we wrote
import sys
import LastLighthouse_AST #abstract syntax tree we wrote


'''
***Here is the full grammar***
program : block

block : LBRACE stmt_list RBRACE

stmt_list : stmt_list stmt
stmt_list :

stmt : type ID SEMICOLON
stmt : ID ASSIGN lowop SEMICOLON
stmt : block
stmt : READ ID SEMICOLON
stmt : WRITE lowop SEMICOLON
stmt : IF lowop LPAREN stmt optelse RPAREN
stmt : WHILE lowop LPAREN stmt RPAREN
stmt : lowop
stmt : comment

optelse : ELSE LPAREN stmt RPAREN
optelse : lowop
optelse : 

type : INT

lowop : lowop AND equal
lowop : lowop OR equal
lowop : equal

equal : equal EQUALTO op
equal : equal NOTEQUAL op
equal : op

op   : op LESSTHAN expr
op   : op GREATERTHAN expr
op   : op LESSEQUAL expr
op   : op GREATEREQUAL expr
op   : expr

expr : expr PLUS term
expr : expr MINUS term
expr : term

term : term TIMES factor
term : term DIVIDE factor
term : term MODULUS factor
term : factor

factor : MINUS factor
factor : UNARYNOT factor
factor : ID
factor : NUM
factor : LPAREN lowop RPAREN

comments : COMMENT
comments : MLCOMMENT

'''
symbol_table_list = []
scope_level = 0
scope_list = []
in_an_if = False

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
    block : LBRACE action_new_scope stmt_list RBRACE
    '''
    global scope_level
    scope_level -= 1
    symbol_table_list.pop(0)
    p[0] = p[3]

def p_action_new_scope(p):
    '''
    action_new_scope :
    '''
    global symbol_table_list
    new_symbol_table = {}
    global scope_level
    scope_level += 1
    symbol_table_list.insert(0,new_symbol_table)
        
#sequence nodes allow statements to be executed
#one after another
def p_stmt_list(p):
    '''
    stmt_list : stmt_list stmt
    '''
    p[0] = LastLighthouse_AST.SeqNode(p[1],p[2])

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
    global symbol_table_list
    global scope_level
    nested_p2 = (p[2] + str(scope_level))
    for symbol_table in symbol_table_list:
        if nested_p2 in symbol_table:
            print("error: this symbol has already been declared in this scope")
            return
    else:
        curr_symbol_table = symbol_table_list[0]
        curr_symbol_table[nested_p2] = (nested_p2,'line '+str(p.lineno(2)))
        p[0] = None #we don't need to include declarations in the tree yet

#assignment statements get assignment nodes
def p_stmt_assign(p):
    '''
    stmt : ID ASSIGN lowop SEMICOLON
    '''
    global symbol_table_list
    global scope_level
    nested_p1 = (p[1] + str(scope_level))
    for symbol_table in symbol_table_list:
        if nested_p1 in symbol_table:
            p[0] = LastLighthouse_AST.AssignNode(nested_p1,p[3])
            return
    print('Error:',nested_p1,'is not in the symbol table')
    p[0] = LastLighthouse_AST.AssignNode(nested_p1,p[3])

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
    global symbol_table_list
    global scope_level
    nested_p2 = (p[2] + str(scope_level))
    for symbol_table in symbol_table_list:
        if nested_p2 in symbol_table:
            p[0] = LastLighthouse_AST.ReadNode(nested_p2)
            return
    print('Error:',nested_p2,'is not in the symbol table')
    p[0] = LastLighthouse_AST.ReadNode(nested_p2)

#write statements get write nodes
def p_stmt_write(p):
    '''
    stmt : WRITE lowop SEMICOLON
    '''
    
    p[0] = LastLighthouse_AST.WriteNode(p[2])
    
def p_stmt_if(p):

    '''
    stmt : IF lowop LPAREN stmt optelse RPAREN
    '''
    if p[5] == None:
        p[0] = LastLighthouse_AST.IfNode(p[2],p[4])
    else:
        p[0] = LastLighthouse_AST.IfElseNode(p[2],p[4], p[5])


def p_stmt_while(p):
    '''
    stmt : WHILE lowop LPAREN stmt RPAREN
    '''
    p[0] = LastLighthouse_AST.WhileNode(p[2],p[4])

def p_stmt_lowop(p):
    '''
    stmt : lowop
    '''
    
    p[0] = p[1]

def p_stmt_comment(p):
    '''
    stmt : comment
    '''
    p[0] = p[1]

def p_optelse_else(p):
    '''
    optelse : ELSE LPAREN stmt RPAREN
    '''
    p[0] = p[3]

def p_optelse_empty(p):
    '''
    optelse : 
    '''
    
    p[0] = None
    
#we're not doing anything with types yet
def p_type_int(p):
    '''
    type : INT
    '''
    p[0] = p[1]

#start of the lowops

def p_lowop_and(p):
    '''
    lowop : lowop AND equal
    '''
    p[0] = LastLighthouse_AST.BinaryOpNode(p[2],p[1],p[3])

def p_lowop_or(p):
    '''
    lowop : lowop OR equal
    '''
    p[0] = LastLighthouse_AST.BinaryOpNode(p[2],p[1],p[3])

def p_lowop_equal(p):
    '''
    lowop : equal
    '''
    p[0] = p[1]

#start of the equals

def p_equal_equalto(p):
    '''
    lowop : equal EQUALTO op
    '''
    p[0] = LastLighthouse_AST.BinaryOpNode(p[2],p[1],p[3])

def p_equal_notequal(p):
    '''
    equal : equal NOTEQUAL op
    '''
    p[0] = LastLighthouse_AST.BinaryOpNode(p[2],p[1],p[3])

def p_equal_op(p):
    '''
    equal : op
    '''
    p[0] = p[1]

#start of the ops
    
def p_op_lessthan(p):
    '''
    op : op LESSTHAN expr
    '''
    p[0] = LastLighthouse_AST.BinaryOpNode(p[2],p[1],p[3])

def p_op_greaterthan(p):
    '''
    op : op GREATERTHAN expr
    '''
    p[0] = LastLighthouse_AST.BinaryOpNode(p[2],p[1],p[3])

def p_op_lessequal(p):
    '''
    op : op LESSEQUAL expr
    '''
    p[0] = LastLighthouse_AST.BinaryOpNode(p[2],p[1],p[3])
    
def p_op_greatequal(p):
    '''
    op : op GREATEQUAL expr
    '''
    p[0] = LastLighthouse_AST.BinaryOpNode(p[2],p[1],p[3])
    
def p_op_expr(p):
    '''
    op : expr
    '''
    p[0] = p[1]

#expression with the + operator are represented
#with a binary operator node in the AST
def p_expr_plus(p):
    '''
    expr : expr PLUS term
    '''
    p[0] = LastLighthouse_AST.BinaryOpNode(p[2],p[1],p[3])

def p_expr_minus(p):
    '''
    expr : expr MINUS term
    '''
    p[0] = LastLighthouse_AST.BinaryOpNode(p[2],p[1],p[3])
	
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
    p[0] = LastLighthouse_AST.BinaryOpNode(p[2],p[1],p[3])

def p_term_divide(p):
    '''
    term : term DIVIDE factor
    '''
    p[0] = LastLighthouse_AST.BinaryOpNode(p[2],p[1],p[3])

def p_term_modulus(p):
    '''
    term : term MODULUS factor
    '''
    p[0] = LastLighthouse_AST.BinaryOpNode(p[2],p[1],p[3])



def p_term_factor(p):
    '''
    term : factor
    '''
    p[0] = p[1]

#we only need the value passed by the lexer
#to create a leaf node with an ID

def p_factor_unaryminus(p):
    '''
    factor : MINUS factor
    '''
    p[0] = LastLighthouse_AST.UnaryNode(p[1], p[2])

def p_factor_unarynot(p):
    '''
    factor : UNARYNOT factor
    '''
    p[0] = LastLighthouse_AST.UnaryNode(p[1], p[2])
    
def p_factor_id(p):
    '''
    factor : ID 
    '''
    global symbol_table_list
    global scope_level
    nested_p1 = (p[1] + str(scope_level))
    for symbol_table in symbol_table_list:
        if nested_p1 in symbol_table:
            p[0] = LastLighthouse_AST.LeafNode(nested_p1)
            return
    print('Error:',nested_p1,'is not in the symbol table')
    p[0] = LastLighthouse_AST.LeafNode(nested_p1)
	
#we only need the value passed by the lexer (which was converted to an int)
#to create a leaf node with a NUM
def p_factor_num(p):
    '''
    factor : NUM
    '''
    p[0] = LastLighthouse_AST.LeafNode(p[1])

#parenthetical statements can be passed up the tree
def p_factor_parens(p):
    '''
    factor : LPAREN lowop RPAREN
    '''
    p[0] = p[2]

def p_comment_comment(p):
    '''
    comment : COMMENT
    '''
    p[0] = None

def p_comment_mlcomment(p):
    '''
    comment : MLCOMMENT 
    '''
    p[0] = None

# Error rule for syntax errors
def p_error(p):
    print("Syntax error in input!")

# Build the parser
parser = yacc.yacc()
parser.parse(sys.stdin.read())



