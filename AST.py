
class Node(object):

	def __str__(self):
		return self.printTree()

class Const(Node):
	pass

class Integer(Const):
	pass

class Float(Const):
	pass

class String(Const):
	pass

class Variable(Node):
	pass

class BinExpr(Node):
	pass 
	
class Program(Node):
	pass
	
class Declarations(Node):
	pass
	
class Declaration(Node):
	pass
	
class ErrorNode(Node):
	pass
	
class Inits(Node):
	pass

class Init(Node):
	pass
	
class Instructions(Node):
	pass
	
class Instruction(Node):
	pass
	
class PrintInstruction(Instruction):
	pass
	
class LabeledInstruction(Instruction):
	pass
	
class Assignment(Instruction):
	pass
	
class ChoiceInstruction(Instruction):
	pass
	
class WhileInstruction(Instruction):
	pass

class RepeatInstruction(Instruction):
	pass

class ReturnInstruction(Instruction):
	pass

class ContinueInstruction(Instruction):
	pass

class BreakInstruction(Instruction):
	pass

class CompoundInstruction(Instruction):
	pass

class Condition(Instruction):
	pass

class Expression(Node):
	pass
	
class IdentExpression(Expression):
	pass

class ConstExpression(Expression):
	pass

class ParenthesizedExpression(Expression):
	pass

class BinaryExpression(Expression):
	pass

class LabeledExpression(Expression):
	pass
	
class EmptyNode(Node):
	pass
	
class ExpressionList(Node):
	pass

class Fundefs(Node):
	pass

class Fundef(Node): 
	pass	

class ArgsList(Node):
	pass

class Arg(Node):
	pass	
	