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
	
	def __init__(self):
		self.prefix, self.opcode, self.modrm, self.displacement, self.immediate = None, None, None, None, None
		self.mnemonic = ''
		self.operands = ''
		
	# Check if the current opcode has a MODRM byte.
	def hasModrm(self):
		for opName, op in IntelDefinitions.opcodeDict.items():
			if self.opcode.hex() in IntelDefinitions.modrmOpcodesList:
				return True
		return False
		
	# Process the current MODRM byte.	
	def processModrm(self, curByte):
		# Create a new modrm object to track its information.
		self.modrm = Modrm(curByte)
		# Check for existence of unsupported SIB byte.
		if (self.modrm.mod != '11') and (self.modrm.rm == '100'):
			print('WARNING: SIB byte detected in instruction. This is unsupported!')
			# throw exception
			
		# TODO: Check for address mode '00' and R/M field == '101' (disp32 case)
		
		# Check if this opcode has an REG field extension (i.e. this opcode is used with multiple instruction types).
		if self.opcode.hex() in opcodesWithExtension.keys():
			self.mnemonic = (opcodesWithExtension[self.opcode.hex()])[self.modrm.reg]
		# Otherwise, one-to-one mapping from opcode to instruction type.
		else:
			self.mnemonic = [opName for opName, op in IntelDefinitions.opcodeDict.items() if self.opcode.hex() in op][0]
			
		# Check for memory access addressing mode.
		if self.modrm.mod == '00':
			self.modrm.regString = IntelDefinitions.registerAddressDict[self.modrm.reg]
			self.modrm.rmString = '[' + IntelDefinitions.registerAddressDict[self.modrm.rm] + ']'
		# Check for memory access addressing mode with 1-byte displacement.
		elif self.modrm.mod == '01':
			self.modrm.regString = IntelDefinitions.registerAddressDict[self.modrm.reg]
			self.modrm.rmString = '[' + IntelDefinitions.registerAddressDict[self.modrm.rm] + '+disp8]'
		# Check for memory access addressing mode with 4-byte displacement.
		elif self.modrm.mod == '10':
			self.modrm.regString = IntelDefinitions.registerAddressDict[self.modrm.reg]
			self.modrm.rmString = '[' + IntelDefinitions.registerAddressDict[self.modrm.rm] + '+disp32]'
		# Check for direct register access addressing mode.
		elif self.modrm.mod == '11':
			self.modrm.regString = IntelDefinitions.registerAddressDict[self.modrm.reg]
			self.modrm.rmString = IntelDefinitions.registerAddressDict[self.modrm.rm]
		
	# Define a function to determine the ordering of operands.
	def processOperandOrdering(self):
		# Lookup the operand encoding for the opcode, to determine the ordering of operands.
		operandEncoding = [opEn for opEn, ops in IntelDefinitions.opcodeOpEnDict.items() if self.opcode.hex() in ops][0]
		if operandEncoding == 'M':
			self.operands = self.modrm.rmString + ', ' + self.modrm.regString
		elif operandEncoding == 'MI':
			self.operands = self.modrm.rmString + ', ' + 'imm32'
		elif operandEncoding == 'MR':
			self.operands = self.modrm.rmString + ', ' + self.modrm.regString
		elif operandEncoding == 'RM':
			self.operands = self.modrm.regString + ', ' + self.modrm.rmString
		elif operandEncoding == 'RMI':
			self.operands = self.modrm.regString + ', ' + self.modrm.rmString + ', ' + 'imm32'
		elif operandEncoding == 'O':
			self.operands = self.modrm.regString
		elif operandEncoding == 'I':
			self.operands = 'imm32'
		elif operandEncoding == 'OI':
			self.operands = self.modrm.regString + ', ' + 'imm32'
		elif operandEncoding == 'D':
			self.operands = 'disp32'
		elif operandEncoding == 'FD':
			self.operands = 'eax, disp32'
		elif operandEncoding == 'TD':
			self.operands = 'disp32, eax'
		elif operandEncoding == 'ZO':
			self.operands = ''
			
		# TODO: Check for disp8 or disp32 and process displacements.
		
		
		