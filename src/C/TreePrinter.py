
import AST


level = -1

def addToClass(cls):

	def decorator(func):
		setattr(cls,func.__name__,func)
		return func
	return decorator


def printFun(s, shift = 0):
	#print (level + shift) * " |", s
	print s,
	
class TreePrinter:

	@addToClass(AST.Node)
	def printTree(self):
		raise Exception("printTree not defined in class " + self.__class__.__name__)

	@addToClass(AST.Integer)
	def printTree(self):
		printFun(self.value)

	@addToClass(AST.Float)
	def printTree(self):
		printFun(self.value)

	@addToClass(AST.String)
	def printTree(self):
		printFun(self.value)

	@addToClass(AST.ErrorNode)
	def printTree(self):
		print self.error
		
	@addToClass(AST.EmptyNode)
	def printTree(self):
		pass
		
	@addToClass(AST.Program)
	def printTree(self):
		pass
		self.dec.printTree()
		self.fun.printTree()
		self.ins.printTree()
		
	@addToClass(AST.Declarations)
	def printTree(self):
		global level
		level += 1
		
		for d in self.dec:
			d.printTree()
			
		level -= 1

	
	@addToClass(AST.Declaration)
	def printTree(self):
		pass
		printFun("var")
		self.inits.printTree()
		
	@addToClass(AST.Inits)
	def printTree(self):
		counter = 0;
		for i in self.inits:
			i.printTree()
			counter+=1
			if counter < len(self.inits):
				print ",",

		print

	@addToClass(AST.Init)
	def printTree(self):
		global level
		level += 1
		
		printFun(self.id, 1)
		printFun("=", 1)
		self.exp.printTree()
		
		level -= 1
		
	@addToClass(AST.Expression)
	def printTree(self):
		pass

	@addToClass(AST.IdentExpression)
	def printTree(self):
		global level
		level += 1
		printFun(self.id)
		
		level -= 1

	@addToClass(AST.ConstExpression)
	def printTree(self):
		global level
		level += 1
		
		self.value.printTree()
		
		level -= 1

	@addToClass(AST.ParenthesizedExpression)
	def printTree(self):
		self.exp.printTree()

	@addToClass(AST.BinaryExpression)
	def printTree(self):
		global level
		level += 1
		
		self.op1.printTree()
		printFun(self.type)
		self.op2.printTree()
		
		level -= 1

	@addToClass(AST.LabeledExpression)
	def printTree(self):
		global level
		level += 1
		
		#printFun("FUNCALL")
		printFun(self.id, 1)
		print "(",
		self.exp.printTree()
		print ")"
		
		level -= 1

	@addToClass(AST.Instructions)
	def printTree(self):

		for i in self.ins:
			i.printTree()

	@addToClass(AST.PrintInstruction)
	def printTree(self):
		global level
		level += 1
		
		printFun("PRINT")
		self.exp.printTree()
		
		level -= 1

	@addToClass(AST.LabeledInstruction)
	def printTree(self):
		global level
		level += 1
		
		printFun(self.id)
		self.ins.printTree()
		
		level -= 1

	@addToClass(AST.Assignment)
	def printTree(self):
		global level
		level += 1
		
		printFun(self.id, 1)
		printFun("=")
		self.exp.printTree()
		
		level -= 1

	@addToClass(AST.ChoiceInstruction)
	def printTree(self):
		global level
		level += 1
		
		printFun("if")
		self.cond.printTree()

		print "{"
		self.ifIns.printTree()
		print
		print "}"
		if self.elIns:
			printFun("else")
			print "{"
			self.elIns.printTree()
			print 
			print "}"
			
		level -= 1

	@addToClass(AST.WhileInstruction)
	def printTree(self):
		global level
		level += 1
		
		printFun("WHILE")
		self.cond.printTree()
		self.ins.printTree()
		
		level -= 1

	@addToClass(AST.RepeatInstruction)
	def printTree(self):
		global level
		level += 1
		
		printFun("REPEAT")
		self.ins.printTree()
		self.cond.printTree()
		
		level -= 1

	@addToClass(AST.ReturnInstruction)
	def printTree(self):
		global level
		level += 1
		
		printFun("return")
		self.exp.printTree()
		
		level -= 1

	@addToClass(AST.ContinueInstruction)
	def printTree(self):
		global level
		level += 1
		
		printFun("CONTINUE")
		
		level -= 1

	@addToClass(AST.BreakInstruction)
	def printTree(self):
		global level
		level += 1
		
		printFun("BREAK")
		
		level -= 1

	@addToClass(AST.CompoundInstruction)
	def printTree(self):
		self.dec.printTree()
		self.ins.printTree()

	@addToClass(AST.Condition)
	def printTree(self):
		print "(",
		self.exp.printTree()
		print ")"

	@addToClass(AST.ExpressionList)
	def printTree(self):
		counter =0
		for e in self.exp:
			counter +=1
			e.printTree()
			if counter < len(self.exp):
				print ",",


	@addToClass(AST.Fundefs)
	def printTree(self):
		for f in self.funs:
			f.printTree()

	@addToClass(AST.Fundef)
	def printTree(self):
		global level
		level += 1
		
		printFun("function")
		printFun(self.id, 1)
		#printFun("RET " + self.type, 1)
		self.args.printTree()
		print "{"
		self.instr.printTree()
		print "}"
		
		level -= 1

	@addToClass(AST.ArgsList)
	def printTree(self):
		global level
		level += 1
		print "(",
		counter = 0;
		for arg in self.args:
			arg.printTree()
			counter+=1
			if counter < len(self.args):
				print ",",
		print ")"
			
		level -= 1

	@addToClass(AST.Arg)
	def printTree(self):
		printFun(self.id)
		
		

