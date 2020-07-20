The backend compiler takes input in the form of three address code and output ARM assembler code
Which can be executed in VisUAL. If your three address code file is called tac.txt, you would run
it like this:

(Mac/Linux)

cat tac.txt | python backend_starter_parser.py

or

(Windows)

type tac.txt | python starter_parser.py

To save the results to a file such as result.txt, redirect the output with a command like 

cat tac.txt | python backend_starter_parser.py > result.txt

or

type tac.txt | python backend_starter_parser.py > result.txt



If you want to combine this with the front end compiler run the following command from the parent directory of both starterFrontEnd and starterBack end. This assumes a program source file called sampleProgram.prg is in the parent folder as well:


(Mac/Linux)

cat sampleProgram.prg | python starterFrontEnd/starter_parser.py | python starterBackEnd/backend_starter_parser.py

or

(Windows)

type sampleProgram.prg | python starterFrontEnd/starter_parser.py | python starterBackEnd/backend_starter_parser.py

To save the results to a file such as result.txt, redirect the output with a command like 

cat sampleProgram.prg | python starterFrontEnd/starter_parser.py | python starterBackEnd/backend_starter_parser.py > result.txt

or

type cat sampleProgram.prg | python starterFrontEnd/starter_parser.py | python starterBackEnd/backend_starter_parser.py > result.txt


11/25/19 Update:

In this update, I added support to the backend parser for the following statements: *, /, +, -, 
<, >, <=, >=, ==, !=, &&, ||, unary - and !, If, Else. The goal was to have the parser print
out code that could be read in VisUAL. The assignment was split into 4 parts: the operators,
the truth operators, the unary operators, and the if statements. 

For the the first part (*,/,+,-) I used the existing code as a template. For subtraction, I
changed the printed "ADD" in the addition branch to a printed "SUB." Similarly, division
was taken from the existing multiplication branch. "signed multiply" was changed to "signed
divide." These can be seen in test1to4.txt.

For the truth operators (<, >, <=, >=, ==, !=, &&, ||), I created new branches. These would
print out code comparing the operands to a truth value (0 or 1) and evtually storing 0 or 1
as the outputed truth value. They all followed the same basic format, only changing to 
match with the truth value being measured. These can be seen in test5to12.txt.

For the unary operators, I borrowed from the assign statement. The idea for unary minus
was to set a value to 0 and subtract that by the affected number. For unary not, I compared
the value of the affected statement against 0 and switched the outputed truth value based on
the results. These can be seen in test13to14.txt.

Finally, I had to add the if statements to the parser. The three address code my compiler created 
included an IfFalse statement and an else statement. For the first one, I compared the result
of the result of the if statement's prerequsite against 0 and had the code create a branch
based on the label included with the if statement. For the else statement, I simply had the
code automatically branch to the associated label beacuase the else would be skipped over
if the if statement was true. These can be seen in test15to16.txt. 