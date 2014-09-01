#!/usr/bin/python

from scanner import Scanner
import AST
from TreePrinter import TreePrinter



class Cparser(object):


	def __init__(self):
		self.scanner = Scanner()
		self.scanner.build()
		tp = TreePrinter()

	tokens = Scanner.tokens


	precedence = (
	   ("nonassoc", 'IFX'),
	   ("nonassoc", 'ELSE'),
	   ("right", '='),
	   ("left", 'OR'),
	   ("left", 'AND'),
	   ("left", '|'),
	   ("left", '^'),
	   ("left", '&'),
	   ("nonassoc", '<', '>', 'EQ', 'NEQ', 'LE', 'GE'),
	   ("left", 'SHL', 'SHR'),
	   ("left", '+', '-'),
	   ("left", '*', '/', '%'),
	)


	def p_error(self, p):
		if p:
			print("Syntax error at line {0}, column {1}: LexToken({2}, '{3}')".format(p.lineno, self.scanner.find_tok_column(p), p.type, p.value))
		else:
			print('At end of input')



	def p_program(self, p):
		"""program : declarations fundefs instructions"""
		p[0] = AST.Program()
		p[0].dec = p[1]
		p[0].fun = p[2]
		p[0].ins = p[3]
		p[0].printTree()

	def p_declarations(self, p):
		"""declarations : declarations declaration
						| """
		p[0] = AST.Declarations()
		if len(p) == 3:
			p[0].dec = p[1].dec + [p[2]]
		else: 
			p[0].dec = []
					 

	def p_declaration(self, p):
		"""declaration : TYPE inits ';' 
					   | error ';' """
		if len(p) == 4:
			p[0] = AST.Declaration()
			p[0].type = p[1]
			p[0].inits = p[2]
		else:
			p[0] = AST.ErrorNode()
			p[0].error = p[1]


	def p_inits(self, p):
		"""inits : inits ',' init
				 | init """
		p[0] = AST.Inits()
		if len(p) == 4: 
			p[0].inits = p[1].inits + [p[3]]
		else: 
			p[0].inits = [p[1]]


	def p_init(self, p):
		"""init : ID '=' expression """
		#self.ids.append(p[1])
		p[0] = AST.Init()
		p[0].id = p[1]
		p[0].exp = p[3]


	def p_instructions(self, p):
		"""instructions : instructions instruction
						| instruction """
		p[0] = AST.Instructions()
		if len(p) == 3: 
			p[0].ins = p[1].ins + [p[2]]
		else:
			p[0].ins = [p[1]]


	def p_instruction(self, p):
		"""instruction : print_instr
					   | labeled_instr
					   | assignment
					   | choice_instr
					   | while_instr 
					   | repeat_instr 
					   | return_instr
					   | break_instr
					   | continue_instr
					   | compound_instr"""
		p[0] = p[1]

	def p_print_instr(self, p):
		"""print_instr : PRINT expression ';'
					   | PRINT error ';' """
		p[0] = AST.PrintInstruction()
		p[0].exp = p[2]					   
					   


	def p_labeled_instr(self, p):
		"""labeled_instr : ID ':' instruction """
		p[0] = AST.LabeledInstruction()
		p[0].id = p[1]
		p[0].ins = p[3]

	def p_assignment(self, p):
		"""assignment : ID '=' expression ';' """
		p[0] = AST.Assignment()
		p[0].id = p[1]
		p[0].exp = p[3]		


	def p_choice_instr(self, p):
		"""choice_instr : IF '(' condition ')' instruction  %prec IFX
						| IF '(' condition ')' instruction ELSE instruction
						| IF '(' error ')' instruction  %prec IFX
						| IF '(' error ')' instruction ELSE instruction """
		p[0] = AST.ChoiceInstruction()
		p[0].cond = p[3]
		p[0].ifIns = p[5]
		p[0].elIns = p[7]


	def p_while_instr(self, p):
		"""while_instr : WHILE '(' condition ')' instruction
					   | WHILE '(' error ')' instruction """
		p[0] = AST.WhileInstruction()
		p[0].cond = p[3]
		p[0].ins = p[5]


	def p_repeat_instr(self, p):
		"""repeat_instr : REPEAT instructions UNTIL condition ';' """
		p[0] = AST.RepeatInstruction()
		p[0].ins = p[2]
		p[0].cond = p[4]
	
	
	def p_return_instr(self, p):
		"""return_instr : RETURN expression ';' """
		p[0] = AST.ReturnInstruction()
		p[0].exp = p[2]

	
	def p_continue_instr(self, p):
		"""continue_instr : CONTINUE ';' """
		p[0] = AST.ContinueInstruction()

	
	def p_break_instr(self, p):
		"""break_instr : BREAK ';' """
		p[0] = AST.BreakInstruction()

	
	
	def p_compound_instr(self, p):
		"""compound_instr : '{' declarations instructions '}' """
		p[0] = AST.CompoundInstruction()
		p[0].dec = p[2]
		p[0].ins = p[3]

	
	def p_condition(self, p):
		"""condition : expression"""
		p[0] = AST.Condition()
		p[0].exp = p[1]
		
	def p_const(self, p):
		"""const : INTEGER
				 | FLOAT
				 | STRING""" 
		if isinstance(p[1],int): p[0] = AST.Integer()
		elif isinstance(p[1], float): p[0] = AST.Float()
		else: p[0] = AST.String()
		p[0].value = p[1]
		#p[0].printTree()

	def p_expression(self, p):
		"""expression : const
					  | ID
					  | expression '+' expression
					  | expression '-' expression
					  | expression '*' expression
					  | expression '/' expression
					  | expression '%' expression
					  | expression '|' expression
					  | expression '&' expression
					  | expression '^' expression
					  | expression AND expression
					  | expression OR expression
					  | expression SHL expression
					  | expression SHR expression
					  | expression EQ expression
					  | expression NEQ expression
					  | expression '>' expression
					  | expression '<' expression
					  | expression LE expression
					  | expression GE expression
					  | '(' expression ')'
					  | '(' error ')'
					  | ID '(' expr_list_or_empty ')'
					  | ID '(' error ')' """
		if len(p) == 2:
			if type(p[1]).__name__ == 'str':
				p[0] = AST.IdentExpression()
				p[0].id = p[1]
			else:
				p[0] = AST.ConstExpression()
				p[0].value = p[1]

		elif len(p) == 4 and p[2] in ['+', '-', '*', '/', '%', '|', '&', '^', 'AND', 'OR', 'SHL', 'SHR', '==', '!=', '>', '<', '<=', '>=']:
			p[0] = AST.BinaryExpression()
			p[0].type = p[2]
			p[0].op1 = p[1]
			p[0].op2 = p[3]
		elif len(p) == 4:
			p[0] = AST.ParenthesizedExpression()
			p[0].exp = p[2]
			pass
		else:
			p[0] = AST.LabeledExpression()
			p[0].id = p[1]
			p[0].exp = p[3]

		
	def p_expr_list_or_empty(self, p):
		"""expr_list_or_empty : expr_list
							  | """
		if len(p) == 2: p[0] = p[1]
		else: p[0] = AST.EmptyNode()
	

	def p_expr_list(self, p):
		"""expr_list : expr_list ',' expression
					 | expression """
		p[0] = AST.ExpressionList()
		if len(p) == 4: p[0].exp = p[1].exp + [ p[3] ]
		else: p[0].exp = [ p[1] ]
	
	
	def p_fundefs(self, p):
		"""fundefs : fundef fundefs
				   |  """
		p[0] = AST.Fundefs()
		if len(p) == 3: p[0].funs = p[2].funs + [ p[1] ]
		else: p[0].funs = []


	def p_fundef(self, p):
		"""fundef : TYPE ID '(' args_list_or_empty ')' compound_instr """
		p[0] = AST.Fundef()
		p[0].type = p[1]
		p[0].id = p[2]
		p[0].args = p[4]
		p[0].instr = p[6]
	
	
	def p_args_list_or_empty(self, p):
		"""args_list_or_empty : args_list
							  | """
		if len(p) == 2: p[0] = p[1]
		else: p[0] = AST.EmptyNode()

	
	def p_args_list(self, p):
		"""args_list : args_list ',' arg 
					 | arg """
		p[0] = AST.ArgsList()
		if len(p) == 4: p[0].args = p[1].args + [ p[3] ]
		else: p[0].args = [ p[1] ]

	
	def p_arg(self, p):
		"""arg : TYPE ID """
		p[0] = AST.Arg()
		p[0].type = p[1]
		p[0].id = p[2]

		
		
