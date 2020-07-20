These files contain the code for a simple starter compiler used in CS 161. To start with, the simple programming language syntax contains variable declarations, assignment statements, input and output statements. Mathematical expressions with multiplication and addition of integers are supported. 

All code is written for Python 3.

The files are as follows:

AST.py - A file with class definitions for an abstract syntax tree representation of the program being compiled
README.txt - this file
sampleProgram.prg - an example program written in a simple programming language syntax
starter_lexer.py - The PLY Lex definitions of the language's tokens
starter_parser.py - The PLY Yacc implementation of language syntax. This parser builds an AST which is then used to generate three address code.


To run this compiler, run the following at a command prompt:

python starter_parser.py


By default, this will wait for you type in the program at standard input. If you would like to compile a program from a file, like sampleProgram.prg, you can run a command like cat (on Mac/Unix/Linux) or type (on Windows) to display the file contents and then pipe them into the compiler with a command like

cat sampleProgram.prg | python starter_parser.py

or

type sampleProgram.prg | python starter_parser.py

To save the results to a file such as result.tac, redirect the output with a command like 

cat sampleProgram.prg | python starter_parser.py > result.tac

or

type sampleProgram.prg | python starter_parser.py > result.tac