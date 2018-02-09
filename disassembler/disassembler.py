'''

@author: Kevin Walther
@class: RE/VA 695.744 Spring 2018
@assignment: Homework 2
@brief: This Python program implements a disassembler.

'''


import os 


registerAddressDict = {
	'000': 'eax', 
	'001': 'ecx', 
	'010': 'edx', 
	'011': 'ebx', 
	'100': 'esp', 
	'101': 'ebp', 
	'110': 'esi', 
	'111': 'edi'
}
opcodeDict = {
	'add': ['01', '03', '05', '81'],
	'and': ['25', '81', '21', '23'],
	'call': ['E8', 'FF', '9A'],
	'clflush': ['0FAE'],
	'cmp': ['3D', '81', '39', '3B'],
	'dec': ['FF', '48'],
	'idiv': ['F7'],
	'imul': ['F7', '0FAF', '69'],
	'inc': ['FF', '40'],
	'jmp': ['EB', 'E9', 'FF', 'EA'],
	'jz': ['74', '0F84'],
	'jnz': ['75', '0F85'],
	'lea': ['8D'],
	'mov': ['89', '8B', 'A1', 'A3', 'B8', 'C7'],
	'movsd': ['A5'],
	'mul': ['F7'],
	'neg': ['F7'],
	'nop': ['90', '0F1F'],
	'not': ['F7'],
	'or': ['0D', '81', '09', '0B'],
	'out': ['EE', 'EF'],
	'pop': ['8F', '58', '1F', '07', '17', '0FA1', '0FA9'],
	'push': ['FF', '50', '68', '0E', '16', '1E', '06', '0FA0', '0FA8'],
	'repne cmpsd': ['F3A6', 'F3A7', 'F2A6', 'F2A7'],
	'retf': ['CA', 'CB'],
	'retn': ['C2', 'C3'],
	'sal': ['D1'],
	'sar': ['D1'],
	'sbb': ['1D', '81', '19', '1B'],
	'shr': ['D1'],
	'test': ['A9', 'F7', '85'],
	'xor': ['35', '81', '31', '33']
}

# Define a list of opcodes that are accompanied by a MODRM byte.
modrmOpcodesList = ['01', '03', '09', '0B', '0F1F', '0FAF', '19', '1B', '21', '23', '31', '33', 
		'39', '3B', '69', '81', '85', '89', '8B', '8D', '8F', 'C7', 'D1', 'F7', 'FF'] 
# Define a list of instructions that often use a MODRM byte.
modrmInstructionsList = ['add', 'and', 'cmp', 'dec', 'idiv', 'imul', 
		'inc', 'jmp', 'lea', 'mov', 'mul', 'neg', 'nop', 'not', 'or', 
		'pop', 'push', 'sal', 'sar', 'sbb', 'shr', 'test', 'xor']

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

# Define a helper function to return the string representation of a bit within a byte.
def getBit(curByte, bitIndex):
	# Given an index into the byte, return the string '0' or '1'.
	return str((ord(curByte) >> bitIndex) & 1)

# Define a class to hold temporary instructions as we read them.
class IntelInstruction():
	def __init__(self):
		self.prefix, self.opcode, self.modrm, self.displacement, self.immediate = None, None, None, None, None
		self.mnemonic = ''
		
	# Check if the current opcode has a MODRM byte.
	def hasModrm(self):
		for opName, op in opcodeDict.items():
			if self.opcode.hex() in modrmOpcodesList:
				return True
		return False
		
	# Process the current MODRM byte.	
	def processModrm(self, curByte):
		# Interpret the components of the MODRM byte.
		mod = getBit(curByte, 7) + getBit(curByte, 6)
		reg = getBit(curByte, 5) + getBit(curByte, 4) + getBit(curByte, 3)
		rm = getBit(curByte, 2) + getBit(curByte, 1) + getBit(curByte, 0)
		# Check for existence of unsupported SIB byte.
		if (mod != '11') and (rm == '100'):
			print('WARNING: SIB byte detected in instruction. This is unsupported!')
			# throw exception
			
		# Check if this opcode has an REG field extension (i.e. this opcode is used with multiple instruction types).
		if self.opcode.hex() in opcodesWithExtension.keys():
			self.mnemonic = (opcodesWithExtension[self.opcode.hex()])[reg]
		# Otherwise, one-to-one mapping from opcode to instruction type.
		else:
			self.mnemonic = [opName for opName, op in opcodeDict.items() if self.opcode.hex() in op][0]
		# Check for memory access addressing mode.
		if mod == '00':
			regString = registerAddressDict[reg]
			rmString = '[' + registerAddressDict[rm] + ']'
		# Check for memory access addressing mode with 1-byte displacement.
		elif mod == '01':
			regString = registerAddressDict[reg]
			rmString = '[' + registerAddressDict[rm] + '+disp8]'
		# Check for memory access addressing mode with 4-byte displacement.
		elif mod == '10':
			regString = registerAddressDict[reg]
			rmString = '[' + registerAddressDict[rm] + '+disp32]'
		# Check for direct register access addressing mode.
		elif mod == '11':
			regString = registerAddressDict[reg]
			rmString = registerAddressDict[rm]
		print('Opcode: ' + self.mnemonic + ', REG: ' + regString + ', R/M: ' + rmString)
		
		# TODO: Determine ordering of operands.
		# TODO: Check for disp8 or disp32 and process displacements.
		
		
# Define a class to hold and track the stateful disassembler variables.
class Disassembler():
	def __init__(self, inputFileId):
		self.fileId = inputFileId
		self.tempByte = None
		self.nextByte = None
		self.tempInstruction = None
		self.instructionList = []

	def getNextByte(self):
		self.tempByte = self.nextByte
		self.nextByte = self.fileId.read(1)
		
	@property
	def opcodeHexStringList(self):
		return [opcode for opcodeList in opcodeDict.values() for opcode in opcodeList]

	# Process the current byte of data.
	def processFile(self):
		self.getNextByte()
		while(1):
			# Attempt to process a new instruction.
			try: 
				self.getNextByte()
				# Check for the end of the file.
				if (self.tempByte.hex() == ''):
					break
				# if self.tempInstruction is None:
				self.tempInstruction = IntelInstruction()
				self.identifyOpcode()
				self.processModrm()
			except ValueError as err:
				print('WARNING: ' + err.args[0])
				continue
			except:
				print('WARNING: Problem processing this instruction!')
				continue
				
	# Process the current opcode.	
	def identifyOpcode(self):
		print('Processing opcode: ' + self.tempByte.hex())
		# Check for a 1-byte opcode match.
		if self.tempByte.hex() in self.opcodeHexStringList:
			self.tempInstruction.opcode = self.tempByte
		else:
			tempOpcode = self.tempByte + self.nextByte
			# Check for a 2-byte opcode match.
			if tempOpcode.hex() in self.opcodeHexStringList:
				self.tempInstruction.opcode = tempOpcode
				self.getNextByte()
			else:
				# No matching opcode.
				print('WARNING: Unsupported opcode detected')
				raise ValueError('Unsupported opcode detected: ' + self.tempByte.hex() + ' or ' + tempOpcode.hex())

	# Process the current MODRM byte.	
	def processModrm(self):
		if self.tempInstruction.hasModrm():
			self.tempInstruction.processModrm(self.nextByte)
			self.getNextByte()
			
	# Process the current displacement.	
	def processDisplacement(self, curChar):
		pass

	# Process the current immediate.	
	def processImmediate(self, curChar):
		pass


def processInputFile(inputFile):
	inputFilePath = os.path.join(os.path.dirname(os.path.abspath(__file__)), inputFile)
	with open(inputFilePath, 'br') as fileId:
		disassembler = Disassembler(fileId)
		disassembler.processFile()
		
# Begin code execution here.
if __name__ == "__main__":
	processInputFile('example2.o')
	print('Successful Completion!')
	






