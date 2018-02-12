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
		self.instructionBytesList = []

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
		while(1):
			# Attempt to process a new instruction.
			try: 
				self.tempInstruction = IntelInstruction()
				self.getNextByte()
				# Check for the end of the file.
				if (self.tempByte.hex() == ''):
					break
				self.identifyOpcode()
				self.processModrm()
				self.tempInstruction.processOperandOrdering()
				self.processDisplacement()
				self.processImmediate()
				self.instructionList.append(self.tempInstruction.mnemonic + ' '  + self.tempInstruction.operands)
				self.instructionBytesList.append(self.tempInstruction.byteList)
			except ValueError as err:
				print('WARNING: ' + err.args[0])
				continue
# 			except:
# 				print('WARNING: Problem processing this instruction!')
# 				continue
				
	# Process the current opcode.	
	def identifyOpcode(self):
# 		print('Processing opcode: ' + self.tempByte.hex().upper())
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
				print('WARNING: Unsupported opcode detected')
				raise ValueError('Unsupported opcode detected: ' + self.tempByte.hex().upper() + ' or ' + tempOpcode.hex().upper())

	# Process the current MODRM byte.	
	def processModrm(self):
		if self.tempInstruction.hasModrm():
			# Must process MODRM components to determine mnemonic.
			self.tempInstruction.processModrm(self.nextByte)
			self.getNextByte()
		else:
			# If no MODRM, we have enough info already to determine mnemonic.
			self.tempInstruction.mnemonic = self.tempInstruction.getMnemonicFromOpcode()
			
	# Process the current displacement.	
	def processDisplacement(self):
		# Check if we need to process an 8-bit displacement value.
		if 'disp8' in self.tempInstruction.operands:
			self.tempInstruction.operands = self.tempInstruction.operands.replace('disp8', '0x' + self.nextByte.hex().upper())
			self.getNextByte()
		# Check if we need to process a 32-bit displacement value.
		elif 'disp32' in self.tempInstruction.operands:
			tempBytes = [self.tempByte for i in range(0,4) if self.getNextByte() is None]	
			tempWord = tempBytes[3]
			for i in range(0,3):
				tempWord = tempWord + tempBytes[2-i]
			self.tempInstruction.operands = self.tempInstruction.operands.replace('disp32', '0x' + tempWord.hex().upper())

	# Process the current immediate.	
	def processImmediate(self):
		# Check if we need to process an 32-bit immediate value.
		if 'imm32' in self.tempInstruction.operands:	
			tempBytes = [self.tempByte for i in range(0,4) if self.getNextByte() is None]	
			tempWord = tempBytes[3]
			for i in range(0,3):
				tempWord = tempWord + tempBytes[2-i]
			self.tempInstruction.operands = self.tempInstruction.operands.replace('imm32', '0x' + tempWord.hex().upper())
			
	# Define a method to print the parsed instructions.
	def printInstructions(self):
		[print(instBytes.hex().upper() + ':\t' + instruction) for instBytes, instruction in zip(self.instructionBytesList, self.instructionList)]
