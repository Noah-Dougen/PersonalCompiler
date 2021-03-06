'''
File: LastLighthouse_back_parser.py

This is Python Yacc code defining the grammar for three address code
used in the Drake University Compiler Construction course (CS 161) and
compiling it into MIPS

Author: Noah Dougen

Last Updated: 11/25/2019

'''
import ply.yacc as yacc
from LastLighhouse_back_lexer import tokens #the lexer we wrote
import sys
import os

#this is used for including the file with
#the multiply and divide procedures
this_directory = os.path.dirname(os.path.abspath(__file__))



'''
***Here is the full grammar***
program : instruction_list label_list

instruction_list : instruction_list instruction
instruction_list :

instruction : label_list three_address_instruction

three_address_instruction : lhs ASSIGN operand
three_address_instruction : lhs ASSIGN MINUS operand
three_address_instruction : lhs ASSIGN UNARYNOT operand
three_address_instruction : lhs ASSIGN operand TIMES operand
three_address_instruction : lhs ASSIGN operand DIVIDE operand 
three_address_instruction : lhs ASSIGN operand PLUS operand
three_address_instruction : lhs ASSIGN operand MINUS operand
three_address_instruction : lhs ASSIGN operand GREATERTHAN operand
three_address_instruction : lhs ASSIGN operand LESSTHAN operand
three_address_instruction : lhs ASSIGN operand GREATEQUAL operand
three_address_instruction : lhs ASSIGN operand LESSEQUAL operand
three_address_instruction : lhs ASSIGN operand EQUALTO operand
three_address_instruction : lhs ASSIGN operand NOTEQUAL operand
three_address_instruction : lhs ASSIGN operand AND operand
three_address_instruction : lhs ASSIGN operand OR operand
three_address_instruction : lhs ASSIGN ID LSQUARE numlist RSQUARE
three_address_instruction : LENGTH ASSIGN NUM
three_address_instruction : lhs ASSIGN ID LSQUARE NUM RSQUARE
three_address_instruction : IFFALSE ID GOTO ID
three_address_instruction : ELSE GOTO ID
three_address_instruction : WRITE operand
three_address_instruction : READ lhs


lhs : ID

label_list : label_list label
label_list :

numlist : NUM COMMA numlist
numlist : NUM
numlist :

operand : ID
operand : NUM

label : ID COLON

'''


'''
***Project notes***
This compiler produces ARM assembly code, with memory-mapped input/output.
That means that there are memory locations associated with console input
and output, and so to read and write, you will just load and store values
to these memory locations.

The registers r11 and r12 will keep track of the current location within
the memory block for each of output and input, so don't use them with any
other instruction translations.

'''


#This class will be used as the type for some
#p[0], p[1], etc. when we need to keep track of
#a value and what kind of thing it is (an id vs. a num)
class OperandInfo:
        def __init__(self):
                self.val = ''
                self.kind = ''

variable_set = set() # create an initially empty set to keep track of all the variables we see

#Each production in the grammar gets a function describing
#what to do when that rule is used in parsing


def p_program(p):
        '''
        program : instruction_list label_list
        '''
        pass

def p_instruction_list_instruction(p):
        '''
        instruction_list : instruction_list instruction
        '''
        pass

def p_instruction_list_empty(p):
        '''
        instruction_list :
        '''
        pass

def p_instruction(p):
        '''
        instruction : label_list three_address_instruction
        '''
        pass

def p_three_address_instruction_array(p):
        '''
        three_address_instruction : lhs ASSIGN ID LSQUARE numlist RSQUARE
        '''
        pass

def p_three_address_instruction_arrlength(p):
        '''
        three_address_instruction : LENGTH ASSIGN NUM
        '''
        print('\narrlength \tDCD\t', p[3])
        
def p_numlist_numlist(p):
        '''
        numlist : NUM COMMA numlist
        '''
        print(p[2], p[1], end='')

def p_numlist_num(p):
        '''
        numlist : NUM 
        '''
        print('arr', '\tDCD\t', p[1], end='')

def p_numlist_empty(p):
        '''
        numlist : 
        '''
        pass

def p_three_instruction_code_enterarray(p):
        '''
        three_address_instruction : lhs ASSIGN ID LSQUARE NUM RSQUARE
        '''
        print('index\t DCD\t', p[5])
        print('\t', 'LDR\tr2,=', p[3])
        print('\t', 'LDR\tr3,=length')
        print('\t', 'LDR\tr6,=index')
        print('\t', 'LDR\tr7,r6')
        print('\t', 'LDR\tr1,=#4')
        print('\t', 'LDR\tr0,r2')
        print('\t', 'LDR\tr4,r3')
        print('\t', 'SUB\tr0,r4,r7')
        print('\t','BL signed_multiply',sep='')
        print('\t', 'LDR\tr8,[r2,r0]')
        print('\t', 'STR\tr8,[r9]')
        
        
def p_three_address_instruction_assign(p):
        '''
        three_address_instruction : lhs ASSIGN operand
        '''
        #r0: address of operand p[3] if it is an id
        #r1: value of operand p[3]
        #r2: address of lhs

        #printing out a comment with a three-address code
        #version of what we're working on
        print('\n\t;',p[1],'=',p[3].val)

        #if it's a num, we don't need to also load the address
        if p[3].kind == 'num':
                print('\t','LDR r1, =',p[3].val,sep='')
        elif p[3].kind == 'id':
                print('\t','LDR r0, =',p[3].val,sep='')
                print('\t','LDR r1, [r0]',sep='')

        print('\t','LDR r2, =',p[1],sep='')
        print('\t','STR r1, [r2]',sep='')

def p_three_address_instruction_unary_minus(p):
        '''
        three_address_instruction : lhs ASSIGN MINUS operand
        '''
        #r0: address of operand p[4] if it is an id
        #r1: value of operand p[4]
        #r2: address of lhs

        #printing out a comment with a three-address code
        #version of what we're working on
        print('\n\t;',p[1],'= -',p[4].val)

        
        #if it's a num, we don't need to also load the address
        if p[4].kind == 'num':
                print('\t','LDR r1, =',p[4].val,sep='')
                print('\t','LDR r3, =0',sep='')
                print('\t','SUB r4, r3, r1',sep='')
                
        elif p[4].kind == 'id':
                print('\t','LDR r0, =',p[4].val,sep='')
                print('\t','LDR r1, [r0]',sep='')
                print('\t','LDR r3, =0',sep='')
                print('\t','SUB r4, r3, r1',sep='')

        print('\t','LDR r2, =',p[1],sep='')        
        print('\t','STR r4, [r2]',sep='')

def p_three_address_instruction_unarynot(p):
        '''
        three_address_instruction : lhs ASSIGN UNARYNOT operand
        '''
        #r0: address of operand p[4] if it is an id
        #r1: value of operand p[4]
        #r2: address of lhs

        #printing out a comment with a three-address code
        #version of what we're working on
        print('\n\t;',p[1],'= !',p[4].val)

        #if it's a num, we don't need to also load the address
        if p[4].kind == 'num':
                print('\t','LDR r1, =',p[4].val,sep='')
                print('\t','LDR r3, =0',sep='')
                
        elif p[4].kind == 'id':
                print('\t','LDR r0, =',p[4].val,sep='')
                print('\t','LDR r1, [r0]',sep='')

        print('\t','CMP r3, r1',sep='')
        print('\t','BE maketrue',sep='')
        print('\t','LDR r1, =',p[1],sep='')
        print('\t','STR r1, [r2]',sep='')
        
        print('maketrue')
        print('\t','LDR r5, =1',sep='')
        print('\t','LDR r1, =',p[1],sep='')
        print('\t','STR r5, [r2]',sep='')

def p_three_address_instruction_plus(p):
        '''
        three_address_instruction : lhs ASSIGN operand PLUS operand
        '''
        #r0: address of operand p[3]
        #r1: value of operand p[3]
        #r2: address of operand p[5]
        #r3: value of operand p[5]
        #r4: address of lhs p[1]
        #r5: address of the result to store in lhs p[1]

        #printing out a comment with a three-address code
        #version of what we're working on
        print('\n\t;',p[1],'=',p[3].val,'+',p[5].val)

        #load p[3]
        #if it's a num, we don't need to also load the address
        if p[3].kind == 'num':
                print('\t','LDR r1, =',p[3].val,sep='')
        elif p[3].kind == 'id':
                print('\t','LDR r0, =',p[3].val,sep='')
                print('\t','LDR r1, [r0]',sep='')

        #load p[5]
        #if it's a num, we don't need to also load the address
        if p[5].kind == 'num':
                print('\t','LDR r3, =',p[5].val,sep='')
        elif p[5].kind == 'id':
                print('\t','LDR r2, =',p[5].val,sep='')
                print('\t','LDR r3, [r2]',sep='')

        #load address for lhs p[1]
        print('\t','LDR r4, =',p[1],sep='')

        #perform operation
        print('\t','ADD r5, r1, r3',sep='')

        #store result
        print('\t','STR r5, [r4]',sep='')

def p_three_address_instruction_minus(p):
        '''
        three_address_instruction : lhs ASSIGN operand MINUS operand
        '''
        #r0: address of operand p[3]
        #r1: value of operand p[3]
        #r2: address of operand p[5]
        #r3: value of operand p[5]
        #r4: address of lhs p[1]
        #r5: address of the result to store in lhs p[1]

        #printing out a comment with a three-address code
        #version of what we're working on
        print('\n\t;',p[1],'=',p[3].val,'-',p[5].val)

        #load p[3]
        #if it's a num, we don't need to also load the address
        if p[3].kind == 'num':
                print('\t','LDR r1, =',p[3].val,sep='')
        elif p[3].kind == 'id':
                print('\t','LDR r0, =',p[3].val,sep='')
                print('\t','LDR r1, [r0]',sep='')

        #load p[5]
        #if it's a num, we don't need to also load the address
        if p[5].kind == 'num':
                print('\t','LDR r3, =',p[5].val,sep='')
        elif p[5].kind == 'id':
                print('\t','LDR r2, =',p[5].val,sep='')
                print('\t','LDR r3, [r2]',sep='')

        #load address for lhs p[1]
        print('\t','LDR r4, =',p[1],sep='')

        #perform operation
        print('\t','SUB r5, r1, r3',sep='')

        #store result
        print('\t','STR r5, [r4]',sep='')
        
def p_three_address_instruction_times(p):
        '''
        three_address_instruction : lhs ASSIGN operand TIMES operand
        '''
        #r2: address of operand p[3]
        #r0: value of operand p[3], later the value returned from
        #  the multiply procedure
        #r3: address of operand p[5]
        #r1: value of operand p[5]
        #r4: address of lhs p[1]

        #printing out a comment with a three-address code
        #version of what we're working on
        print('\n\t;',p[1],'=',p[3].val,'*',p[5].val)

        #load p[3]
        #if it's a num, we don't need to also load the address
        if p[3].kind == 'num':
                print('\t','LDR r0, =',p[3].val,sep='')
        elif p[3].kind == 'id':
                print('\t','LDR r2, =',p[3].val,sep='')
                print('\t','LDR r0, [r2]',sep='')

        #load p[5]
        #if it's a num, we don't need to also load the address
        if p[5].kind == 'num':
                print('\t','LDR r1, =',p[5].val,sep='')
        elif p[5].kind == 'id':
                print('\t','LDR r3, =',p[5].val,sep='')
                print('\t','LDR r1, [r3]',sep='')

        #load address for lhs p[1]
        print('\t','LDR r4, =',p[1],sep='')

        #perform operation, result goes in r0
        print('\t','BL signed_multiply',sep='')

        #store result
        print('\t','STR r0, [r4]',sep='')

def p_three_address_instruction_divide(p):
        '''
        three_address_instruction : lhs ASSIGN operand DIVIDE operand
        '''
        #r2: address of operand p[3]
        #r0: value of operand p[3], later the value returned from
        #  the divide procedure
        #r3: address of operand p[5]
        #r1: value of operand p[5]
        #r4: address of lhs p[1]

        #printing out a comment with a three-address code
        #version of what we're working on
        print('\n\t;',p[1],'=',p[3].val,'/',p[5].val)

        #load p[3]
        #if it's a num, we don't need to also load the address
        if p[3].kind == 'num':
                print('\t','LDR r0, =',p[3].val,sep='')
        elif p[3].kind == 'id':
                print('\t','LDR r2, =',p[3].val,sep='')
                print('\t','LDR r0, [r2]',sep='')

        #load p[5]
        #if it's a num, we don't need to also load the address
        if p[5].kind == 'num':
                print('\t','LDR r1, =',p[5].val,sep='')
        elif p[5].kind == 'id':
                print('\t','LDR r3, =',p[5].val,sep='')
                print('\t','LDR r1, [r3]',sep='')

        #load address for lhs p[1]
        print('\t','LDR r4, =',p[1],sep='')

        #perform operation, result goes in r0
        print('\t','BL signed_divide',sep='')

        #store result
        print('\t','STR r0, [r4]',sep='')

def p_three_address_instruction_greater_than(p):
        '''
        three_address_instruction : lhs ASSIGN operand GREATERTHAN operand
        '''

        #printing out a comment with a three-address code
        #version of what we're working on
        print('\n\t;',p[1],'=',p[3].val,'>',p[5].val)

        #load p[3]
        #if it's a num, we don't need to also load the address
        if p[3].kind == 'num':
                print('\t','LDR r0, =',p[3].val,sep='')
        elif p[3].kind == 'id':
                print('\t','LDR r2, =',p[3].val,sep='')
                print('\t','LDR r0, [r2]',sep='')

        #load p[5]
        #if it's a num, we don't need to also load the address
        if p[5].kind == 'num':
                print('\t','LDR r1, =',p[5].val,sep='')
        elif p[5].kind == 'id':
                print('\t','LDR r3, =',p[5].val,sep='')
                print('\t','LDR r1, [r3]',sep='')

        
        print('\t','CMP r1, r3',sep='')
        print('\t', 'BGT greater',sep='')

        print('\t','LDR r5, =0',sep='')
        #store result
        print('\t','STR r5, [r4]',sep='')
        
        print('greater')
        print('\t', 'LDR r5, =1',sep='')

        #store result
        print('\t','STR r5, [r4]',sep='')
        
def p_three_address_instruction_less_than(p):
        '''
        three_address_instruction : lhs ASSIGN operand LESSTHAN operand
        '''

        #printing out a comment with a three-address code
        #version of what we're working on
        print('\n\t;',p[1],'=',p[3].val,'<',p[5].val)

        #load p[3]
        #if it's a num, we don't need to also load the address
        if p[3].kind == 'num':
                print('\t','LDR r0, =',p[3].val,sep='')
        elif p[3].kind == 'id':
                print('\t','LDR r2, =',p[3].val,sep='')
                print('\t','LDR r0, [r2]',sep='')

        #load p[5]
        #if it's a num, we don't need to also load the address
        if p[5].kind == 'num':
                print('\t','LDR r1, =',p[5].val,sep='')
        elif p[5].kind == 'id':
                print('\t','LDR r3, =',p[5].val,sep='')
                print('\t','LDR r1, [r3]',sep='')

        
        print('\t','CMP r1, r3',sep='')
        print('\t', 'BLT less',sep='')

        print('\t','LDR r5, =0',sep='')
        #store result
        print('\t','STR r5, [r4]',sep='')
        
        print('less')
        print('\t', 'LDR r5, =1',sep='')

        #store result
        print('\t','STR r5, [r4]',sep='')

def p_three_address_instruction_great_equal(p):
        '''
        three_address_instruction : lhs ASSIGN operand GREATEQUAL operand
        '''

        #printing out a comment with a three-address code
        #version of what we're working on
        print('\n\t;',p[1],'=',p[3].val,'>=',p[5].val)

        #load p[3]
        #if it's a num, we don't need to also load the address
        if p[3].kind == 'num':
                print('\t','LDR r0, =',p[3].val,sep='')
        elif p[3].kind == 'id':
                print('\t','LDR r2, =',p[3].val,sep='')
                print('\t','LDR r0, [r2]',sep='')

        #load p[5]
        #if it's a num, we don't need to also load the address
        if p[5].kind == 'num':
                print('\t','LDR r1, =',p[5].val,sep='')
        elif p[5].kind == 'id':
                print('\t','LDR r3, =',p[5].val,sep='')
                print('\t','LDR r1, [r3]',sep='')

        
        print('\t','CMP r1, r3',sep='')
        print('\t', 'BGE greatequal',sep='')

        print('\t','LDR r5, =0',sep='')
        #store result
        print('\t','STR r5, [r4]',sep='')
        
        print('greatequal')
        print('\t', 'LDR r5, =1',sep='')

        #store result
        print('\t','STR r5, [r4]',sep='')

def p_three_address_instruction_less_equal(p):
        '''
        three_address_instruction : lhs ASSIGN operand LESSEQUAL operand
        '''

        #printing out a comment with a three-address code
        #version of what we're working on
        print('\n\t;',p[1],'=',p[3].val,'<=',p[5].val)

        #load p[3]
        #if it's a num, we don't need to also load the address
        if p[3].kind == 'num':
                print('\t','LDR r0, =',p[3].val,sep='')
        elif p[3].kind == 'id':
                print('\t','LDR r2, =',p[3].val,sep='')
                print('\t','LDR r0, [r2]',sep='')

        #load p[5]
        #if it's a num, we don't need to also load the address
        if p[5].kind == 'num':
                print('\t','LDR r1, =',p[5].val,sep='')
        elif p[5].kind == 'id':
                print('\t','LDR r3, =',p[5].val,sep='')
                print('\t','LDR r1, [r3]',sep='')

        print('\t','CMP r1, r3',sep='')
        print('\t', 'BLE lessequal',sep='')
        print('\t','LDR r5, =0',sep='')
        #store result
        print('\t','STR r5, [r4]',sep='')
        
        print('lessequal')
        print('\t', 'LDR r5, =1',sep='')

        #store result
        print('\t','STR r5, [r4]',sep='')        

def p_three_address_instruction_equalto(p):
        '''
        three_address_instruction : lhs ASSIGN operand EQUALTO operand
        '''

        #printing out a comment with a three-address code
        #version of what we're working on
        print('\n\t;',p[1],'=',p[3].val,'==',p[5].val)

        #load p[3]
        #if it's a num, we don't need to also load the address
        if p[3].kind == 'num':
                print('\t','LDR r0, =',p[3].val,sep='')
        elif p[3].kind == 'id':
                print('\t','LDR r2, =',p[3].val,sep='')
                print('\t','LDR r0, [r2]',sep='')

        #load p[5]
        #if it's a num, we don't need to also load the address
        if p[5].kind == 'num':
                print('\t','LDR r1, =',p[5].val,sep='')
        elif p[5].kind == 'id':
                print('\t','LDR r3, =',p[5].val,sep='')
                print('\t','LDR r1, [r3]',sep='')

        print('\t','CMP r1, r3',sep='')
        print('\t', 'BNE false',sep='')
        print('\t','LDR r5, =1',sep='')
        #store result
        print('\t','STR r5, [r4]',sep='')
        
        print('false')
        print('\t', 'LDR r5, =0',sep='')

        #store result
        print('\t','STR r5, [r4]',sep='')

def p_three_address_instruction_notequal(p):
        '''
        three_address_instruction : lhs ASSIGN operand NOTEQUAL operand
        '''

        #printing out a comment with a three-address code
        #version of what we're working on
        print('\n\t;',p[1],'=',p[3].val,'!=',p[5].val)

        #load p[3]
        #if it's a num, we don't need to also load the address
        if p[3].kind == 'num':
                print('\t','LDR r0, =',p[3].val,sep='')
        elif p[3].kind == 'id':
                print('\t','LDR r2, =',p[3].val,sep='')
                print('\t','LDR r0, [r2]',sep='')

        #load p[5]
        #if it's a num, we don't need to also load the address
        if p[5].kind == 'num':
                print('\t','LDR r1, =',p[5].val,sep='')
        elif p[5].kind == 'id':
                print('\t','LDR r3, =',p[5].val,sep='')
                print('\t','LDR r1, [r3]',sep='')

        print('\t','CMP r1, r3',sep='')
        print('\t', 'BE false',sep='')
        print('\t','LDR r5, =1',sep='')
        #store result
        print('\t','STR r5, [r4]',sep='')
        
        print('false')
        print('\t', 'LDR r5, =0',sep='')

        #store result
        print('\t','STR r5, [r4]',sep='')
        
def p_three_address_instruction_and(p):
        '''
        three_address_instruction : lhs ASSIGN operand AND operand
        '''

        #printing out a comment with a three-address code
        #version of what we're working on
        print('\n\t;',p[1],'=',p[3].val,'&&',p[5].val)

        #load p[3]
        #if it's a num, we don't need to also load the address
        if p[3].kind == 'num':
                print('\t','LDR r0, =',p[3].val,sep='')
        elif p[3].kind == 'id':
                print('\t','LDR r2, =',p[3].val,sep='')
                print('\t','LDR r0, [r2]',sep='')

        #load p[5]
        #if it's a num, we don't need to also load the address
        if p[5].kind == 'num':
                print('\t','LDR r1, =',p[5].val,sep='')
        elif p[5].kind == 'id':
                print('\t','LDR r3, =',p[5].val,sep='')
                print('\t','LDR r1, [r3]',sep='')

        print('\t', 'LDR r6, =0',sep='')
        
        print('\t','CMP r1, r6',sep='')
        print('\t', 'BE false',sep='')
        print('\t','CMP r3, r6',sep='')
        print('\t', 'BE false',sep='')

        print('\t','LDR r5, =1',sep='')
        #store result
        print('\t','STR r5, [r4]',sep='')
        
        print('false')
        print('\t', 'LDR r5, =0',sep='')
        #store result
        print('\t','STR r5, [r4]',sep='')

def p_three_address_instruction_or(p):
        '''
        three_address_instruction : lhs ASSIGN operand OR operand
        '''

        #printing out a comment with a three-address code
        #version of what we're working on
        print('\n\t;',p[1],'=',p[3].val,'||',p[5].val)

        #load p[3]
        #if it's a num, we don't need to also load the address
        if p[3].kind == 'num':
                print('\t','LDR r0, =',p[3].val,sep='')
        elif p[3].kind == 'id':
                print('\t','LDR r2, =',p[3].val,sep='')
                print('\t','LDR r0, [r2]',sep='')

        #load p[5]
        #if it's a num, we don't need to also load the address
        if p[5].kind == 'num':
                print('\t','LDR r1, =',p[5].val,sep='')
        elif p[5].kind == 'id':
                print('\t','LDR r3, =',p[5].val,sep='')
                print('\t','LDR r1, [r3]',sep='')

        print('\t', 'LDR r6, =0',sep='')
        
        print('\t','CMP r1, r6',sep='')
        print('\t', 'BNE true',sep='')
        print('\t','CMP r3, r6',sep='')
        print('\t', 'BNE true',sep='')

        print('\t','LDR r5, =0',sep='')
        #store result
        print('\t','STR r5, [r4]',sep='')
        
        print('true')
        print('\t', 'LDR r5, =1',sep='')
        #store result
        print('\t','STR r5, [r4]',sep='')

def p_three_address_instruction_if(p):
        '''
        three_address_instruction : IFFALSE ID GOTO ID 
        '''

        #printing out a comment with a three-address code
        #version of what we're working on
        print('\n\t;',p[1], p[2], p[3], p[4])


        print('\t', 'LDR r8, =0',sep='')
        
        print('\t','CMP r4, r6',sep='')
        print('\t', 'BE ', p[4],sep='')
        print(p[4])

def p_three_address_instruction_else(p):
        '''
        three_address_instruction : ELSE GOTO ID 
        '''
        print(p[3])

def p_three_address_instruction_write(p):
        '''
        three_address_instruction : WRITE operand
        '''
        #r11: address where we put output
        #   we will increase r11 by 4 so it points to the
        #   next spot for output
        #r0: value to output
        #r1: address of operand p[2]
        #r10: 4 - the amount to increase r11 by

        #printing out a comment with a three-address code
        #version of what we're working on
        print('\n\t; write',p[2].val)

        #load p[2]
        #if it's a num, we don't need to also load the address
        if p[2].kind == 'num':
                print('\t','LDR r0, =',p[2].val,sep='')
        elif p[2].kind == 'id':
                print('\t','LDR r1, =',p[2].val,sep='')
                print('\t','LDR r0, [r1]',sep='')
        
        #store value to output memory location
        print('\t','STR r0, [r11]',sep='')        

        #change r11 to point at the next input value
        print('\t','LDR r10, =4',sep='')      
        print('\t','ADD r11, r11, r10',sep='')

def p_three_address_instruction_read(p):
        '''
        three_address_instruction : READ lhs
        '''

        #r12: address where we find input
        #   we will increase r12 by 4 so it points to the
        #   next value of input
        #r0: value of the input
        #r1: address of lhs p[2]
        #r10: 4 - the amount to increase r12 by

        #printing out a comment with a three-address code
        #version of what we're working on
        print('\n\t; read',p[2])

        #load value at memory location of next input
        print('\t','LDR r0,[r12]',sep='')

        #load memory location of lhs
        print('\t','LDR r1, =',p[2],sep='')

        #store input value to memory location of lhs
        print('\t','STR r0, [r1]',sep='')

        #change r12 to point at the next input value
        print('\t','LDR r10, =4',sep='')      
        print('\t','ADD r12, r12, r10',sep='')


def p_label_list_label(p):
        '''
        label_list : label_list label
        '''
        pass

def p_label_list_empty(p):
        '''
        label_list :
        '''
        pass

def p_lhs(p):
        '''
        lhs : ID
        '''
        #labels in ARM code can't be a single character,
        #so to be on the safe side, we will prefix each
        #variable name with var_
        p[0] = 'var_'+p[1]

        #include this in the set of variables we need to
        #make space in memory for
        variable_set.add(p[0])


def p_operand_id(p):
        '''
        operand : ID
        '''
        #labels in ARM code can't be a single character,
        #so to be on the safe side, we will prefix each
        #variable name with var_
        p[0] = OperandInfo()
        p[0].val = 'var_'+p[1]
        p[0].kind = 'id'

        #include this in the set of variables we need to
        #make space in memory for
        variable_set.add(p[0].val)


def p_operand_num(p):
        '''
        operand : NUM
        '''
        p[0] = OperandInfo()
        p[0].val = p[1]
        p[0].kind = 'num'


#when we see a label, we just need to print the
#ARM label - same name but no colon
def p_label(p):
        '''
        label : ID COLON
        '''
        print(p[1])

  
# Error rule for syntax errors
def p_error(p):
	print("Syntax error in input!")

# Build the parser
parser = yacc.yacc()

#r12 will be used to keep track of the first address for input
#r11 will be used to keep track of the first address for output
print('\t; initializing the first addresses for the input and output buffers')
print('\tLDR r12, =_input')
print('\tLDR r11, =_output')

#parse the string from standard in
#stop at the EOF character
parser.parse(sys.stdin.read())

#emit the command to end execution here
print('\tEND')

#every output assembly file will contain some procedures
#for doing multiplication and division
mult_div_file = open(this_directory+'/mult_div.asm','r')
mult_div_file_contents = mult_div_file.read()
print(mult_div_file_contents)

print('\n\t; Below is the memory space for variables needed in this program')
for variable_name in variable_set:
        print(variable_name,'\tDCD\t0')

#initializing space for up to 100 input values
print('\n\t; Below is the memory space for memory-mapped input')
print('_input\tDCD\t'+('0,'*99)+'0')

#initializing space for up to 100 output values
print('\n\t; Below is the memory space for memory-mapped output')
print('_output\tDCD\t'+('0,'*99)+'0')





