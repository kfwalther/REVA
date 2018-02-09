'''

@author: Kevin Walther
@class: RE/VA 695.744 Spring 2018
@assignment: Homework 2
@brief: This Python program implements a disassembler.

'''


import os 

opcodeDict = 	{'add': ['0x00', '0x01', '0x02', '0x03', '0x04', '0x05', '0x80', '0x81', '0x83'],
				'and': ['0x24', '0x25', '0x80', '0x81', '0x83', '0x20', '0x21', '0x22', '0x23'],
				'call': ['0xE8', '0xFF', '0x9A'],
				'clflush': ['0x0FAE', '', '', '', '', '', '', ''],
				'cmp': ['0x3C', '0x3D', '0x80', '0x81', '0x83', '0x38', '0x39', '0x3A', '0x3B'],
				'dec': ['0xFE', '0xFF', '0x48'],
				'idiv': ['0xF6', '0xF7'],
				'imul': ['0xF6', '0xF7', '0x0FAF', '0x6B', '0x69'],
				'inc': ['0xFE', '0xFF', '0x40'],
				'jmp': ['0xEB', '0xE9', '0xFF', '0xEA'],
				'jz': ['0x74', '0x0F84'],
				'jnz': ['0x75', '0x0F85'],
				'lea': ['0x8D'],
				'mov': ['0x88', '0x89', '0x8A', '0x8B', '0x8C', '0x8E', '0xA0', '0xA1', '0xA2', '0xA3', '0xB0', '0xB8', '0xC6', '0xC7'],
				'movsd': ['0xA4', '0xA5'],
				'mul': ['0xF6', '0xF7'],
				'neg': ['0xF6', '0xF7'],
				'nop': ['0x90', '0x0F1F'],
				'not': ['0xF6', '0xF7'],
				'or': ['0x0C', '0x0D', '0x80', '0x81', '0x83', '0x08', '0x09', '0x0A', '0x0B'],
				'out': ['0xE6', '0xE7', '0xEE', '0xEF'],
				'pop': ['0x8F', '0x58', '0x1F', '0x07', '0x17', '0x0FA1', '0x0FA9'],
				'push': ['0xFF', '0x50', '0x6A', '0x68', '0x0E', '0x16', '0x1E', '0x06', '0x0FA0', '0x0FA8'],
				'repne cmpsd': ['0xF3A6', '0xF3A7', '0xF2A6', '0xF2A7'],
				'retf': ['0xCA', '0xCB'],
				'retn': ['0xC2', '0xC3'],
				'sal': ['0xD0', '0xD2', '0xC0', '0xD1', '0xD3', '0xC1'],
				'sar': ['0xD0', '0xD2', '0xC0', '0xD1', '0xD3', '0xC1'],
				'sbb': ['0x1C', '0x1D', '0x80', '0x81', '0x83', '0x18', '0x19', '0x1A', '0x1B'],
				'shr': ['0xD0', '0xD2', '0xC0', '0xD1', '0xD3', '0xC1'],
				'test': ['0xA8', '0xA9', '0xF6', '0xF7', '0x84', '0x85'],
				'xor': ['0x34', '0x35', '0x80', '0x81', '0x83', '0x30', '0x31', '0x32', '0x33']
}

# Define a class to hold temporary instructions as we read them.
class IntelInstruction():
	def __init__(self):
		self.prefix, self.opcode, self.modrm, self.displacement, self.immediate = None, None, None, None, None
		

# Define a class to hold and track the stateful disassembler variables.
class Disassembler():
	def __init__(self, inputFileId):
		self.fileId = inputFileId
		self.tempByte = None
		#self.nextByte = None
		self.tempInstruction = None
		self.instructionList = []

	@property
	def getNextByte(self):
		self.tempByte = self.nextByte
		self.nextByte = self.fileId.read(1)
		
	# Process the current byte of data.
	def processFile(self):
		# if self.tempInstruction is None:
		self.tempByte = self.fileId.read(1)
		self.tempInstruction = IntelInstruction()
		self.processOpcode()
	
	# Process the current opcode.	
	def processOpcode(self):
		print('Processing opcode: ' + hex(self.tempByte))
		# Check for a 1-byte opcode match.
		if self.tempByte in [int(op, 16) for op in list(opcodeDict.values)]:
			self.tempInstruction.opcode = self.tempByte
		else:
			nextByte = self.fileId.read(1)
			tempOpcode = self.tempByte + nextByte
			# Check for a 2-byte opcode match.
			if tempOpcode in [int(op, 16) for op in list(opcodeDict.values)]:
				self.tempInstruction.opcode = tempOpcode
			else:
				# No matching opcode.
				print('WARNING: Invalid opcode detected')
				self.processOpcode
				
	# Process the current MODRM byte.	
	def processModrm(self, curChar):
		pass

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
	processInputFile('example1.o')
	






