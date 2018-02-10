'''

@author: Kevin Walther
@class: RE/VA 695.744 Spring 2018
@assignment: Homework 2
@brief: This Python program implements a disassembler.

'''

from Modrm import Modrm
from IntelInstruction import IntelInstruction
import IntelDefinitions
import os
import sys


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
		return [opcode for opcodeList in IntelDefinitions.opcodeDict.values() for opcode in opcodeList]

	# Process the current byte of data.
	def processFile(self):
		self.getNextByte()
		while(1):
			# Attempt to process a new instruction.
# 			try: 
			self.getNextByte()
			# Check for the end of the file.
			if (self.tempByte.hex() == ''):
				break
			# if self.tempInstruction is None:
			self.tempInstruction = IntelInstruction()
			self.identifyOpcode()
			self.processModrm()
			# TODO: Do we need this function if no MODRM?
			self.tempInstruction.processOperandOrdering()
			print(self.tempInstruction.mnemonic + ' '  + self.tempInstruction.operands)
# 			except ValueError as err:
# 				print('WARNING: ' + err.args[0])
# 				continue
# 			except:
# 				print('WARNING: Problem processing this instruction!')
# 				continue
				
	# Process the current opcode.	
	def identifyOpcode(self):
		print('Processing opcode: ' + self.tempByte.hex())
		# Check for a 1-byte opcode match.
		if self.tempByte.hex() in self.opcodeHexStringList:
			self.tempInstruction.opcode = self.tempByte
		elif self.tempInstruction.checkOpcodeWithinRange(self.tempByte):
			self.getNextByte()
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
	processInputFile('example1.o')
	print('Successful Completion!')
	






