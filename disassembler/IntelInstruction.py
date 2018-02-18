'''

@author: Kevin Walther
@assignment: RE/VA 695.744 Spring 2018 - Homework 2
@class: IntelInstruction
@brief: This class stores information about the MODRM byte within an Intel instruction.

'''

from Modrm import Modrm
import IntelDefinitions

opcodeExtension81 = {
	'000': 'add', 
	'001': 'or', 
	'011': 'sbb', 
	'100': 'and', 
	'110': 'xor', 
	'111': 'cmp'
}

opcodeExtensionD1 = {
	'100': 'sal', 
	'101': 'shr', 
	'111': 'sar'
}

opcodeExtensionF7 = {
	'000': 'test', 
	'010': 'not', 
	'011': 'neg', 
	'100': 'mul', 
	'101': 'imul', 
	'111': 'idiv'
}

opcodeExtensionFF = {
	'000': 'inc', 
	'001': 'dec', 
	'010': 'call', 
	'011': 'call', 
	'100': 'jmp', 
	'101': 'jmp', 
	'110': 'push'
}

opcodesWithExtension = {
	'81': opcodeExtension81, 
	'D1': opcodeExtensionD1,
	'F7': opcodeExtensionF7,
	'FF': opcodeExtensionFF
}

# Define a class to hold temporary instructions as we read them.
class IntelInstruction():
	
	def __init__(self, memPosition):
		self.prefix, self.opcode, self.modrm, self.displacement, self.immediate = None, None, None, None, None
		self.mnemonic = ''
		self.operands = ''
		self.operandEncoding = ''
		self.opcodeBase, self.offset = None, 0
		self.byteList = None
		self.memoryPosition = memPosition
		self.DISP8, self.DISP32, self.IMM8, self.IMM16, self.IMM32  = 'disp8', 'disp32', 'imm8', 'imm16', 'imm32'
		
	@property
	def opcodeHexStringList(self):
		return [opcode for opcodeList in IntelDefinitions.opcodeDict.values() for opcode in opcodeList]
		
	# Define a helper function to perform 8-bit signed integer addition.
	def performSignedInt8Addition(self, op1, op2):
		# Assume operand 2 is the only one we need to worry about (check its sign bit).
		if (op2 & 0x80):
			return (op1 + (op2 - 0x100))
		else:
			return (op1 + op2)
	
	# Define a helper function to perform 32-bit signed integer addition.
	def performSignedInt32Addition(self, op1, op2):
		# Assume operand 2 is the only one we need to worry about (check its sign bit).
		if (op2 & 0x80000000):
			return (op1 + (op2 - 0x100000000))
		else:
			return (op1 + op2)
			
	# Define a function to return the mnemonic for the current opcode (assumes a 1-to-1 mapping).
	# Cases which do not have 1-to-1 mapping use opcode extensions, and are handled in processModrm() function.
	def getMnemonicFromOpcode(self):
		return [opName for opName, op in IntelDefinitions.opcodeDict.items() if self.opcodeBase.hex().upper() in op][0]
		
	# Define a method to check for a 1-byte opcode match.
	def oneByteOpcodeMatch(self, curByte):
		# Check for an exact match or if the opcode has an offset from its base opcode value.
		if curByte.hex().upper() in self.opcodeHexStringList:
			self.opcode = curByte
			self.opcodeBase = curByte
			return True
		elif self.checkOpcodeWithinRange(curByte):
			self.opcode = curByte
			return True
		else:
			return False
		
	# Check if the opcode is within a range (cases where base opcode can have register number added).
	def checkOpcodeWithinRange(self, curByte):
		baseOpcodes = [ops for opEn, opList in IntelDefinitions.opcodeOpEnDict.items() if (opEn == 'O') or (opEn == 'OI') for ops in opList]
		for op in baseOpcodes:
			opInt = int(op, 16)
			curByteInt = int.from_bytes(curByte, byteorder='little')
			# Check if current opcode is within range: [opcodeBase, opcodeBase + 8]
			if (curByteInt > opInt) and (curByteInt < (opInt + 8)):
				self.offset = curByteInt - opInt
				self.opcodeBase = bytes.fromhex(op)
				return True
		return False
			
	# Check if the current opcode has a MODRM byte.
	def hasModrm(self):
		if self.opcode.hex().upper() in IntelDefinitions.modrmOpcodesList:
			return True
		return False
					
	# Process the current MODRM byte.	
	def processModrm(self, curByte):
		# Create a new modrm object to track its information.
		self.modrm = Modrm(curByte)
		# Check for existence of unsupported SIB byte.
		if (self.modrm.mod != '11') and (self.modrm.rm == '100'):
			raise ValueError('SIB byte detected in instruction. This is unsupported!')
					
		# Check if this opcode has an REG field extension (i.e. this opcode is used with multiple instruction types).
		if self.opcode.hex().upper() in opcodesWithExtension.keys():
			self.mnemonic = (opcodesWithExtension[self.opcode.hex().upper()])[self.modrm.reg]
		# Otherwise, one-to-one mapping from opcode to instruction type.
		else:
			self.mnemonic = self.getMnemonicFromOpcode()
			
		# Check for invalid LEA instruction format.
		if ((self.mnemonic == 'lea') and (self.modrm.mod == '11')):
			raise ValueError('Illegal LEA instruction detected!')
		
		# TODO: Ensure square brackets on LEA and CLFLUSH are applied properly.
		
		# Check for memory access addressing mode.
		if self.modrm.mod == '00':
			self.modrm.regString = IntelDefinitions.registerAddressDict[self.modrm.reg]
			if self.modrm.rm == '101':
				# TODO: Check if this interpretation of the MODRM definition is correct...
				self.modrm.rmString = self.DISP32
			else:
				self.modrm.rmString = '[' + IntelDefinitions.registerAddressDict[self.modrm.rm] + ']'
		# Check for memory access addressing mode with 1-byte displacement.
		elif self.modrm.mod == '01':
			self.modrm.regString = IntelDefinitions.registerAddressDict[self.modrm.reg]
			self.modrm.rmString = '[' + IntelDefinitions.registerAddressDict[self.modrm.rm] + '+' + self.DISP8 + ']'
		# Check for memory access addressing mode with 4-byte displacement.
		elif self.modrm.mod == '10':
			self.modrm.regString = IntelDefinitions.registerAddressDict[self.modrm.reg]
			self.modrm.rmString = '[' + IntelDefinitions.registerAddressDict[self.modrm.rm] + '+' + self.DISP32 + ']'
		# Check for direct register access addressing mode.
		elif self.modrm.mod == '11':
			self.modrm.regString = IntelDefinitions.registerAddressDict[self.modrm.reg]
			self.modrm.rmString = IntelDefinitions.registerAddressDict[self.modrm.rm]
		
	# Define a function to determine the ordering of operands.
	def processOperandOrdering(self):
		# Lookup the operand encoding for the opcode, to determine the ordering of operands.
		operandEncoding = [opEn for opEn, ops in IntelDefinitions.opcodeOpEnDict.items() if self.opcodeBase.hex().upper() in ops]
		# Account for opcodes that can have multiple operand encodings (right now just F7).
		if len(operandEncoding) > 1:
			if self.modrm.reg == '000':
				# This is the 'F7 /0' case (TEST instruction).
				self.operandEncoding = 'MI'
			else:
				# These are the other 'F7 /X' cases.
				self.operandEncoding = 'M'
		else:
			self.operandEncoding = operandEncoding[0]
		if self.operandEncoding == 'M':
			self.operands = self.modrm.rmString + ', ' + self.modrm.regString
		elif self.operandEncoding == 'MI':
			self.operands = self.modrm.rmString + ', ' + self.IMM32
		elif self.operandEncoding == 'MR':
			self.operands = self.modrm.rmString + ', ' + self.modrm.regString
		elif self.operandEncoding == 'RM':
			self.operands = self.modrm.regString + ', ' + self.modrm.rmString
		elif self.operandEncoding == 'RMI':
			self.operands = self.modrm.regString + ', ' + self.modrm.rmString + ', ' + self.IMM32
		elif self.operandEncoding == 'O':
			self.operands = IntelDefinitions.registerAddressDict['{:03b}'.format(self.offset)]
		elif self.operandEncoding == 'I':
			# Check for OUT instruction, which is actually an 8-bit immediate value.
			if self.opcodeBase.hex().upper() == 'E7':
				self.operands = self.IMM8
			# Check for the return instructions, which are only 16-bit immediate values.
			if self.opcodeBase.hex().upper() in ['C2', 'CA']:
				self.operands = self.IMM16
			else:
				self.operands = self.IMM32
		elif self.operandEncoding == 'OI':
			self.operands = IntelDefinitions.registerAddressDict['{:03b}'.format(self.offset)] + ', ' + self.IMM32
		elif self.operandEncoding == 'D':
			# Check for size of displacement based on specific opcode.
			if self.opcodeBase.hex().upper() in ['74', '75']:
				self.operands = self.DISP8
			elif self.opcodeBase.hex().upper() in ['E8', '0F84', '0F85', 'E9']:
				self.operands = self.DISP32
		elif self.operandEncoding == 'ZO':
			self.operands = ''
			
		
		
		