'''

@author: Kevin Walther
@assignment: RE/VA 695.744 Spring 2018 - Homework 2
@class: Modrm
@brief: This class stores information about the MODRM byte within an Intel instruction.

'''


# Define a helper function to return the string representation of a bit within a byte.
def getBit(curByte, bitIndex):
	# Given an index into the byte, return the string '0' or '1'.
	return str((ord(curByte) >> bitIndex) & 1)

	
class Modrm():

	def __init__(self, curByte):
		self.fullByte = curByte
		# Interpret the components of the MODRM byte.
		self.mod = getBit(curByte, 7) + getBit(curByte, 6)
		self.reg = getBit(curByte, 5) + getBit(curByte, 4) + getBit(curByte, 3)
		self.rm = getBit(curByte, 2) + getBit(curByte, 1) + getBit(curByte, 0)
		self.regString, self.rmString = '', ''
		
		