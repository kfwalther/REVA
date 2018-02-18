'''

@author: Kevin Walther
@assignment: RE/VA 695.744 Spring 2018 - Homework 2
@class: Disassembler
@brief: This class stores information about disassembler process as a whole.

'''


from Modrm import Modrm
from IntelInstruction import IntelInstruction
import IntelDefinitions

# Define a class to hold and track the stateful disassembler variables.
class Disassembler():
	def __init__(self, inputFileId):
		self.fileId = inputFileId
		self.tempByte = None
		self.nextByte = None
		self.byteCounter = 0
		self.tempInstruction = None
		self.instructionList = []
		self.jumpLabelList = []
		
	# Define a method to read the next byte from file, and increment counters.
	def getNextByte(self):
		self.tempByte = self.nextByte
		self.nextByte = self.fileId.read(1)
		self.byteCounter += 1
		if self.tempInstruction is not None:
			if self.tempInstruction.byteList is None:
				self.tempInstruction.byteList = self.tempByte
			else:
				self.tempInstruction.byteList += self.tempByte
		return None

	# Process the current byte of data.
	def processFile(self):
		self.getNextByte()
		# Loop forever, living life on the edge!
		while (1):
			# Attempt to process a new instruction.
			try:
				self.tempInstruction = IntelInstruction(self.byteCounter - 1)
				self.getNextByte()
				# Check for the end of the file.
				# TODO: Is there a more sure-fire way to exit?
				if (self.tempByte.hex() == ''):
					break
				self.processPrefix()
				self.identifyOpcode()
				self.processModrm()
				self.tempInstruction.processOperandOrdering()
				self.processDisplacement()
				self.processImmediate()
				self.instructionList.append(self.tempInstruction)
			except ValueError as err:
				# Save the unsupported byte or instruction to display to user.
				self.tempInstruction.mnemonic = '(Unknown instruction)'
				self.instructionList.append(self.tempInstruction)
				print('WARNING: ' + err.args[0])
				continue
# 			except:
# 				print('WARNING: Problem processing this instruction!')
# 				continue
				
	# Define a method to identify and save any prefixes that are encountered.
	def processPrefix(self):
		if self.tempByte.hex().upper() in IntelDefinitions.prefixList:
			# Currently only supporting the 'F2' prefix (REPNE).
			if self.tempByte.hex().upper() == 'F2':
				self.tempInstruction.prefix = self.tempByte
				self.getNextByte()
		
	# Process the current opcode.	
	def identifyOpcode(self):
		# Check for a 1-byte opcode match.
		if self.tempInstruction.oneByteOpcodeMatch(self.tempByte):
			self.tempInstruction.opcode = self.tempByte
		else:
			tempOpcode = self.tempByte + self.nextByte
			# Check for a 2-byte opcode match.
			if tempOpcode.hex().upper() in self.tempInstruction.opcodeHexStringList:
				self.tempInstruction.opcode = tempOpcode
				self.getNextByte()
			else:
				# No matching opcode.
				raise ValueError('Unsupported opcode detected: ' + self.tempByte.hex().upper() + ' or ' + tempOpcode.hex().upper())

	# Process the current MODRM byte.
	def processModrm(self):
		if self.tempInstruction.hasModrm():
			# Must process MODRM components to determine mnemonic.
			self.getNextByte()
			self.tempInstruction.processModrm(self.tempByte)
		else:
			# If no MODRM, we have enough info already to determine mnemonic.
			self.tempInstruction.mnemonic = self.tempInstruction.getMnemonicFromOpcode()
			
	# Process the current displacement.	
	def processDisplacement(self):
		# Check if we need to process an 8-bit displacement value.
		if self.tempInstruction.DISP8 in self.tempInstruction.operands:
			self.processByteDisplacement()
		# Check if we need to process a 32-bit displacement value.
		elif self.tempInstruction.DISP32 in self.tempInstruction.operands:
			self.processDoubleWordDisplacement()
		
	# Process a 1-byte displacement.	
	def processByteDisplacement(self):
		# Check for a displacement jump/call instruction, so we can save a label.
		if self.tempInstruction.operandEncoding is 'D':
			# Calculate the offset, checking for overflow.
			# TODO: Is this the correct address to jump to in each 8/32-bit case?
			offset = self.tempInstruction.performSignedInt8Addition(
					self.byteCounter, int.from_bytes(self.nextByte, byteorder='little'))
			self.jumpLabelList.append(offset)
			self.tempInstruction.operands = self.tempInstruction.operands.replace(self.tempInstruction.DISP8, ('offset_' + ('%0.8X' % offset)))
		else:
			self.tempInstruction.operands = self.tempInstruction.operands.replace(self.tempInstruction.DISP8, '0x' + self.nextByte.hex().upper())
		self.getNextByte()
			
	# Process a double word displacement (32 bits).
	def processDoubleWordDisplacement(self):
		tempBytes = [self.tempByte for i in range(0,4) if self.getNextByte() is None]
		# Save the displacement in big endian.
		tempWord = tempBytes[3] + tempBytes[2] + tempBytes[1] + tempBytes[0]
		# Check for a 4-byte displacement jump instruction, so we can save a label.
		if self.tempInstruction.operandEncoding is 'D':
			# Calculate the offset, checking for overflow.
			offset = self.tempInstruction.performSignedInt32Addition(
					self.byteCounter, int.from_bytes(tempWord, byteorder='big'))
			self.jumpLabelList.append(offset)
			self.tempInstruction.operands = self.tempInstruction.operands.replace(self.tempInstruction.DISP32, ('offset_' + ('%0.8X' % offset)))
		else:
			self.tempInstruction.operands = self.tempInstruction.operands.replace(self.tempInstruction.DISP32, '0x' + tempWord.hex().upper())
	
	# Process the current immediate.	
	def processImmediate(self):
		# Check if we need to process an 16-bit immediate value.
		if self.tempInstruction.IMM16 in self.tempInstruction.operands:	
			tempBytes = [self.tempByte for i in range(0,2) if self.getNextByte() is None]	
			tempWord = tempBytes[1] + tempBytes[0]
			self.tempInstruction.operands = self.tempInstruction.operands.replace(self.tempInstruction.IMM16, '0x' + tempWord.hex().upper())
		# Check if we need to process an 32-bit immediate value.
		if self.tempInstruction.IMM32 in self.tempInstruction.operands:	
			tempBytes = [self.tempByte for i in range(0,4) if self.getNextByte() is None]	
			tempWord = tempBytes[3]
			for i in range(0,3):
				tempWord = tempWord + tempBytes[2-i]
			self.tempInstruction.operands = self.tempInstruction.operands.replace(self.tempInstruction.IMM32, '0x' + tempWord.hex().upper())
			
	# Define a method to print the parsed instructions.
	def printInstructions(self):
		lastMemPosition = 0
		for instruction in self.instructionList:
			for curLabel in self.jumpLabelList:
				if ((curLabel > lastMemPosition) and (curLabel <= instruction.memoryPosition)):
					print('offset_' + ('%0.8X' % curLabel))
			print(('%0.8X' % instruction.memoryPosition) + ':\t' + instruction.byteList.hex().upper() + '\t' + instruction.mnemonic + ' ' + instruction.operands)
			lastMemPosition = instruction.memoryPosition










